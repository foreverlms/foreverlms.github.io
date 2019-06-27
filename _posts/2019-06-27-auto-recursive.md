---
layout: post
title: C++通过迭代修改字符串本身（auto类型说明符）
date: 2018-04-21 15:18:17 +0800
categories: [笔记]
tags: [cpp, C++ Primer]
---

以字符串这种支持
```cpp
for (declaration : expression)
	statement
```
这样`for`语句迭代的数据结构为例，我们看看`auto`关键字在类型推断中的作用。
```cpp
string s = "I LOVE YOU!";

for (char ch : s){
   	cout << ch << endl;
}
```
输出：
```
I LOVE YOU!
```
这种情况下用不用`auto`都无所谓，因为这时候`auto`并不能减少代码量，但是一到复杂的循环时就可以体现出来了，因此最好还是用`auto`。
像上面那样对string进行遍历并不能改变其本身，`ch`是`s`中每个字符的副本拷贝。想要改变`s`本身，则要限定参与遍历的是引用：
```cpp
for (auto &ch : s) {
    ch = tolower(ch);
    cout << ch << endl;
}
```
输出：
```
i love you!
```
这样`ch`是`s`中每个字符的引用，对`ch`进行修改也就可以修改`s`本身了。
`for-each`这样的语法应用于多维数组时，需要注意的是外层循环要使用引用：
```cpp
int array[3][3] = { {1,2,3},{4,5,6},{7,8,9} };

for (auto &row : array){
    for (auto col : row)
        cout << col << " ";
    cout << endl;
}
```
如果`row`不是引用，那么它会被自动转化为对这个二维数组每一行的指针，成为了指针，内层循环对指针进行遍历就当然不合法了。
下面就`auto`比较特殊的一点来举个栗子：
```cpp
int foo = 11;
const int &a = 10;
int *p = &foo;

auto x = foo;//x是int
auto y = a;//y是int，int类型的变量y当然可以用引用a来初始化，这里a的顶层const属性被移除。
auto &yy = a;//yy是const int &，所以可以用a来对yy进行初始化。
auto pp = p;//这个与下面一样，我暂时还不能搞懂
auto *ppp = p;//ppp是int *，可以用p赋值初始化

cout << y << endl;
cout << yy << endl;
cout << pp << endl;
cout << ppp << endl;
```
结果：
```cpp
10
10
0x61fefc
0x61fefc
```
发现没有，`pp`与`ppp`是一样的，这里涉及到`auto`的一些原理，我不是太清楚。而且`auto`定义的是引用时，初始化值顶层的`const`属性并不会移除，`yy`是个例子；`auto`定义的不是引用时，初始化值顶层的`const`属性会被移除，`y`就是个例子。