# sklearn 使用总结

`scikit-learn` —— Python 最常用的机器学习库。本项目共用到 **11 个子模块、29 个 API**，全部列举如下（按工作流顺序分组，示例代码摘自项目原文）。

## 子模块总览

| 子模块 | 本项目用到的 API | 类别 |
| :--- | :--- | :--- |
| `sklearn.datasets` | make_blobs、make_classification | 数据生成 |
| `sklearn.model_selection` | train_test_split、GridSearchCV | 划分 / 调参 |
| `sklearn.preprocessing` | PolynomialFeatures、StandardScaler、MinMaxScaler、OneHotEncoder | 特征工程 |
| `sklearn.compose` | ColumnTransformer | 特征工程 |
| `sklearn.feature_selection` | VarianceThreshold | 特征工程 |
| `sklearn.decomposition` | PCA | 特征工程 |
| `sklearn.utils.extmath` | randomized_svd | 特征工程 |
| `sklearn.linear_model` | LinearRegression、Lasso、Ridge、LogisticRegression、SGDRegressor | 模型 |
| `sklearn.neighbors` | KNeighborsClassifier、KNeighborsRegressor | 模型 |
| `sklearn.cluster` | KMeans | 模型 |
| `sklearn.pipeline` | make_pipeline | 组合 |
| `sklearn.metrics` | mean_squared_error、confusion_matrix、accuracy_score、precision_score、recall_score、f1_score、classification_report、roc_curve、roc_auc_score、silhouette_score、calinski_harabasz_score | 评估 |
| joblib（非 sklearn） | dump、load | 模型持久化 |

## 数据准备

### make_blobs —— 生成带簇结构的模拟数据

```python
from sklearn.datasets import make_blobs

# 1. 生成数据
X, y = make_blobs(n_samples=300, centers=3, cluster_std=2, random_state=42)
```

关键参数：`n_samples` 样本数、`centers` 簇数、`cluster_std` 簇标准差、`random_state`。
出处：`ml-base/unsupervised/01_kmeans.ipynb`

### make_classification —— 生成随机分类数据集

```python
from sklearn.datasets import make_classification    # 生成随机分类数据集

X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
```

关键参数：`n_samples`、`n_features`、`n_classes`、`random_state`。
出处：`ml-base/classification/classification_evaluation.ipynb`

## 数据划分与调参

### train_test_split —— 划分训练集 / 测试集

```python
from sklearn.model_selection import train_test_split

# 返回四元组
trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=42)
```

关键参数：`test_size` 测试集占比（项目用 0.2 / 0.3）、`random_state` 随机种子（全项目统一 42）。
出处：8 个文件使用 —— `ml-base/01_fitting_test.py`、`02_regularization.py`、`knn/04`、`knn/05`、`logistic_regression/digit_recognizer.ipynb`、`logistic_regression/heart_disease.ipynb`、`classification/classification_evaluation.ipynb`、`linear_regression/advertising.ipynb`

### GridSearchCV —— 网格搜索 + 交叉验证自动调参（全项目唯一）

```python
from sklearn.model_selection import train_test_split, GridSearchCV

knn = KNeighborsClassifier()
# 定义网格搜索参数列表
param_grid = {'n_neighbors': range(1, 11), "weights": ["uniform", "distance"]}
# 10 折交叉验证，在训练集上分 10 折，每次 9 折训练，1 折验证
grid_search_cv = GridSearchCV(estimator=knn, param_grid=param_grid, cv=10)
grid_search_cv.fit(X_train, Y_train)

results = pd.DataFrame(grid_search_cv.cv_results_)
print(grid_search_cv.best_estimator_)   # 最佳模型
print(grid_search_cv.best_params_)      # {'n_neighbors': 9, 'weights': 'distance'}
print(grid_search_cv.best_score_)       # 0.9888
```

关键参数：`estimator`、`param_grid`、`cv`（折数）。属性：`cv_results_`、`best_estimator_`、`best_params_`、`best_score_`。
出处：`ml-base/knn/05_heart_disease_GridSearchCV.ipynb`

## 特征工程

### PolynomialFeatures —— 多项式特征构造

```python
from sklearn.preprocessing import PolynomialFeatures, StandardScaler  # 构建多项式特征

poly5 = PolynomialFeatures(degree=5)
trainX5 = poly5.fit_transform(trainX)
testX5 = poly5.transform(testX)          # 测试集只用 transform

# degree=2, include_bias=False 时:[[2] [3]] → [[2. 4.] [3. 9.]] 即 [x, x²]
```

关键参数：`degree` 最高次数（项目用 2/5/20 对比欠拟合/过拟合）、`include_bias` 是否含常数项。
出处：`ml-base/01_fitting_test.py`、`02_regularization.py`

