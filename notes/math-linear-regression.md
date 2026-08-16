# 线性回归的数学原理

确定一个损失函数，用
* 正规方程法
* 梯度下降法

找到能让损失函数最小的 $\mathbf{\beta}$

### 确定损失函数

当因变量 y 与 自变量 x 存在线性关系，

且误差具有独立同分布（正态分布）时。

$$p(\epsilon_i) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{\epsilon_i^2}{2\sigma^2}\right)$$

代入 $y_i - x_i = \epsilon_i$，从 $x_i$ 得 $y_i$ 的概率为

$$p(y_i \mid x_i; \mathbf{\beta}) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(y_i - \mathbf{\beta}^T x_i)^2}{2\sigma^2}\right)$$

似然函数(把它们都乘起来)为

$$L(\mathbf{\beta} | X; Y) = p(Y | X; \mathbf{\beta}) = \prod_{i=1}^n p(y_i | x_i | \mathbf{\beta}) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(y_i - \mathbf{\beta}^T x_i)^2}{2\sigma^2}\right)$$

对数似然函数为

$$\ln L(\mathbf{\beta}) = -\frac{n}{2} \ln(2\pi\sigma^2) - \frac{1}{2\sigma^2} \sum_{i=1}^n (y_i - \mathbf{\beta}^T x_i)^2$$

$$
\begin{align}
让 \mathbf{\beta} 最合理: \\
&= 让 p(y_i \mid x_i; \mathbf{\beta}) 最大 \\
&= 让似然函数最大 \\
&= 让对数似然最大 \\
&= \sum_{i=1}^n (y_i - \mathbf{\beta}^T x_i)^2 最小 \\
&= \mathrm{MSE} 最小
\end{align}
$$
那损失函数就是 MSE

## 正规方程法

损失函数表达：

$$
\mathrm{MSE} = \frac{1}{n} \sum_{i=1}^n (\boldsymbol{\beta}^T \mathbf{x}_i - y_i)^2 = \frac{1}{n} (\mathbf{X}\boldsymbol{\beta} - \mathbf{y})^T (\mathbf{X}\boldsymbol{\beta} - \mathbf{y})
$$

损失函数求偏导：

$$
\frac{\partial MSE}{\partial \beta} 
= \frac{\partial ( \frac{1}{n} (X\beta - y)^T (X\beta - y) )}{\partial \beta} \\
= \frac{2}{n} X^T (X\beta - y)
$$

求极值，令偏导 = 0

$$
\frac{2}{n} X^T X \beta - \frac{2}{n} X^T y = 0
$$

$$
X^T X \beta = X^T y
$$

$$
\beta = (X^T X)^{-1} X^T y
$$

因为矩阵的逆计算量很大 $O(n^3)$，所以当特征维度和数量上来以后性能会很低

总复杂度: $O(nm^2 + m^3)$ , $m$ 为特征数， $n$ 为数据量

## 梯度下降法

同样，损失函数为

$$
J(\beta) = \frac{1}{n} \|X\beta - y\|_2^2 = \frac{1}{n} (\mathbf{X}\boldsymbol{\beta} - \mathbf{y})^T (\mathbf{X}\boldsymbol{\beta} - \mathbf{y})
$$

梯度为各个 $\beta_i$ 偏导组成的向量，记

$$
\nabla J(\beta) = \begin{bmatrix}
\dfrac{\partial J}{\partial \beta_1} \\[6pt]
\dfrac{\partial J}{\partial \beta_2} \\[6pt]
\vdots \\[6pt]
\dfrac{\partial J}{\partial \beta_p}
\end{bmatrix} = \frac{2}{n} X^T (X\beta - y)
$$

梯度下降的算法逻辑为：

```python
while 
(np.abs(grad := g(X, y, beta)) > 1e-6).any() and 
(iter := iter - 1) >= 0:

    beta = beta - alpha * grad
```

需要设置好的超参数

```
初始 beta = [1, 1, ...]
初始 alpha = 0.01
最大迭代次数
梯度阈值
然后开始迭代
```