# 超参数总结

**超参数** —— 训练前人为设定、不随训练更新的参数；区别于模型参数（如线性回归的 w、b 由训练学习得到）。

全项目共 23 个代码文件（`ml-base/` 21 个 + `math/` 2 个），超参数集中在 `ml-base/`。全项目**唯一的自动调参**是 KNN 心脏病预测中的 GridSearchCV，其余均为手动设置或同文件内参数对比；所有随机种子统一为 `random_state=42`。

## 超参数总览

### KNN（k 近邻）

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| `n_neighbors` | 2（分类示例）、4（回归示例）、3（心脏病预测）、**9（GridSearchCV 最优）** | 邻居个数，越大越平滑、越容易欠拟合 | `ml-base/knn/01`、`02`、`04`、`05` |
| `weights` | `distance`（距离加权）/ `uniform`（等权） | 邻居投票权重 | `ml-base/knn/01`、`02`、`05` |

### 逻辑回归 LogisticRegression

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| `max_iter` | **1000**（默认 100 不收敛，故调大） | 优化算法最大迭代次数 | `ml-base/logistic_regression/digit_recognizer.ipynb` |

其余文件（`heart_disease.ipynb`、`classification_evaluation.ipynb`）使用全部默认参数。

### 多项式拟合 PolynomialFeatures

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| `degree` | 2 / 5 / **20** 三档对比 | 多项式阶数，越大越容易过拟合 | `ml-base/01_fitting_test.py` |

`degree=2` 欠拟合、`degree=5` 恰好拟合、`degree=20` 过拟合 —— 手动对比的经典演示。

### 正则化 Lasso / Ridge

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| Lasso `alpha` | **0.01** | L1 正则化强度，越大系数越稀疏 | `ml-base/02_regularization.py` |
| Ridge `alpha` | **1** | L2 正则化强度，越大越抑制大系数 | `ml-base/02_regularization.py` |

同文件内以无正则 LinearRegression 作基线，对比 degree=20 过拟合场景下 Lasso / Ridge 的抑制效果。

### SGD 回归 SGDRegressor

`ml-base/linear_regression/03_sgd.ipynb` 中 5 处实例化的公共超参数：

| 超参数 | 本项目取值 | 含义 |
| :--- | :--- | :--- |
| `loss` | `squared_error` | 损失函数（平方误差） |
| `penalty` | `l1` | 正则化类型 |
| `alpha` | 0.0001 | 正则化强度 |
| `learning_rate` | `constant` | 恒定学习率 |
| `eta0` | 0.1 | 恒定学习率的值 |
| `max_iter` | 1 / **10⁶** / **10⁹** 对比 | 最大迭代次数（只迭代 1 次看效果 → 标准 → 更严格收敛） |
| `tol` | 1e-5 / **1e-8** 对比 | 收敛容忍度，越小训练越充分 |

### 手写梯度下降（学习率手动调参）

| 超参数 | 本项目取值 | 出处 |
| :--- | :--- | :--- |
| 学习率 `alpha` | 0.01（多元线性回归）；0.1（一元函数，试过 0.2） | `ml-base/linear_regression/02_gradient_descent.ipynb`、`ml-base/03_gradient_descent_1.ipynb`、`04_gradient_descent_2.ipynb` |
| 迭代上限 | 10000 | 同上 |
| 停止阈值 | 1e-6、1e-10（梯度小于阈值即停） | 同上 |

### 无监督 KMeans

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| `n_clusters` | **3** | 聚类个数 | `ml-base/unsupervised/01_kmeans.ipynb` |

评估用了 `inertia_` / `silhouette_score` / `calinski_harabasz_score`，未做肘部法则遍历。

### 降维 PCA / SVD

| 超参数 | 本项目取值 | 出处 |
| :--- | :--- | :--- |
| PCA `n_components` | 2（3 维降到 2 维） | `ml-base/feature/04_pca.ipynb` |
| randomized_svd `n_components` | 1 | `math/SVD.ipynb` |

### 特征工程

| 超参数 | 本项目取值 | 含义 | 出处 |
| :--- | :--- | :--- | :--- |
| VarianceThreshold `threshold` | 0.01 | 方差低于该值的特征被删除 | `ml-base/feature/01_variance_filter.ipynb` |
| MinMaxScaler `feature_range` | (-1, 1)（默认 0~1） | 归一化目标区间 | `ml-base/knn/03_scaler.ipynb` |

### 固定随机种子

全项目统一 `random_state=42`，用于 `train_test_split`、`make_blobs`、`make_classification`、`np.random.seed`。

## 调参方式

### 网格搜索 GridSearchCV（全项目唯一）

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_neighbors': range(1, 11),          # 1~10 共 10 个取值
    'weights': ['uniform', 'distance'],   # 2 种权重
}                                          # 10 折交叉验证 × 10 × 2 = 200 次训练
grid_search_cv = GridSearchCV(KNeighborsClassifier(), param_grid, cv=10)
grid_search_cv.fit(x_train, y_train)

grid_search_cv.best_params_   # {'n_neighbors': 9, 'weights': 'distance'}
grid_search_cv.best_score_    # 0.9888（交叉验证准确率）
```

出处 `ml-base/knn/05_heart_disease_GridSearchCV.ipynb`，测试集得分 1.0。最佳模型保存于 `model/knn_best_estimator`（`joblib.dump(grid_search_cv.best_estimator_, ...)`）。

### 手动对比调参

同一文件内不同取值对比效果（本项目的主要形式）：

- **多项式阶数**:`degree=2/5/20` —— 欠拟合 / 恰好拟合 / 过拟合三图对比（`ml-base/01_fitting_test.py`）
- **正则化**:无正则 vs Lasso(α=0.01) vs Ridge(α=1) 对比（`ml-base/02_regularization.py`）
- **收敛条件**:SGD 的 `max_iter` 1→10⁶→10⁹、`tol` 1e-5→1e-8 对比（`ml-base/linear_regression/03_sgd.ipynb`）
- **学习率**:梯度下降试过 0.2，最终用 0.1（`ml-base/04_gradient_descent_2.ipynb` 中被注释的 `# alpha = 0.2`）

## 已保存的模型

| 模型文件 | 固化超参数 | 来源 |
| :--- | :--- | :--- |
| `model/knn_model` | `n_neighbors=3, weights=uniform` | 手动设置模型（`ml-base/knn/04`） |
| `model/knn_best_estimator` | `n_neighbors=9, weights=distance` | GridSearchCV 最优模型（`ml-base/knn/05`） |

两个 KNeighborsClassifier 的其他参数相同：`algorithm=auto, leaf_size=30, p=2, metric=minkowski`（默认值）。
