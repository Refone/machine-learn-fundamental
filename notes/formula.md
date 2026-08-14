# 公式总结

## 皮尔逊相关系数

$$
r = \frac{
  \sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})
}{
  \sqrt{\sum_{i=1}^n (x_i - \bar{x})^2}
  \sqrt{\sum_{i=1}^n (y_i - \bar{y})^2}
}
$$

* Pearson Correlation

* 正相关接近 1，负相关接近 -1，无关接近 0。

* API：`X.corrwith(y, method="pearson")`

## 斯皮尔曼相关系数

$$r_s = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$

* Spearman's Rank Correlation Coefficient
* $d_i$ 是两个变量 rank 差
* $n$ 是样本数
* 适用于非线性关系，或不符合正态分布的情况