### StandardScaler —— 标准化（Z-score，均值 0 方差 1）

```python
from sklearn.preprocessing import StandardScaler

std_scaler = StandardScaler()
X_std_scaled = std_scaler.fit_transform(X)   # 训练集:拟合并转换
X_test = std_scaler.transform(X_test)        # 测试集:沿用训练集统计量
```

原理：`(X - mean) / std`。属性：`scale_`（标准差）、`mean_`。
出处：7 处使用 —— `knn/03_scaler.ipynb`（并手写公式验证原理）、`01_fitting_test.py`、`02_regularization.py`、`linear_regression/03_sgd.ipynb`、`advertising.ipynb`、`knn/04`、`knn/05`、`heart_disease.ipynb`

### MinMaxScaler —— 归一化（缩放到指定区间）

```python
from sklearn.preprocessing import MinMaxScaler

mm_scaler = MinMaxScaler(feature_range=(-1, 1))    # 默认是 0, 1
X_scaled = mm_scaler.fit_transform(X)
```

关键参数：`feature_range`（默认 [0, 1]）。
出处：`ml-base/knn/03_scaler.ipynb`、`logistic_regression/digit_recognizer.ipynb`

### OneHotEncoder —— 类别特征独热编码

```python
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 类别类特征
category_feats = ["胸痛类型", "静息心电图结果", "峰值ST段的斜率", "地中海贫血"]
columnTransformer = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_feats),
        ("cat", OneHotEncoder(drop='first'), category_feats),   # drop='first' 丢第一列避免共线性
        ("bin", 'passthrough', binary_feats),
    ]
)
```

关键参数：`drop='first'`（丢弃第一列）。项目里总是嵌套在 ColumnTransformer 中使用。
出处：`ml-base/knn/04`、`knn/05`、`logistic_regression/heart_disease.ipynb`

### ColumnTransformer —— 对不同列应用不同转换器

```python
from sklearn.compose import ColumnTransformer

# 数值类特征
numerical_feats = ["年龄", "静息血压", "胆固醇", "最大心率", "运动后的ST下降", "主血管数量"]
# 二元特征
binary_feats = ["性别", "空腹血糖", "运动性心绞痛"]

columnTransformer = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_feats),
        ("cat", OneHotEncoder(drop='first'), category_feats),
        ("bin", 'passthrough', binary_feats),     # passthrough = 原样通过
    ]
)
X_train = columnTransformer.fit_transform(X_train)
X_test = columnTransformer.transform(X_test)
```

出处：`ml-base/knn/04_heart_disease_prediction.ipynb`、`knn/05`、`heart_disease.ipynb`

### VarianceThreshold —— 低方差特征过滤

```python
from sklearn.feature_selection import VarianceThreshold

# 低方差过滤
vt = VarianceThreshold(0.01)
X_filter = vt.fit_transform(X)
print(X_filter.shape)
```

关键参数：`threshold`（低于该方差的列被删除）。
出处：`ml-base/feature/01_variance_filter.ipynb`

### PCA —— 主成分分析降维

```python
from sklearn.decomposition import PCA

# 使用 PCA 进行降维，将3维数据降为2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
```

关键参数：`n_components` 保留的主成分个数。
出处：`ml-base/feature/04_pca.ipynb`、`math/SVD.ipynb`

### randomized_svd —— 随机化截断 SVD

```python
from sklearn.utils.extmath import randomized_svd

U, S, V = randomized_svd(A, n_components=1)
print(U.round(2)); print(S.round(2)); print(V.round(2))
```

关键参数：`n_components`。用于低秩近似，返回 U、S、V 三个矩阵。
出处：`math/SVD.ipynb`

## 模型

### LinearRegression —— 普通最小二乘线性回归

```python
from sklearn.linear_model import LinearRegression       # 线性回归模型

lr_model = LinearRegression()
lr_model.fit(X, y)
print(lr_model.coef_)
print(lr_model.intercept_)

# 当一元线性回归不计算截距时，可以加速训练
model = LinearRegression(fit_intercept=False)
```

关键参数：`fit_intercept` 是否计算截距。属性：`coef_`、`intercept_`。
出处：`ml-base/linear_regression/01_lr_basic.ipynb`、`01_fitting_test.py`、`advertising.ipynb`

### Lasso —— L1 正则化回归（系数稀疏化）

```python
from sklearn.linear_model import LinearRegression, Lasso, Ridge

# 2. 加 L1 正则化 (Lasso回归)
lasso = make_pipeline(StandardScaler(), Lasso(alpha=0.01))
lasso.fit(x_train, trainY)
y_pred1 = lasso.predict(x_test)

ax[1, 1].bar(np.arange(d), lasso[1].coef_.reshape(-1))   # 通过 pipeline[1] 取模型系数
```

