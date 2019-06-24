---
layout: math
title: 高斯滤波--卡尔曼滤波
mathjax: true
date: 2019-05-26 15:31:53
categories: [读书笔记]
tags: [概率机器人, slam]
---

卡尔曼滤波对具有线性动态测量函数的有限阶问题利用矩参数来实现贝叶斯滤波,属于高斯滤波一种.
<!--more-->

高斯滤波的基本思想是置信度(belief)用多元正态分布表示.$x$的密度用两个参数均值$\mu$和方差$\Sigma$来表示.均值是n维向量,协方差是对称半正定二次型.高斯滤波的参数均值和方差称为矩参数(moments parameterization),这二者分别是概率分布的一阶矩和二阶矩,正态分布的其他矩都为零.

卡尔曼滤波(Kalman Filter, KF)实现了对**连续状态**的置信度计算,不适用于离散或混合状态空间.

## 线性高斯系统

在除了贝叶斯滤波的马尔科夫假设之外,若连续变量满足以下三个特性,可以认为其后验是满足高斯(Gaussian)分布的:

* 状态转移概率$p({\boldsymbol x}_t|{\boldsymbol u}_t,x_{t-1})$必须是携带随机高斯噪声的参数的线性函数,即:
$${\boldsymbol x}_t=A_t{\boldsymbol x}_{t-1}+B_t{\boldsymbol u}_t+\varepsilon_t$$
式中$\varepsilon_t$是一个高斯随机变量,表示由状态转移引入的不确定性,其维数与状态向量$x$的维数相同.其均值为0,方差用$R_t$表示.上式表明状态变量与带有附加高斯噪声的状态转移成线性关系.后验表达式为:
$$p(x_t|u,x_{t-1})={\rm det}{(2\pi R_t)}^{-\frac{1}{2}}{\rm exp}\{-\frac{1}{2}(x_t-A_tx_{t-1}-B_tu_t)^TR_t^{-1}(x_t-A_tx_{t-1}-B_tu_t)\}$$
式中均值为$A_tx_{t-1}+B_tu_t$,方差由$R_t$给定.

* 测量概率$p(z_t|x_t)$也与带有高斯噪声的自变量成线性关系:
$$z_t=C_tx_t+\delta_t$$
$\delta_t$是均值为0,方差为$Q_t$的多变量高斯分布.$P(z_t|x_t)$由下式给出:
$$p(z_t|x_t)=det(2\pi Q_t)^{-\frac{1}{2}}exp\{-\frac{1}{2}(z_t-C_tx_t)^TQ_t^{-1}(z-C_tx_t\}$$

* 初始置信度${\rm bel}(x_0)$必须是正态分布的.$\mu_0$表示置信度的均值,$\Sigma_0$表示方差:
$${\rm bel}(x_0)=p(x_0)={\rm det}(x_0)={\rm det}(2\pi \Sigma_0)^{-\frac{1}{2}}{\rm exp}\{-\frac{1}{2}(x_0-\mu_0)^T\Sigma_0^{-1}(x_0-\mu_0)\}$$

上面的三个假设保证了后验${\rm bel}(x_t)$在任何时刻t总符合高斯分布.

## 卡尔曼滤波算法

KF的输入就是$t-1$时刻的置信度,输出的是$t$时刻的置信度.卡尔曼滤波算法主要由预测和更新(innovation)构成,具体步骤如下:

1. 接收输入$\mu_{t-1}$,$\Sigma_{t-1}$,$z_t$,分别为上一时刻的状态均值和方差以及当前的观测值.

2. $\bar \mu_t=A_t\mu_{t-1}+B_t\mu_t$
	$\bar \Sigma_t=A_t\Sigma_{t-1}A^T_t+R_t$

3. $K_t=\bar \Sigma_{t-1}C_t^T(C_t\bar \Sigma_t^T+Q_t)^{-1}$

4. $\mu_t=\bar \mu_t+K_t(z_t-C_t\bar \mu_t)$
	$\Sigma_t=(I-K_tC_t)\bar \Sigma_t$

5. *return* $\mu_t,\Sigma_t$

在算法中,$K_t$是卡尔曼增益(Kalman gain).对于算法的复杂度,由于第3步矩阵求逆时间复杂度至少为$O(d^{2.4})$,$d$为矩阵维度$d\times d$;在SLAM中,测量空间$z$的维度往往小于状态空间$x$维度,第4步更新的矩阵乘法时间复杂度至少为$O(n^2)$.