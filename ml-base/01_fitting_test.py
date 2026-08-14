import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression       # 线性回归模型
from sklearn.model_selection import train_test_split    # 划分训练姐和测试集
from sklearn.metrics import mean_squared_error          # MSE 均方误差损失函数
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler  # 构建多项式特征

"""
1. 生成数据
2. 划分训练集和测试集（验证集）
3. 定义模型（线性回归模型，把 x, x**2, x**3,... 视为不同特征,x1, x2, ...）
4. 训练模型
5. 预测结果，计算误差
"""

"""
1. 生成数据 (sinx)
"""
# -pi～pi 看差不多一个周期，reshape 做一个行转列
n = 300
X = np.linspace(-3, 3, n).reshape(-1, 1)
np.random.seed(42)
y = np.sin(X) + np.random.uniform(-0.5, 0.5, n).reshape(-1, 1)
# y = np.sin(X) + np.random.randn(*X.shape) * 0.2

print(X.shape)
print(y.shape)

# 画出三个散点图（欠拟合，正常拟合，过拟合）
fig, ax = plt.subplots(1, 3, figsize=(18, 3))
plt.rcParams['font.sans-serif'] = ['Kai']
plt.rcParams['axes.unicode_minus'] = False

ax[0].scatter(X, y, s=10, c='y', alpha=0.8)
ax[1].scatter(X, y, s=10, c='y', alpha=0.8)
ax[2].scatter(X, y, s=10, c='y', alpha=0.8)

for a in ax:
    a.grid(True, alpha=0.3, linestyle='--')

"""
2. 划分训练集、测试集
"""
# 返回四元组
trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=42)

"""
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
原始特征 X:
 [[2]
 [3]]
转换后 X_poly:
 [[2. 4.]    # 即 [x, x²]  ->  [2, 4]
 [3. 9.]]   # 即 [x, x²]  ->  [3, 9]
"""
poly5 = PolynomialFeatures(degree=5)
trainX5 = poly5.fit_transform(trainX)
testX5 = poly5.transform(testX)

polyOverfit = PolynomialFeatures(degree=20)
trainX20 = polyOverfit.fit_transform(trainX)
testX20 = polyOverfit.transform(testX)

"""
3. 定义模型（线性回归模型）
"""
model = LinearRegression()

"""
4. 训练模型
"""
model.fit(trainX, trainY)

# 打印查看模型参数
# print(model.coef_)          # coefficients 斜率
# print(model.intercept_)     # 截距

"""
5. 预测结果，计算误差
"""
# 测试误差
y_pred0 = model.predict(testX)
test_loss0 = mean_squared_error(testY, y_pred0)
# 训练误差
y_train_pred0 = model.predict(trainX)
train_loss0 = mean_squared_error(trainY, y_train_pred0)
# 画出拟合曲线，标注训练误差和测试误差
ax[0].plot(X, model.predict(X), 'r')
ax[0].text(-3, 1, f"测试误差: {test_loss0:.4f}\n训练误差: {train_loss0:.4f}")

# 二、恰好拟合（5次多项式）
model.fit(trainX5, trainY)
# 误差统计
y_pred1 = model.predict(testX5)
test_loss1 = mean_squared_error(testY, y_pred1)
y_train_pred1 = model.predict(trainX5)
train_loss1 = mean_squared_error(trainY, y_train_pred1)
ax[1].plot(X, model.predict(poly5.transform(X)), 'r')
ax[1].text(-3, 1, f"测试误差: {test_loss1:.4f}\n训练误差: {train_loss1:.4f}")

# 三、过拟合（20次多项式）
model = make_pipeline(StandardScaler(), LinearRegression())
model.fit(trainX20, trainY)
# 误差统计
y_pred2 = model.predict(testX20)
test_loss2 = mean_squared_error(testY, y_pred2)
y_train_pred2 = model.predict(trainX20)
train_loss2 = mean_squared_error(trainY, y_train_pred2)
ax[2].plot(X, model.predict(polyOverfit.transform(X)), 'r')
ax[2].text(-3, 1, f"测试误差: {test_loss2:.4f}\n训练误差: {train_loss2:.4f}")

plt.show()