关键参数：`alpha` 正则化强度（项目用 0.01）。
出处：`ml-base/02_regularization.py`

### Ridge —— L2 正则化回归（缩小系数但不置零）

```python
# 3. 加 L2 正则化 (Ridge回归)
ridge = make_pipeline(StandardScaler(), Ridge(alpha=1))
ridge.fit(x_train, trainY)
y_pred2 = ridge.predict(x_test)
```

关键参数：`alpha`（项目用 1）。
出处：`ml-base/02_regularization.py`

### LogisticRegression —— 逻辑回归分类器

```python
from sklearn.linear_model import LogisticRegression # 逻辑回归分类模型

model = LogisticRegression(max_iter=1000)   # 默认 100 不收敛，故调大
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 获取预测正类的概率值
y_pred_proba = model.predict_proba(X_test)[:, 1]
```

关键参数：`max_iter` 收敛迭代次数。方法：`predict`、`predict_proba`（各类别概率）、`score`（准确率）。
出处：`ml-base/logistic_regression/digit_recognizer.ipynb`、`heart_disease.ipynb`、`classification/classification_evaluation.ipynb`

### SGDRegressor —— 随机梯度下降回归

```python
from sklearn.linear_model import SGDRegressor

sgd_model = SGDRegressor(
    loss="squared_error",  # 损失函数，默认为均方误差
    fit_intercept=True,  # 是否计算截距
    learning_rate="constant",  #  学习率是否恒定（如果收敛了，是否可以慢慢变小）
    eta0=0.1,  # 初始学习率
    max_iter=10 ** 6,  # 最大迭代次数
    tol=1e-5,  # 损失值变化量小于 tol 时停止迭代
    penalty="l1",  # 正则化类型，防止复杂模型过拟合
    alpha=0.0001,  # 正则化强度
)
scaler = StandardScaler()
X = scaler.fit_transform(X)
sgd_model.fit(X, y)
```

关键参数：`loss`、`learning_rate`、`eta0`、`max_iter`、`tol`、`penalty`、`alpha`。
出处：`ml-base/linear_regression/03_sgd.ipynb`（max_iter 1/10⁶/10⁹、tol 1e-5/1e-8 对比）、`advertising.ipynb`

### KNeighborsClassifier —— K 近邻分类

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=2, weights='distance') # 如果多个点打平，给每个点配置权重
knn.fit(X, y)
x_class = knn.predict(x)

score = knn.score(X_test, Y_test)   # 计算预测准确率
```

关键参数：`n_neighbors` 邻居个数、`weights`（uniform / distance）。
出处：`ml-base/knn/01_knn_classification.ipynb`、`04_heart_disease_prediction.ipynb`、`05_heart_disease_GridSearchCV.ipynb`

### KNeighborsRegressor —— K 近邻回归

```python
from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor(n_neighbors=4, weights='distance')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
# 绘制到最近2个邻居的连线
distances, indices = knn.kneighbors([X_test[i]])
```

附加方法：`kneighbors()` 查询最近邻的索引与距离。
出处：`ml-base/knn/02_knn_regression.ipynb`

### KMeans —— K-Means 聚类

```python
from sklearn.cluster import KMeans

# 定义模型并聚类
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

# 获取聚类结果
centers = kmeans.cluster_centers_
y_pred = kmeans.predict(X)

print(kmeans.inertia_)    # WCSS 簇内平方和，越低说明高内聚，越好
```

关键参数：`n_clusters`。属性：`cluster_centers_`（簇中心）、`inertia_`（簇内平方和）。
出处：`ml-base/unsupervised/01_kmeans.ipynb`

## 组合

### make_pipeline —— 把转换器和模型串成流水线

```python
from sklearn.pipeline import make_pipeline

model = make_pipeline(StandardScaler(), LinearRegression())
model.fit(trainX, trainY)

# 按索引取步骤: pipeline[0] 是 scaler,pipeline[1] 是模型
lasso = make_pipeline(StandardScaler(), Lasso(alpha=0.01))
lasso[1].coef_          # 模型的系数

# 用 pipeline 还原标准化后的系数
scaler = pipeline[0]
w_original = pipeline[1].coef_[0] / scaler.scale_[0]
b_original = pipeline[1].intercept_[0] - w_original * scaler.mean_[0]
```

出处：`ml-base/01_fitting_test.py`、`02_regularization.py`、`linear_regression/03_sgd.ipynb`

## 评估指标

### mean_squared_error —— 均方误差 MSE（回归）

```python
from sklearn.metrics import mean_squared_error          # MSE 均方误差损失函数

