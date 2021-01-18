---
layout: post
title: Pytorch-TensorIterator
date: 2021-01-18 22:26:28 +0800
categories: [ML]
tags: [Pytorch]
---

> TensorIterator is a helper class for element-wise operations, such as arithmetic, comparisons, and trigonometric functions. It handles broadcasting and type conversions of operands.

一个TensorIterator的构建需要提供操作数，根据操作数的个数有一元(unary)、二元(binary)、无操作数(nullary)三种。操作数TensorOperand对参与运算的tensor进行包装，iterator内部维护两个容器inputs_和outputs_来复制操作数，进行后续操作。

> Note：input操作数和output操作数可能既是输入也是输出。

### Broadcast

* Broadcasting: [definition](https://numpy.org/doc/stable/user/basics.broadcasting.html#module-numpy.doc.broadcasting  https://numpy.org/devdocs/user/theory.broadcasting.html)

> Subject to certain constraints, the smaller array is “broadcast” across the larger array so that they have compatible shapes. 
广播操作是当两个参与运算的tensor维度或shape不一致时，要对较小size的维度进行扩张（stretch）。stretch并没有对tensor的数据进行拷贝，这也是为什么tensoriterator高效。两个操作数之间能否进行广播操作，需要通过以下条件判断：
- 每个tensor至少有一维（标量除外）
- 从尾部低维开始，相应的size要么相等，要么其中一个为1，要么有一个不存在

#### broadcastshape计算
维度扩充需要先判断tensor间是否是可广播的，然后根据规则将相应的size扩充至另一个tensor的大小。
维度的判断与推算主要在compute_shape中实现，这之间会对输入的操作数之间进行common shape计算（output此时并不参与common shape计算）：
1. 遍历操作数取公共集：
```cpp
for (auto& op : inputs_) {
    iter_block(op, true);
}
for (auto& op : outputs_) {
    iter_block(op, false);
}
```
iter_block中首先对传入的op判断是不是输入op：
  1. 不是输入：将op转为output_op。接下来判断op是不是允许resize：
    1. 不允许：判断是否同时也是输入op：
      1. 是：即为in-out一体的操作，需要判断此时的shape和最终的common shape是否一致，不一致，无法广播；
      2. 不是：Non-resize op，此时不参与common shape计算
    2. 允许：不论是不是input，后面再根据common shape resize
  2. 是输入：首先获取当前遍历到的操作数的维度，然后进行标量、标量判断。通过all_ops_same_shape来设置标志位。在循环计算common_shape时，infer_broad_size会在确实需要扩充维度时进行计算：

```cpp
inline std::vector<int64_t> infer_broadcast_size(IntArrayRef a, IntArrayRef b) {
    size_t dimsA = a.size();
    size_t dimsB = b.size();
    //lms 取二者较大的维度
    size_t ndim = dimsA > dimsB ? dimsA : dimsB;
    //lms expandedSizes 每个维度对应的数目，默认为0，已经包含维度不存在的情况
    std::vector<int64_t> expandedSizes(ndim);

    // Use ptrdiff_t to ensure signed comparison.
    for (ptrdiff_t i = (ptrdiff_t)ndim - 1; i >= 0; --i) {
        //lms ptrfiff_t 有符号比较
        ptrdiff_t offset = ndim - 1 - i;
        ptrdiff_t dimA = dimsA - 1 - offset;
        ptrdiff_t dimB = dimsB - 1 - offset;
        int64_t sizeA = (dimA >= 0) ? a[dimA] : 1;
        int64_t sizeB = (dimB >= 0) ? b[dimB] : 1;

        //
        TORCH_CHECK(
                sizeA == sizeB || sizeA == 1 || sizeB == 1,
                "The size of tensor 'A':(", sizeA,
                ") must match the size of tensor 'B':(", sizeB,
                ") at non-singleton dimension ", i);

        // 1s map to the other size (even 0).
        expandedSizes[i] = sizeA == 1 ? sizeB : sizeA;
    }
    return expandedSizes;
}
```
common_shape计算完成后，根据mutate_output_without_temp_来确定对传入的outputop的更新方式。当然，output op其他情况也被考虑到了。
output参与到shape计算的情况：output不在inputs_列表里，但是又被用户指定为outputs_，并且无法进行resize操作，此时在计算出inputs的common shape后，要考虑output的shape。
### Typepromotion
BroadCast Shape计算完后需要对不一致的dtype进行类型提升。同时也包括common device的计算。
DataPromotionStrategy
类型提升的策略/是否提升有四种：

```cpp
enum class DataPromotionStrategy : uint8_t {
    NONE, // Do not compute a common dtype and any check
    CHECK, // Compute and validate a common dtype but don't promote.
    PROMOTE_INPUTS, // Promote common dtype but only validate inputs (comparison ops have boolean output)
    PROMOTE // Promote to common dtype.
};
```

- NONE：策略下，不对dType提升，一般适用tensor的类型相同时
- CHECK ：仅计算commontype并检查
- PROMOTE_INPUTS 进行类型提升，但只对输入的提升结果进行验证，即为保证运算，必须对输入进行类型提升，但有可能输出本来就要求类型与输入不一致，例如比较操作，输出是bool类型的。这种情况下，要求通过output op的preferred_dtype指定输出的dtype。
- PROMOTE对输入输出都进行检查并提升类型。
#### Compute common device
```cpp
//lms 计算操作数的common device. operands为所有操作数 已第一个碰到的device为准
//qes
for (auto& op : operands) {
    if (!op->tensor().defined()) continue;
    if (op->tensor().n_dim() == 0) continue;
    return op->tensor().device();
}
for (auto& op : operands) {
    if (!op->tensor().defined()) continue;
    if (op->tensor().unsafeGetTensorImpl()->is_wrapped_number()) continue;
    return op->tensor().device();
}
return kCPU;
```
以第一个碰到的非0维op的device为准，后续可能调整。
#### Compute common dtype
1. 首先进行类型检查，由于输入类型都会给出，只需要对输出的类型进行检查，如果所有tensor的数据类型一致，直接返回device和type：
```cpp
bool missing_output_dtype = false;
for (auto& out_op : outputs_) {
    if (!out_op.defined() && out_op.preferred_dtype_ == ScalarType::Undefined) {
        missing_output_dtype = true;//lms 这种情况下output_type缺失
    }
}
```
检查标志位：need_compute_common_dtype_and_device
3. 在compute_common_type_函数中遍历所有操作数，计算common_type。先判断是否all_same_type：
```cpp
auto common_type = ScalarType::Undefined;
bool all_same_type = true;
for (const auto& op: operands){
    if (!op->defined()) { continue; }
    //don't handle scalars
    if (op->tensor().n_dim() > 0){
        ScalarType current = op->tensor().dtype().scalar_type();
        if (current == ScalarType::Undefined){
            TORCH_THROW_ERROR(Error, "DataType mustn't be equal to `Undefined` in `compute_common_type_`");
            all_same_type = false;
            break;
        }
        if (common_type == ScalarType::Undefined) common_type = current;
        if (common_type != current) {
            //lms 判断操作数tensor是不是为same type
            all_same_type = false;
            break;
        }
    } else {
        //lms 存在标量，all_same_type = false
        all_same_type = false;
        break;
    }
}
if (all_same_type) {
    //lms 类型一样
    return std::make_tuple(device, common_type, true);
}
```
4. device和common_type组合成tuple，进行最后一步的检查与更正：

```cpp
for (const auto& op : operands) {
    //lms 对所有操作数进行循环遍历，确定最终的state
    state = TORCH::computation::update_result_type_state(op->tensor(), state);
}
auto dtype = TORCH::computation::result_type(state);

auto result = std::make_tuple(device, dtype, false);
//lms 最终的dType 肯定不能为Undefned
TORCH_INTERNAL_ASSERT(dtype != ScalarType::Undefined);
return result;
```
这里TypePromotion这个类比较重要，负责处理类型不同时的情况：
TypePromotion有wrappedResult、dimResult、zeroResult三种scalar_type。wrappedResult处理tensor是由c++数据类型直接转化来的情况，dimResult处理正常tensor，zeroResult处理维度为0的情况。
TypePromotion首先对操作数的类型进行is_wrapped_number->isComplexType进行基本数据类型、复数的判断。然后根据tensor的具体情况，走wrappedResult、dimResult、zeroResult三个分支。每个分支都会走promote_skip_undefined，里面会进行查表确定类型：

在所有的操作数都经历过上面这个步骤后，维护的state的三个result会被联合比较取出最符合的作为result:

```cpp
static inline ScalarType combine_categories(ScalarType higher, ScalarType lower) {
    //lms
    /**
     * 1、higher 是复数，按复数来
     * 2、lower 不是复数，higher是float，那就按higher来
     * 3、bool是层级最低的
     * 4、查表确定 promoteTypes
     *
     */
    if(isComplexType(higher)) {
        return higher;
    }
    else if(!isComplexType(lower) && isFloatingType(higher)) {
        return higher;
    }
    if (higher == ScalarType::Bool || isFloatingType(lower) || isComplexType(lower)) {
        return promote_skip_undefined(higher, lower);
    }
    if (higher != ScalarType::Undefined) {
        return higher;
    }
    return lower;
}
```
得到了common device和common type，开始真正提升了，此时promote_and_check_block会对所有的输入输出op进行检查，根据策略实行不同的操作，其中主要的是策略为promotion_strategy_ == DataPromotionStrategy::PROMOTE || promotion_strategy_ == DataPromotionStrategy::PROMOTE_INPUTS且当前tensor类型与common type不一致时，需要进行op的tensor替换：

```cpp
if (op.defined() && to_be_promoted && common_dtype_ != op.tensor().dtype().scalar_type()) {
    op.set_origin_tensor(op.tensor());

    TensorOptions options = op.tensor().options();
    options = options.dtype(scalar_type_to_type_meta(common_dtype_.value()));

    // MemoryFormat::Contiguous will not affect origin tensor's memory_format;
    //lms 提升之后的tensor
    Tensor promoted = is_output ? TORCH::empty_like(op.tensor(), options, MemoryFormat::Contiguous)
            : op.tensor().to(options,  /*non_blocking*/ false, /*copy*/false, TORCH::nullopt);
    // Promoting
    op.set_tensor(promoted);
}
```
> Note: 这里都没有涉及shape的改变，因为对于inputs_，我们是不会实际改变shape。

#### 待粘贴