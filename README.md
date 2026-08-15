# 数据分析

- [NumPy 笔记](notes/numpy.md)
- [Pandas 笔记](notes/pandas.md)
- [Matplotlib 笔记](notes/matplotlib.md)
- [Seaborn 笔记](notes/seaborn.md)

# 机器学习基础

* 机器学习方法汇总

![img](./notes/images/机器学习方法汇总.png)

* 有监督训练核心流程：

![img](./notes/images/监督学习一般流程.png)

## 核心 API

| 子模块 | API | 作用简述 |
| :--- | :--- | :--- |
| `sklearn.datasets` | `make_blobs` | 生成各向同性的高斯团状数据（聚类常用） |
| | `make_classification` | 生成自定义的分类数据集（可控制特征数、类别数等） |
| `sklearn.model_selection` | `train_test_split` | 将数据集随机划分为训练集和测试集 |
| | `GridSearchCV` | 对指定参数网格进行穷举搜索，结合交叉验证选出最佳参数 |
| `sklearn.preprocessing` | `PolynomialFeatures` | 生成特征的多项式组合，用于多项式回归 |
| | `StandardScaler` | 标准化（去均值 + 单位方差），使特征服从标准正态分布 |
| | `MinMaxScaler` | 最小-最大缩放，将特征缩放到指定区间（默认 [0,1]） |
| | `OneHotEncoder` | 将分类特征编码为独热向量（稀疏矩阵） |
| `sklearn.compose` | `ColumnTransformer` | 对不同列应用不同的预处理器，组合成统一转换器 |
| `sklearn.feature_selection` | `VarianceThreshold` | 移除方差低于阈值的特征（低方差特征过滤） |
| `sklearn.decomposition` | `PCA` | 主成分分析，线性降维方法 |
| `sklearn.utils.extmath` | `randomized_svd` | 随机化 SVD 分解，用于大规模矩阵的近似奇异值分解 |
| `sklearn.linear_model` | `LinearRegression` | 普通最小二乘线性回归 |
| | `Lasso` | L1 正则化线性回归，可用于特征选择 |
| | `Ridge` | L2 正则化线性回归（岭回归） |
| | `LogisticRegression` | 逻辑回归分类器（支持多分类） |
| | `SGDRegressor` | 随机梯度下降回归器，支持多种损失函数，适合大规模数据 |
| `sklearn.neighbors` | `KNeighborsClassifier` | K 近邻分类器（基于距离投票） |
| | `KNeighborsRegressor` | K 近邻回归器（基于距离加权平均） |
| `sklearn.cluster` | `KMeans` | K-Means 聚类算法 |
| `sklearn.pipeline` | `make_pipeline` | 快速创建 Pipeline 的便捷函数，按顺序串联多个转换器 + 最终估计器 |
| `sklearn.metrics` | `mean_squared_error` | 计算均方误差（MSE），回归常用 |
| | `confusion_matrix` | 计算混淆矩阵，评估分类结果 |
| | `accuracy_score` | 计算准确率（预测正确的比例） |
| | `precision_score` | 计算精确率（TP / (TP + FP)） |
| | `recall_score` | 计算召回率（TP / (TP + FN)） |
| | `f1_score` | 计算 F1 分数（精确率和召回率的调和均值） |
| | `classification_report` | 输出包含精确率、召回率、F1 分数等指标的分类报告 |
| | `roc_curve` | 计算 ROC 曲线的 FPR 和 TPR |
| | `roc_auc_score` | 计算 ROC 曲线下的面积（AUC 值） |
| | `silhouette_score` | 计算轮廓系数，评估聚类效果（越大越好，范围 [-1,1]） |
| | `calinski_harabasz_score` | 计算 Calinski-Harabasz 指数（方差比），评估聚类效果（越大越好） |
| joblib（非 sklearn） | `dump` | 将 Python 对象序列化保存到磁盘（模型持久化） |
| | `load` | 从磁盘加载由 `dump` 保存的 Python 对象 |

- [API 总结](./notes/sklearn.md)

## 公式总结

- [公式总结](notes/formula.md)

## 特征工程

- [特征工程](notes/feature-engineering.md)

```
低方差过滤 ｜ 相关系数法 ｜ 独热编码 ｜ 标准化 ｜ PCA | 列转换器
```