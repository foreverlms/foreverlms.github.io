---
layout: post
title: C Primer Plus--位操作
date: 2019-04-08 15:51:42
categories: [笔记]
tags: [c, C Primer Plus]
---

C中位字段(bit field)
<!--more-->

## 位字段 bit field
>位字段是一个`signed int`或者`unsigned int`中一组相邻的位。位字段由一个结构声明建立，该结构声明为每个字段提供标签，并决定字段的宽度。

```c
struct p {
    unsigned int autfd : 1;//autfd字段占一个int其中的1位宽度
    unsigned int bldfc : 1;
    unsigned int undln : 1;
    unsigned int itals : 1;
    //字节剩下的位空出
} ;
struct p pt;
pt.autfd = 0;
pt.bldfc = 1;
//...
```
这里生命了一个`p`，其包含四个一位字段。`p`被存储在一个usigned int大小的存储单元中，但仅使用了其中的4位。
字段的位数可以是多位。
```c
 struct pp {
        unsigned int code1 : 2;
        unsigned int code2 : 2;
        unsigned int code3 : 4;
        unsigned int code4 : 1;
    } ;//pp中声明了两个2位字段，一个4位字段，一个1位字段
```
`pp`会占两个`unsigned int`存储单元，但是只会按顺序使用其中的9位。
如果声明的位字段总位数超过一个`unsigned int`空间，像上面那样，相邻的下一个`unsigned int`存储空间会被利用。但是不允许一个位字段的位数跨越两个`unsigned int`的边界。当出现一个位字段位数跨越了边界时，编译器会自动移除掉这个位字段，空出来，就像一个洞一样，使得边界对齐。
可以使用未命名的字段填充这样的洞。当指定**未命名位字段**宽度为0时，会使得下一个位字段变量移动到下一个`unsigned int`边界开始计算位数。
```c
struct ppp {
        unsigned int field1 : 2;
        unsigned int        : 2;//空出两位
        unsigned int field2 : 3;//然后才算field2占3位
        unsigned int        : 0;//field3必须从下一个unsigned int开始算位数
        unsigned int field3 : 2;
    };
```
位字段由于在不同机器上可能会有不同的存储顺序，对于字段边界位置也有区别，因此难以移植。
这样的结构赋值可以像普通struct那样进行赋值：
```c
struct {
        unsigned int field1 : 2;
        unsigned int        : 2;//空出两位
        unsigned int field2 : 3;//然后才算field2占3位
        unsigned int        : 0;//field3必须从下一个unsigned int开始算位数
        unsigned int field3 : 2;
    } ppp = {
            1,1,3
    };//需要注意1,1,3按顺序值不能超出位字段位数限制
```
这一章我没有仔细看。