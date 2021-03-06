---
layout: post
title: Makefile初探-1
date: 2018-04-01 16:12:13
categories: [笔记]
tags: [makefile]
---

makefile的基本概念
<!--more-->

makefile是在编译中大型程序中使用的自动化编译工具 `make` 依赖的指令文件。这样可以使得程序的编译更加便捷快速。
makefile的一般规则如下：
```makefile
target ... : prerequisites ...
command
```
`target`即是一个目标文件，它可以是可执行程序、目标中间文件、标记（label）等。这个目标要想编译出来需要的前提条件就是`prerequisites`这些已存在的文件。编译过程中的规则则是由`command`里面的各个命令组成。`command`以一个`Tab`起头。`make`会比较目标文件与条件中的文件更新时间，一旦有文件被修改，`make`就会依赖于这些前提文件进行重新编译。`makefile`中第一个`target`会被认为是`make`的默认目标。
当`prerequisites`是空的时候，前面的目标文件被当成一个命令，使用`make`执行时会直接执行`command`里的命令。
```makefile
clean :
	rm edit main.o kbd.o command.o display.o \
	insert.o search.o files.o utils.o
```
执行这个`make clean`会将当前文件夹下的几个中间文件删除掉。
`makefile`中可以使用变量，类似于C语言中的宏：
```makefile
edit : main.o kda.o command.o
	gcc -o edit main.o kda.o command.o
```
这里面如果要向`edit`的依赖项中添加文件，那么也得向`command`中加入同样的文件，`makefile`一大，就很难批量处理，这时候可以声明变量：
```
objects = main.o kda.o command.o
```
那么上面的makefile可以改成：
```makefile
objects = main.o kda.o command.o

edit : $(objects)
	gcc -o edit $(objects)
```
通过美元符号`$(变量名)`的方式来引用变量。
`make`工具会`.o`文件对应的`.c`文件自动的添加到依赖关系中。如果找到一个`foo.o`，那么对应的`foo.c`就会自动的加入到依赖关系并且会在`command`中自动隐式添加一行`gcc -o `。那么`foo,o`的生成就可以简写为：
```makefile
foo.o : other_files_list
```
其中的`command`直接就不用写了。
`.PHONY`用来修饰`target`，表示它是一个“伪目标”。
总结：
* 显式规则
* 隐式规则
* 变量定义
* 引用文件
* 注释
makefile中只有行注释，注释以`#`开头。