test_loss0 = mean_squared_error(testY, y_pred0)
train_loss0 = mean_squared_error(trainY, y_train_pred0)
```

越小越好。出处：`ml-base/01_fitting_test.py`、`02_regularization.py`、`advertising.ipynb`

### confusion_matrix —— 混淆矩阵（分类）

```python
from sklearn.metrics import confusion_matrix

# labels 控制显示哪些 label 以及排序
matrix = confusion_matrix(y_true, y_pred, labels=labels)
pd.DataFrame(matrix, columns=labels, index=labels)   # 行=真实,列=预测
```

出处：`ml-base/classification/classification_basic.ipynb`（并用 seaborn.heatmap 可视化）

### accuracy_score —— 准确率

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true, y_pred)
```

出处：`ml-base/classification/classification_basic.ipynb`

### precision_score —— 精确率 TP/(TP+FP)

```python
from sklearn.metrics import precision_score

precision = precision_score(y_true, y_pred, pos_label='猫')   # pos_label 指定正类
```

出处：`ml-base/classification/classification_basic.ipynb`

### recall_score —— 召回率 TP/(TP+FN)

```python
from sklearn.metrics import recall_score

recall = recall_score(y_true, y_pred, pos_label='猫')
```

出处：`ml-base/classification/classification_basic.ipynb`

### f1_score —— 精确率与召回率的调和平均

```python
from sklearn.metrics import f1_score

f1 = f1_score(y_true, y_pred, pos_label='猫')
```

出处：`ml-base/classification/classification_basic.ipynb`

### classification_report —— 一键生成完整分类报告

```python
from sklearn.metrics import classification_report   # 生成分类评估报告

report = classification_report(y_true, y_pred, target_names=labels)   # 指定类别显示名
```

一次输出 precision / recall / f1-score / support。出处：`classification_basic.ipynb`、`classification_evaluation.ipynb`

### roc_auc_score / roc_curve —— ROC 曲线与 AUC

```python
from sklearn.metrics import roc_curve, roc_auc_score

# 8. 计算 AUC (Area Under the Curve) 曲线下面积
roc_auc = roc_auc_score(y_test, y_pred_proba)      # 输入为预测概率

# 9. 绘制 ROC 曲线
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
```

AUC = 0.5 为随机猜测。出处：`ml-base/classification/classification_evaluation.ipynb`

### silhouette_score —— 轮廓系数（聚类）

```python
from sklearn.metrics import calinski_harabasz_score, silhouette_score

print(silhouette_score(X, y_pred))  # 轮廓系数 越接近1越好
```

取值 [-1, 1]。出处：`ml-base/unsupervised/01_kmeans.ipynb`

### calinski_harabasz_score —— CH 指数（聚类）

```python
print(calinski_harabasz_score(X, y_pred))   # CH 指数 簇间和簇内分散度的比值，越大越好
```

出处：`ml-base/unsupervised/01_kmeans.ipynb`

## 模型持久化

```python
import joblib

# 保存模型
joblib.dump(value=knn, filename='../../model/knn_model')
joblib.dump(grid_search_cv.best_estimator_, '../../model/knn_best_estimator')

# 加载模型
knn_loaded = joblib.load('../../model/knn_model')
knn_best_est = joblib.load('../../model/knn_best_estimator')
```

（joblib 不是 sklearn，但常与 sklearn 搭配保存模型。）
出处：`ml-base/knn/04`、`knn/05`；产物为 `model/knn_model`、`model/knn_best_estimator`

## 估计器通用 API 范式

所有 sklearn 估计器 / 转换器共享同一套接口：

| 方法 | 用途 | 本项目使用处 |
| :--- | :--- | :--- |
| `fit(X, y)` | 训练 | 所有模型 |
| `predict(X)` | 预测 | 所有模型 |
| `predict_proba(X)` | 预测概率（分类器） | LogisticRegression |
| `score(X, y)` | 自带评分（准确率 / R²） | KNN、LogisticRegression |
| `fit_transform(X)` | 拟合并转换（训练集） | 所有转换器 |
| `transform(X)` | 仅转换（测试集，沿用训练集统计量） | 所有转换器 |

下划线属性（训练后产生）：`coef_`、`intercept_`（线性模型）、`cv_results_`、`best_estimator_`、`best_params_`、`best_score_`（GridSearchCV）、`cluster_centers_`、`inertia_`（KMeans）、`scale_`、`mean_`（StandardScaler）。

## 附:本项目未使用但常见的 API

`load_digits` / `load_iris` 等内置数据集、`cross_val_score`、`validation_curve`、`KFold`、`r2_score`、`mean_absolute_error`、`TruncatedSVD`、`SelectKBest` —— 本项目均未出现,留待后续学习。
