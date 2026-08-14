# Numpy

多维性 ｜ 同质性 ｜ 高效性

## 核心属性

假设 `arr = np.array([[1, 2], [3, 4]])`

| 属性名称 | 通俗解释 | 使用示例 | 输出结果 |
| :--- | :--- | :--- | :--- |
| shape | 数组的形状 | `arr.shape` | `(2, 2)` |
| ndim | 维度数量 | `arr.ndim` | `2` |
| size | 总元素个数 | `arr.size` | `4` |
| dtype | 元素类型 | `arr.dtype` | `int64` (或 `int32`) |
| T | 转置 | `arr.T` | `[[1,3],[2,4]]` |
| itemsize | 单个元素占用字节 | `arr.itemsize` | `8` (int64) |
| nbytes | 数组总字节数 | `arr.nbytes` | `32` (4 x int64) |

## ndarry 的创建

### 基础构造

```python
np.array([[1,2],[3,4]])
np.copy(arr)
```

### 预定义填充

```python
np.zeros(2, 3)  # 2行3列，shape = (2,3) 的全0数组
np.ones(2, 3)
np.full((2, 3), 5)

np.zeros_like(arr)
np.full_like(arr, 5)
```

### 范围生成

```python
np.arange(0, 10, 2)     # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)    # [0.0, 0.25, 0.5, 0.75, 1.0]
np.logspace(0, 2, 3, base = 10) # [1.0, 10.0, 100.0]
```

### 特殊矩阵

```python
np.eye(3) # 3x3 单位矩阵
np.diag([1, 2, 3])  # 3x3 对角矩阵
```

### 随机矩阵

```python
# 2 x 2 随机矩阵
np.random.rand(2, 2)                # [0,1) 均匀
np.random.uniform(1, 10, (2, 2))    # [1, 10) 浮点数
np.random.randn(2, 2)               # 标准分布
np.random.normal(μ, σ, (2, 2))      # μ,σ 正态分布
np.random.randint(1, 10, (2, 2))    # [1, 10) 整数
```

### 拼接矩阵

注：np 默认都是 **列向量**
```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

"""
a:          b:
    1 | 3       5 | 7
    2 | 4       6 | 8
"""
np.vstack((a, b)) # 竖直堆叠
"""
[[1, 2],
 [3, 4],
 [5, 6],
 [7, 8]]

1 | 3 | 5 | 7
2 | 4 | 6 | 8
"""

np.hstack((a, b)) # 水平堆叠
"""
[[1, 2, 5, 6],
 [3, 4, 7, 8]]

1 | 3
2 | 4
5 | 7
6 | 8
"""
```

## 数据类型

```python
"""
int8  | int16  | int32  | int64
i1    | i2     | i4     | i8
uint8 | uint16 | uint32 | uint64
u1    | u2     | u4     | u8

float16 | float32 | float64
f2      | f4      | f8
        | f       | d
"""
```

```python
np.array([1, 2, 3], dtype=np.float32)
np.array([1, 2, 3], dtype='i8')
arr.astype(np.int64)
```

## 索引与切片
```python
arr = np.arange(1, 10).reshape(3, 3)
"""
1 2 3
4 5 6
7 8 9
"""
arr[1, 2] # 6
arr[:, 1] # [2, 5, 8] shape = (3,)
arr[1, :] # [4, 5, 6] shape = (3,)
arr[::2, ::2] # [[1, 3],[7, 9]] shape = (2, 2)

# 条件索引
arr[arr > 0]
print(arr[2][arr[2] > 50])
print(arr[2, arr[2] > 50])
```

## 基本运算

* 相同维度(shape)：\+ \- \* \/ 相同位置逐元素计算
* 不同维度：广播机制，1 -> 合适维度，只能从 1 扩展

## 重要统计函数

可搭配 `axis=0` 参数，约束维度。

大部分第一个参数为 `arr` 的，也可以通过 `arr.xxx()` 调用。

| 统计量名 | API |
| :--- | :--- |
| 总和 | `np.sum(arr)` |
| 计数 | `np.size(arr)` |
| 平均数 | `np.mean(arr)` |
| 中位数 | `np.median(arr)` |
| 众数 | `np.mode(arr)` |
| 最大索引 | `np.argmax(arr)` |
| 最小索引 | `np.argmin(arr)` |
| 方差 | `np.var(a)` |
| 标准差 | `np.std(a)` |
| 分位数 | `np.quantile(a, 0.25, axis=0)` |
| 协方差 | `np.cov()` |
| 累加和 | `np.cumsum()` |
| 唯一值 | `np.unique()` |
| 范数 | `np.linalg.norm(ord=2)` |
| 展平 | `np.flatten(arr)` |
| 变形 | `arr.reshape((3, 3))` |
