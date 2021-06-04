---
layout: post
title: C++中的Trivial Type/ Standard Layout and POD Type
date: 2021-06-04 21:52:47 +0800
categories: [笔记]
tags: [C++]
---

`layout`指的是C++数据类型（class/struct/union）在内存中如何排布的。数据类型的布局与语言特性强相关，有的是预先就能在编译前就能确定；但是当使用到C++的一些特性（诸如虚函数），编译器指定该种数据类型的内存布局是运行时确定的。

对象的内存布局既受语言特性的影响，也受到编译器版本、编译优化的影响。对于部分能够与C兼容的数据类型，它在内存中的排布是连续的，其包含的数据在内存中顺序与其声明顺序保持一致，因此可以在C和C++程序间进行二进制的流转。而像包含了虚函数的数据类型（class），所有实例的内存布局共享了一张虚函数表，在内存上就是不连续的了，因此也无法传递给C函数；同样无法使用memcpy这种原生的内存拷贝命令。
C++ 11引入了一系列的类别判断模板来帮助进行类型的布局判断：
- `is_trivial<T>`
- `is_standard_layout<T>`
- `is_pod<T>`

### Trivial Type
> When a class or struct in C++ has **compiler-provided or explicitly defaulted special member functions**, then it is a trivial type. It occupies a contiguous memory area. It can have members with different access specifiers.

Trivial Type必须满足下列条件：
- 无虚函数且不继承自虚基类
- 基类不存在non-trivial的构造函数、拷贝构造函数、移动构造函数、赋值运算符、移动赋值运算符和析构函数
- 其具有的成员变量所属类型同样需要满足上面两个条件
Trivial是琐碎的意思，那么C++里trivial-type即意指编译器已经自动给这个比较琐碎的东西（像默认的构造函数）完成了，开发者并没有去人为定义。
Trivial Type具备的特性是其对象占据连续的内存空间，那么它就可以在内存上直接进行操作或者进行静态初始化。
Trivial Type的成员数据类型能够有不一样的access specifier：

```cpp
struct TrivialButNotPOD {
public:
    int a;

private:
    int b;

public:
    int c;
};
```
这个类型是Trivial的，但是具有不同类型的访问限定符，因此也是无法被C函数使用。

> 当开发者指定speicial member function（构造/析构等等）为= default时，这时候类型仍然可以保持为Trivial的，见cppdemo代码。

### Standard layout type

> When a class or struct **does not contain** certain C++ language features such as virtual functions which are not found in the C language, and all members have the **same access** control, it is a standard-layout type.

标准布局类型指的是实现中不存在C++特性的Class/Struct，特性：
- memcopy-able（是否内存连续？）
- 能够被C函数使用并通过C API来进行C++<->C的交互。
标准布局类型的必要要求：
- 无虚基类、虚函数;
- 没有引用成员;
- 成员的访问限定符必须保持一致；
- 其基类必须也是Standard Layout、非静态成员也要为Standard Layout Type；
- 非静态成员满足其一：
  - 本身（most derived class）类型不具备非静态成员并且&拥有非静态成员的基类不超过一个
  - 基类不存在非静态成员

Standard Layout类型能够拥有special member，并不影响：

> Please note that at this point, we talk about the layout in the memory and the interoperability with C. What you do not see in the definition above is that a standard-layout class could **have special members**. They do not change the memory layout. Special members only help to initialize an object. Despite that C has no special members, we can have them in C++ in a standard-layout type because it is just about the layout, nothing else.

### POD（Plain old type）

POD类型：trivial type & standard layout type

POD类型特性：

> - we can compile a POD in C++ and still use it in a C program, as it has the same memory layout in both languages (meet by standard-layout);
> - a POD supports static initialization (meet by trivial type).

POD Class/Struct的非静态成员必须是POD类型。

> POD type is deprecated in C++ 20.

### Aggregate Tyoe
> An aggregate is an array or a class with **no user-declared constructors (12.1), no private or protected non-static data members** , no base classes（C++20中允许有public base class） , and **no virtual functions** .

Aggregate Type可以通过`{}`进行初始化：

```cpp
int array4 = {0,1,2,3};
```

Aggregate Type可能是standard-layout或者trivial。

> Cite from：https://andreasfertig.blog/2021/01/cpp20-aggregate-pod-trivial-type-standard-layout-class-what-is-what/

| Type        | memcopy-able   |  C compatible memory layout  |
| --------   | -----:   | :----: |
| Trivial Type   | Yes     |   Yes   |
| Standard Layout        | Yes      |   Yes   |
| Aggregate       | Yes     |   Maybe    |

### Literal Type

> A literal type is one whose layout can be determined at **compile time**.

下述类型是Literal Type：

- void
- scalar types
- references
- Arrays of void, scalar types or references
- A class that has a trivial destructor, and one or more constexpr constructors that are not move or copy constructors. Additionally, all its non-static data members and base classes must be literal types and not volatile.

### Reference

1. [C++20: Aggregate, POD, trivial type, standard layout class, what is what](https://andreasfertig.blog/2021/01/cpp20-aggregate-pod-trivial-type-standard-layout-class-what-is-what/)

2. [What are Aggregates and PODs and how/why are they special?](https://stackoverflow.com/questions/4178175/what-are-aggregates-and-pods-and-how-why-are-they-special)

3. [Trivial, standard-layout, POD, and literal types](https://docs.microsoft.com/en-us/cpp/cpp/trivial-standard-layout-and-pod-types?view=msvc-160)