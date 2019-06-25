---
layout: post
title: "C++中的基本概念之复合类型"
date: 2019-04-08 16:14:45
categories: [笔记]
tags: [cpp,C++ Primer]
---

C++中的复合类型
<!--more-->

复合类型是指基于其他类型定义的类型，其中有这几种：
* 数组
* 字符串
* struct 结构
* enum 枚举
* union 共用体
* 指针
* 引用

这里看看其中的引用和指针。

## 引用
引用为对象齐了另外一个名字，引用类型引用另外一种类型。通过将声明符写成`&d`的形式来定义引用类型，其中`d`是声明的变量名。引用不是对象。

```cpp
#include <iostream>
using namespace std;
int main() {

    char ch(65);
    char * p = &ch;//指针

    char &r = ch;//引用
    cout << ch << "\n";//输出A
    *p = ch+1;//ch++;
    cout << ch << "\n";//输出B
    r = ch+2;//ch+=2;
    cout << ch << "\n";//输出D
    return 0;

}
```

引用的赋值时绑定变量，初始化之后引用就会和其初始绑定对象一直绑定。对引用进行操作其实就是对其绑定对象进行操作。
**引用无法解绑，初始化之后不可改变。**引用一般只能绑定到对象上，不能与`字面值`或者某个`表达式的计算结果`绑定在一起。
```cpp
int &refer = 0;//错误，引用类型初始值不能为字面常量
double d = 3.14;
int &refer1 = d;//错误，`int`类型的引用不可绑定到`double`类型上
```

## 指针
指针也是对其他对象的间接访问，类似于C里面的指针。指针与引用不同，其本身是对象，允许对指针进行赋值、拷贝；指针无需在定义时进行赋值。未被初始化的指针是一个不确定的指针。

C++中指针定义方式与C中一致。
引用不是对象，因此无法创建指向引用的指针。
指针的值应该是对象的地址，值有下列四种状态：
1. 指向一个对象
2. 指向紧邻对象所占空间的下一个位置
3. 空指针
空指针不指向任何对象。创建一个空指针可以如下几种方式：
```cpp
int *p = nullptr;
int *pp = 0;
int *ppp = NULL;
```
4. 无效指针

后三种情况一般都会造成不可估计的后果。


## const 与指针
之前C部分的笔记中提到了`const`与指针的组合，C++中基本一致。下面看一种情况：
```cpp
char ch = 'A';
typedef char *pstring;
const pstring cstr = &ch;

*cstr = 'G';
```
这种情况下`*cstr = 'G'`这个赋值合法吗？有的同学就会认为`const pstring cstr = &ch;`的意思就是`const char *cstr = &ch;`，因此`cstr`是一个指向常量的指针，通过这个指针对对象进行修改是不合法的。但是，我们知道`typedef`与宏定义是不一样的，它不是简单的文本替换。这里`pstring`其实已经是一种数据类型了，他的类型就是**`char *`，即字符指针。**所以这时候用`const`修饰`cstr`这个变量，就和`const int foo = 0;`一样，只不过这里`int`换成了`pstring`，`const`所规定的常量是个指针，所以最终`cstr`是一个**常量指针**，而不是一个**指向常量的指针**，因此是可以通过`cstr`对`ch`的值进行修改的。反之，`const char *cstr = &ch;`这种写法就含义不一样了。这里`const`修饰的基本数据类型是什么呢？是`char`，这里`*`变成了指针的声明符，所以这样写意义就是`cstr`是一个指向常量字符的指针。
另外，C++中引入了`using`这个关键字来达到`typdef`的效果。上面`typedef char *pstring`可以改写成`using pstring = char *;`。

## 类型说明符auto
C++中`auto`与C中的`auto`关键字好像很不一样啊。C++中`auto`是让编译器分析表达式来确定变量的类型。`auto`定义的变量必须进行初始化。
```cpp
int a = 10;
int b = 10;
auto c = a+b;//这里没有直接声明c的类型，而是通过a,b相加推断出来c是int。c=20
```
`auto`的使用很灵活：
```cpp
int a = 10;
int b = 10;
auto c = a+b;
auto *p = &c;//p被自动推断出为int *。
int &r = a;
auto rr = r;//rr被自动推断为int，因为r只是a的引用，a的类型才是rr的类型
const auto d = a;//auto推断出int，那么d的类型就成了`const int`。
```
可以在一个`auto`语句中同时推断多个变量的类型，但前提条件是这些变量的类型不会冲突，即都是一个类型的。
```cpp
auto a = 10; b = 100;//正确，a,b都是int
auto a = 10; b =0.01;//错误，a,b不是同一个类型
```

## 类型说明符decltype()
`auto`是用变量的初始化值的类型推断变量本身的类型，而`decltype()`则是推断出表达式的类型，但是仅仅返回类型而不使用值：
```cpp
decltype(f()) foo = x;//推断出f函数返回值类型，声明foo为该类型，并用x的值进行初始化。
int a = 10
decltype(p) pp = &a;//p是int *，pp也是
int &g = a;
decltype(g) r = a;//g是一个引用，因此r是int &类型。
decltype(a) e;//a是int，那么e也是int，可以不进行初始化
// decltype((a)) h;//这种双括号写法会导致h的类型被认为是引用，不进行初始化不合法
decltype((a)) h =a;
```