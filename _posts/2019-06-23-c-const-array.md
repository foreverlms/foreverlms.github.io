---
layout: post
title: const关键字与数组、指针
date: 2019-04-08 15:48:40
categories: [读书笔记]
tags: [c, C Primer Plus]
---


`const`关键字小记
<!--more-->

开始回顾C基础知识。C中使用指针是很危险的事情，一个不慎就会造成程序崩溃，因此对于传入函数的参数进行保护就是必须的了，特别是针对数组。 
## const关键字
`const`关键字用于将一个变量声明为只读，也就是常量，无法被修改。
```c
const int constant = 10;//声明constant为常量的同时对它进行初始化赋值
int const constant = 10;//也可以将const放在int后面
```
## const修饰数组
使用const来修饰数组声明了一个数组常量，是对数组里面数据的一种保护，当试图修改一个被const修饰的数组内容时，编译时会产生错误。
```c
const int days[5] = {1,2,3,4,5};//int const days[5]一样
//想要把days[0]重新赋值为6，报错
days[0] = 6;
//Cannot assign to variable 'days' with const-qualified type 'const int [5]'
```
但是我们有一点要注意，是不是`days`里面的数据一定无法修改呢？我们做个试验：
```c
    const int days[5] = {1,2,3,4,5};
    int * p = days;
    *p = 6;
    for (int i = 0; i < 5; ++i) {
        printf("%d\n",*p++);
    }
```
结果：
```
6
2
3
4
5
```
所以虽然数组days被声明为只读的，但是如果通过指针去访问数组，还是可以改变数组元素的，这也就是指针的强大与易错。
## const修饰指针
const修饰指针创建了一个指针常量，但是const的位置会导致这个指针常量有不同的含义。
```c
    int days[5] = {1,2,3,4,5};
    const int *p1;//const修饰的是int，表示p1指向的变量值不可改变,指针本身可以改变
    //p1指向的值为常量
    p1 = days;
    *p1 = 6;//报错，不允许修改指针指向的值。Read-only variable is not assignable
    p1[1] = 7;//报错，不允许修改
    days[0] = 6;//允许，days不是常量
    p1++;//合法，p1这个指针本身是可以修改的，这里让其指向days的第二个元素
    
    
    int * const p2 = days;//const修饰的是p2，表示p2这个指针本身是无法修改的，但是其指向的值是可以修改的
    //这里p2本身是常量，因此声明p2的时候就要初始化，否则后面无法对p2进行初始化
    *p2 = 10;//合法，p2指向的值可以修改
    p2 = &days[1];//不合法，报错，p2是常量，因此想要修改指针的值使其指向days[1]不合法。
    //Cannot assign to variable 'p2' with const-qualified type 'int *const'
```
上面就说明了两种const修饰的指针常量的区别。这里有以下几点需要注意：
* 将常量或非常量数据的地址赋值给指向常量的的指针是合法的。但是非常量数据的地址可以赋值给普通指针，而常量数据的地址就不可以赋值给普通指针。这样做只会提示不合法，却仍然可以这样操作，但最好不要这样做，数据既然数据已经被声明为常量，那么就不要试图去修改，因此指针不要这样赋值，以免修改了倡廉打个值，就像上面const修饰数组里面说的。
```c
    double un_locked[3] = {1.2,2.3,3.1};
    const double locked[3] = {1.0,2.0,3.0};
    const double * p3 = locked;//合法
    p3 = un_locked;//合法
    p3 = &un_locked[1];//合法
    double *p4;
    p4 = un_locked;//合法
    p4 = locked;//非法，但是程序可以运行，
```
* const用来修饰形式参量。C语言的传参特性这里不提，如果函数并不想修改本来的数据，一般会把相应的形式参量修饰为const的，告诉编译器这里要把传进来的指针地址当做常量来对待，不允许修改，当函数体内部想要做修改时，编译器会报错。需要注意的是并不要求传进来的参数是常量，而是编译器这样做保证函数执行过程中对源数据不会修改而已。
```c
void foo(const int *bar);
//foo接受一个指针，并把这个指针当做常量对待
void foo1(int *bar);
//foo1声明接受一个普通指针
int main() {
    int test1[2] = {1,2};
    const int test2[2] = {3,4};
    
    foo(test1);//合法
    foo(test2);//合法
    foo1(test1);//合法
    foo1(test2);//不合法，不提倡这样做。Passing 'const int [2]' to parameter of type 'int *' discards qualifiers
}

void foo(const int *bar){
}
void foo1(int *bar){
}
```
## 用两个const修饰指针
用两个`const`修饰符修饰指针会使得这个指针本身既不可以更改所指向的地址，也无法修改所指向的数据。
```c
    int days[3] = {1,2,3};
    const int * const p = days;
    
    p = &days[2];//不合法
    *p = 6;//不合法
```
`const`修饰函数本身我还没用过，碰到了再来补上。