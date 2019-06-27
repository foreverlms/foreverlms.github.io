---
layout: post
title: C存储类、链接和内存管理之动态分配内存及类型限定词
date: 2018-04-08 15:32:06
categories: [笔记]
tags: [c, C Primer Plus]
---

C中的内存动态分配及类型限定词
<!--more-->

## 存储类说明符
C中存储类说明符共有5个，为`auto` `register` `static` `extern` `typeddef`，最后一个关键字`typedef`与内存存储无关。
规定：*不可以在一个声明中使用一个以上存储类说明符*。
存储类说明符用来确定变量的存储类型。
## 存储类和函数
函数的存储类有两种：
* 外部
* 静态

在一个文件中定义的函数默认是外部的，也就是说其他文件可以调用它，只有使用`static`关键字修饰的函数才是函数定义所在文件所私有的函数,通常用来解决不同文件函数之间的命名冲突。
```c
double a();//默认声明，函数a是外部的
extern int b();//此处显式声明b函数是在其他文件中定义的，可以省略。主要是为了让程序更清晰，除非函数声明使用了关键字`static`，否则默认其为`extern`的
static int c();//c函数只能在本文件中调用
```

## 动态分配内存
`malloc`与`free`函数原型存在于`stdlib.h`中。
### `malloc`函数
在C中，一些数据的内存是由系统自动分配的，也允许程序主动要求分配。
```c
int foo = 0;//系统自动分配内存空间用来存储一个int
char string[] = "I love you.";//系统自动为数组string分配正好装下字符串的内存空间
int bar[10];//要求分配10个用来存储int的内存空间
```
还可以手动分配内存。
`extern void * malloc(unsigned int num_bytes)`
函数`malloc`函数接受一个参数，该餐宿用于指定需要分配的内存字节数。`malloc`找到可用内存中一个区块，并返回该区块内存第一个字节的地址。它的`void *`返回值是一个通用指针，可以转换为其他指针类型。C中不要求强制转换，但C++中要求强制转换。如果`malloc`找不到符合要求的可用内存，它会返回空指针。例子：
```c
double *p;
p = (double *)malloc(30 * sizeof(double));
```
例子中，分配了一块内存用于存储30个`double`类型数据，并将首字节地址赋值给了指针`p`。
### `free`函数
`void free(void *p)`
对应每个`malloc`函数调用，应该有对应的`free`调用来进行内存释放。它的参数是之前`malloc`函数分配内存块第一个字节的地址。也就是说分配的内存可用时间是从`malloc`执行结束开始到`free`释放内存为止。
例子：
```c
#include <stdio.h>
#include <stdlib.h>

/*
 * test.c 编译后产生可执行文件test.exe或test.out
 */


int main() {

    double *p;
    int max;
    int number;
    int i = 0;

    puts("What's the number of \"double\" entries?");
    while (scanf("%d",&max) != 1){
//        setbuf(stdin,NULL);
        scanf("%*s");
        puts("Please input a integer:");
    }

    printf("max = %d\n",max);

    p = (double *) malloc(max * sizeof(double));
    if (p == NULL){
        puts("Memory allocation has failed. Try to Restart this program.");
        exit(EXIT_FAILURE);
    }

    puts("Enter the values(q to quit): ");
    while (i < max && scanf("%lf",&p[i]) == 1)
        ++i;
    printf("Here are the number of entries: %d\n",number = i);
    for (int j = 0; j < number; ++j) {
        printf("%7.2f ",p[j]);
        if (j % 7 == 6)
            putchar('\n');
    }
    if (i % 7 !=0)
        putchar('\n');
    printf("i = %d\n",i);
    puts("Done.");
    free(p);
    return 0;
}
```
### `calloc`函数
与`malloc`类似，不同的是`calloc`可以指定要分配单元数目以及每个单元所需要的字节数。`calloc`会默认将内存块中的各个位置0。
`calloc`分配的内存同样需要用`free`函数来释放。
### 动态分配内存的缺点
动态分配内存给了程序一定的自由，但是若是忘记释放内存，那么就会造成资源的浪费（内存泄漏）。而且相对于自动变量栈式管理，动态分配内存不是紧凑的连续分配，而是在内存中找合适的区块，会造成内存碎片，拖慢速度。
## C类型限定关键字
### `const`定义全局常量
`const`定义常量之前已经做了笔记，[看这里](https://blog.csdn.net/m0_37196787/article/details/83687141)。这里我们来看它与全局常量的关系。
`constant`定义全局常量有两种方式：
第一种方法：
```c
//file1.c
const double PI = 3.14;

//file2.c
extern const double PI;
```
第二种：
```c
//constant.h中定义常量，需要`static`关键字来修饰
static const double PI = 3.14;

//file1.c只需include 头文件即可
#include "constant.h"

//file2.c
#include "cobnstant.h"
```
第二种方法中，`file1.c`和`file2.c`文件都包含了`constant.h`头文件，那么这两个文件都会定义声明一个本文件私有的静态内部链接变量`PI`，其实是对`constant.h`中`PI`值的拷贝。为什么必须要使用`static`关键字呢？因为如果不使用的话同一个静态外部链接变量就要在两个文件中定义声明两次，而我们知道外部变量只允许定义声明一次，其余的都应该是引用声明，定义两次会造成标识符冲突，还不如直接加个`static`修饰，为每个文件分别拷贝一个`PI`值给他们用。

### `volatile`关键字
`volatile`告诉编译器某个变量除了能被程序本身修改之外，还可以被超出程序之外的其他部分改变。假定，有一个变量的值记录的是时间，那么不管程序有没有在运行，运行的如何，这个变量的值肯定是要随着时间变化而变化的，那么这个变量就应该加`volatile`修饰来提醒编译器。再来个例子：
```c
int x = 10;
int val1 = x;
int val2 = x;
```
编译器注意到`x`变量被使用了两次而没有进行别的操作，那么他可以将`x`的值临时存储在寄存器中，那么当`val2`和`val1`进行赋值操作时就会变快。但是，如果`x`的值可能被除了程序之外的部分改变，那么就应该这样：`volatile int x = 10;`来告诉编译器这个变量可能会如此，那么编译器就不会做出将`x`值存于寄存器这样的优化。一个变量既可以是`constant`，也可以是`volatile`的，因为不能被程序改变的量为常量，但可能被硬件改变，那么就是`volatile`的。这与Java中的`volatile`关键字可不一样。
### `restrict`关键字
`restrict`关键字只能用来修饰指针，表示某个数据对象的唯一访问方式就是该指针，方便编译器优化。用法：
`int * restrict foo = (int *) malloc(10 * sizeof(int))`。这里表明`foo`这个指针是数组的唯一访问方式。
```c
int array[4] = {};
int *p = array;
```
这里就不能给`p`加`restrict`限定词，因为`array`这个数组可以通过`array`和`p`两种方式进行访问。
