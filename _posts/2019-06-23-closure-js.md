---
layout: post
title: "通过闭包(Closure)实现\"加减乘除\""
date: 2019-04-08 11:24:17
toc: true
categories: [code]
tags: [javascript]
---

通过闭包实现函数执行次数上的加减乘除
<!--more-->


## 闭包(Closure)

今天在网上随便逛的时候看到了python里的闭包概念，搜了一下，结果不小心尽到了javascript里的闭包...我看了一下，二者理念是一致的，都是涉及到两点：
* 函数变量作用域
* 函数的返回值是一个函数

具体的概念不做赘述，两篇关于闭包的文章很值得一看，分别是[python](https://www.programiz.com/python-programming/closure)和[javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)，大意上就是返回的函数可以持有外层函数局部变量的引用。

## 闭包与加减乘除
我对js不熟悉，甚至都没有用过，但是看到了有关闭包的一个问题，很有意思：**如何通过闭包实现某种意义上的加减乘除**？这个问题很有意思，它给了0和1的定义：

```javascript
var zero = function (f) {
	return function (x){
		return x;
	}
}

var one = function (f){
	return function (x) {
		return f(x);
	}
}
```
### 加法
从上面可以看出`zero`和`one`可以看出，`one`接收一个函数`f`作为参数，返回一个函数，该函数会执行f一次；`zero`同样，但是不会执行f。这确实是某中意义上的0与1。接着问我们：如何通过类似于`add(m,n)`的形式实现加法？意思就是，如果我们像`var two = add(one,one)`这样调用的话，`add`返回的`two`如果调用会执行`f`两次，相当于`one`+`one`。那么真的是这样吗？怎么实现呢？

其实很好理解，只要在`add(m,n)`里面保证`m`与`n`都可以接收到`f`，然后分别调用其返回的函数不就可以了吗？相当于先执行了`m`次`f`，再执行`n`次`f`。来看看怎么实现：

```javascript
function add(n,m) {
	return function (f) {
		return function (x){
			return m(f)(n(f)(x));//先执行n次，再执行m次
		}
	}
}
```

那么我们来测试一下：

```javascript
var two = add(one,one);
//执行2=1+1两次，也就是加法
(two(function (){
	console.log('print 2 times');
}))();
```
确实打印出了两次`print 2 times`。

### 减法

减法可以利用栈来实现。我们定义一个数组，先执行`m`次的push，再执行`n`次的pop，那么剩下的就是他们的差应该执行的次数。

```javascript
function sub(m,n){
	return function (f){
		return function(x){
			var stack = new Array();

			var push_func = function(){
				stack.push(function (){
					f(x);
				})
			}

			var pop_func = function(){
				stack.pop();
			}

			m(push_func)();
			n(pop_func)();

			for (var i=0;i<stack.length;i++){
				stack[i]();
			}
		}
	}
}
````
### 乘法

乘法可以理解为递归。即执行m次n就行了。

```javascript
function multiply(n,m){
	return function(f){
		return function(x){
			//y是一个函数，他会执行n(f)(z)
			var y = function (z){
				return n(f)(z);
			}

			//这里y其实相当于f,接收参数x,x转为形参z
			return m(y)(x);
		}
	}
}
```

### 除法

除法也需要用到栈。但是这时候相对于减法来说需要三个栈，原理就是除法可以看成每次弹出`n`，没弹出一次，那么就说明`m`减去了一个`n`。当弹出到`m`数目比`n`还小时，也就剩下了余数，结束。弹出次数就是商。具体请看代码实现：


```javascript
function div(m,n){
	return function(f){
		return function(x){
			var stack_m = new Array();
			var stack_n = new Array();
			var stack = new Array();

			m(function(){
				stack_m.push('hi');
			})();
			n(function(){
				stack_n.push('hi');
			})();

			while(stack_m.length >= stack_n.length){
				stack_m.splice(0,stack_n.length);
				stack.push(f);
			}


			for (var i=0;i<stack.length;i++){
				stack[i](x);
			}


		}
	}

}
```

### 测试及完全代码

完全代码：

```javascript
var zero = function (f) {
	return function (x){
		return x;
	}
}

(zero(function (){
	console.log('print 0 times');//不会执行
}))();

var one = function (f){
	return function (x) {
		return f(x);
	}
}

//执行一次
(one(function (){
	console.log('print 1 times');
}))();

//加法
function add(n,m) {
	return function (f) {
		return function (x){
			return m(f)(n(f)(x));
		}
	}
}

var two = add(one,one);
var three = add(one,two);

//执行2=1+1两次，也就是加法
(two(function (){
	console.log('print 2 times');
}))();

//乘法
function multiply(n,m){
	return function(f){
		return function(x){
			//y是一个函数，他会执行n(f)(z)
			var y = function (z){
				return n(f)(z);
			}

			//这里y其实相当于f,接收参数x,x转为形参z
			return m(y)(x);
		}
	}
}

//减法
function sub(m,n){
	return function (f){
		return function(x){
			var stack = new Array();

			var push_func = function(){
				stack.push(function (){
					f(x);
				})
			}

			var pop_func = function(){
				stack.pop();
			}

			m(push_func)();
			n(pop_func)();

			for (var i=0;i<stack.length;i++){
				stack[i]();
			}
		}
	}
}

//除法
function div(m,n){
	return function(f){
		return function(x){
			var stack_m = new Array();
			var stack_n = new Array();
			var stack = new Array();

			m(function(){
				stack_m.push('hi');
			})();
			n(function(){
				stack_n.push('hi');
			})();

			while(stack_m.length >= stack_n.length){
				stack_m.splice(0,stack_n.length);
				stack.push(f);
			}


			for (var i=0;i<stack.length;i++){
				stack[i](x);
			}


		}
	}

}

//执行6=2*3次
var six = multiply(two,three);

(six(function (){
	console.log('print 6 times');
}))();

//执行4=6-2次
var four = sub(six,two);

(four(function (){
	console.log('print 4 times');
}))();

var ten = add(six,four);
var five = div(ten,two);

(five(function (){
	console.log('print 5 times');
}))();
```

测试结果：
```
print 1 times
print 2 times
print 2 times
print 6 times
print 6 times
print 6 times
print 6 times
print 6 times
print 6 times
print 4 times
print 4 times
print 4 times
print 4 times
print 5 times
print 5 times
print 5 times
print 5 times
print 5 times
```