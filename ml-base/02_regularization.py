import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

plt.rcParams['font.sans-serif'] = ['Kai']
plt.rcParams['axes.unicode_minus'] = False

n = 300
X = np.linspace(-3, 3, n).reshape(-1, 1)
Y = np.sin(X) + np.random.uniform(low=-0.5, high=0.5, size=n).reshape(-1, 1)

fig, ax = plt.subplots(2, 3, figsize=(18, 8))
for a in ax[0]:
    a.scatter(X, Y, c='y', s=10, alpha=0.5)
    a.grid(True, linestyle='--', alpha=0.3)

# 数据划分
trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2)

d = 20
polyHigh = PolynomialFeatures(degree=d, include_bias=False)
x_train = polyHigh.fit_transform(trainX)
x_test = polyHigh.fit_transform(testX)

model = make_pipeline(StandardScaler(), LinearRegression())

# 1. 不加正则化
model.fit(x_train, trainY)

y_train0 = model.predict(x_train)
y_pred0 = model.predict(x_test)
train_loss0 = mean_squared_error(trainY, y_train0)
test_loss0 = mean_squared_error(testY, y_pred0)

ax[0, 0].plot(X, model.predict(polyHigh.transform(X)), 'r')
ax[0, 0].text(-3, 1, f"训练误差: {train_loss0:.4f}\n测试误差: {test_loss0:.4f}")
ax[1, 0].bar(np.arange(d), model[1].coef_.reshape(-1))


# 2. 加 L1 正则化 (Lasso回归)
lasso = make_pipeline(StandardScaler(), Lasso(alpha=0.01))
lasso.fit(x_train, trainY)

y_train1 = lasso.predict(x_train)
y_pred1 = lasso.predict(x_test)
train_loss1 = mean_squared_error(trainY, y_train1)
test_loss1 = mean_squared_error(testY, y_pred1)

ax[0, 1].plot(X, lasso.predict(polyHigh.transform(X)), 'r')
ax[0, 1].text(-3, 1, f"训练误差: {train_loss1:.4f}\n测试误差: {test_loss1:.4f}")
ax[1, 1].bar(np.arange(d), lasso[1].coef_.reshape(-1))

# 3. 加 L2 正则化 (Ridge回归)
ridge = make_pipeline(StandardScaler(), Ridge(alpha=1))
ridge.fit(x_train, trainY)

y_train2 = ridge.predict(x_train)
y_pred2 = ridge.predict(x_test)
train_loss2 = mean_squared_error(trainY, y_train2)
test_loss2 = mean_squared_error(testY, y_pred2)

ax[0, 2].plot(X, ridge.predict(polyHigh.transform(X)), 'r')
ax[0, 2].text(-3, 1, f"训练误差: {train_loss2:.4f}\n测试误差: {test_loss2:.4f}")
ax[1, 2].bar(np.arange(d), ridge[1].coef_.reshape(-1))

plt.show()