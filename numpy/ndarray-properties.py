# -*- coding: utf-8 -*-
"""
NumPy ndarray 属性案例
======================
演示 NumPy 数组的核心属性：维度、形状、元素个数、数据类型、字节大小等。
"""

import numpy as np


# ============================================================
# 1. 创建二维数组
# ============================================================
print("=" * 50)
print("1. 创建二维数组")
print("=" * 50)

arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr)
# [[1 2 3]
#  [4 5 6]]


# ============================================================
# 2. 核心属性
# ============================================================
print("\n" + "=" * 50)
print("2. 核心属性")
print("=" * 50)

# ---------- 维度 (ndim) ----------
# 数组的轴（维度）的个数，也叫 rank
print(f"维度 (ndim):        {arr.ndim}")         # 2  → 二维数组

# ---------- 形状 (shape) ----------
# 各维度的大小，返回元组
print(f"形状 (shape):       {arr.shape}")       # (2, 3)  → 2行3列

# ---------- 元素总个数 (size) ----------
# 数组中所有元素的个数
print(f"元素个数 (size):     {arr.size}")        # 6

# ---------- 数据类型 (dtype) ----------
# 数组中元素的数据类型
print(f"数据类型 (dtype):    {arr.dtype}")       # int64（取决于平台）

# ---------- 每个元素的字节数 (itemsize) ----------
# 每个元素占用的字节数
print(f"每个元素字节数 (itemsize): {arr.itemsize} 字节")  # 8（int64 = 8字节）

# ---------- 总字节数 (nbytes) ----------
# 整个数组占用的内存字节数 = size × itemsize
print(f"总字节数 (nbytes):   {arr.nbytes} 字节")  # 48


# ============================================================
# 3. 其他重要属性
# ============================================================
print("\n" + "=" * 50)
print("3. 其他重要属性")
print("=" * 50)

# ---------- T（转置） ----------
# 返回数组的转置视图（不复制数据）
print(f"转置 (T):\n{arr.T}")
# [[1 4]
#  [2 5]
#  [3 6]]
print(f"原形状: {arr.shape}  →  转置后: {arr.T.shape}")  # (2,3) → (3,2)

# ---------- data（数据缓冲区） ----------
# 指向数组数据起始位置的 Python buffer 对象（一般不直接使用）
print(f"数据缓冲区 (data):   {arr.data}")

# ---------- real / imag（实部 / 虚部） ----------
# 复数数组时有用；实数数组 real 返回自身，imag 返回全零
print(f"实部 (real):\n{arr.real}")
print(f"虚部 (imag):\n{arr.imag}")

# ---------- flat（扁平迭代器） ----------
# 返回一个一维迭代器，遍历所有元素
print("扁平迭代器 (flat):  ", end="")
for item in arr.flat:
    print(item, end=" ")
print()  # 1 2 3 4 5 6

# ---------- strides（步长） ----------
# 在每个维度上移动到下一个元素需要跳过的字节数
print(f"步长 (strides):      {arr.strides}")    # (24, 8) → 下一行跨24字节，下一列跨8字节

# ---------- base（基础数组） ----------
# 如果当前数组是另一个数组的视图，base 指向原数组；否则为 None
view = arr[:1, :2]           # 切片生成视图
print(f"视图的 base 是否为 arr: {view.base is arr}")  # True
print(f"原数组的 base:         {arr.base}")            # None → 自己拥有数据
print(f"view:                 {view}")

# ---------- flags（内存布局信息） ----------
# 数组内存布局的标志位
print(f"\nflags 信息:")
print(f"  C_CONTIGUOUS:    {arr.flags['C_CONTIGUOUS']}")     # C 顺序连续
print(f"  F_CONTIGUOUS:    {arr.flags['F_CONTIGUOUS']}")     # Fortran 顺序连续
print(f"  OWNDATA:         {arr.flags['OWNDATA']}")          # 是否拥有数据
print(f"  WRITEABLE:       {arr.flags['WRITEABLE']}")        # 是否可写
print(f"  ALIGNED:         {arr.flags['ALIGNED']}")          # 是否对齐


# ============================================================
# 4. 属性对比：不同数据类型
# ============================================================
print("\n" + "=" * 50)
print("4. 不同数据类型对比")
print("=" * 50)

# 同一个数组，不同 dtype —— 演示 itemsize 和 nbytes 的变化
for dtype_name in ["int32", "int64", "float32", "float64", "complex128"]:
    a = np.array([[1, 2, 3], [4, 5, 6]], dtype=dtype_name)
    print(f"dtype={str(a.dtype):12s}  "
          f"itemsize={a.itemsize:2d}字节  "
          f"nbytes={a.nbytes:3d}字节  "
          f"shape={str(a.shape):8s}")


# ============================================================
# 5. shape / reshape / resize 的关系
# ============================================================
print("\n" + "=" * 50)
print("5. shape 重塑相关")
print("=" * 50)

a = np.array([[1, 2, 3], [4, 5, 6]])
print(f"原数组 (2×3):\n{a}")

# reshape：返回新形状的视图（共享数据），-1 表示自动推导
b = a.reshape(3, 2)
print(f"\nreshape(3, 2):\n{b}")
print(f"b 和 a 共享数据: {b.base is a if b.base is not None else '不共享（但这里肯定共享）'}")

# 用 -1 自动推导维度
c = a.reshape(-1)   # 展平为一维
print(f"\nreshape(-1) 展平: {c}")  # [1 2 3 4 5 6]

# 注意：reshape 要求元素个数匹配，否则报错
# a.reshape(2, 2)  # ❌ ValueError: cannot reshape array of size 6 into shape (2,2)


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 50)
print("属性速查表")
print("=" * 50)
print("""
┌──────────────┬──────────────────────────────────────┐
│ 属性         │ 说明                                 │
├──────────────┼──────────────────────────────────────┤
│ ndim         │ 数组的维度数（轴数）                 │
│ shape        │ 各维度大小的元组                     │
│ size         │ 元素总个数                           │
│ dtype        │ 元素的数据类型                       │
│ itemsize     │ 每个元素的字节数                     │
│ nbytes       │ 数组总字节数 (= size × itemsize)     │
│ T            │ 转置视图                             │
│ real / imag  │ 实部 / 虚部                          │
│ flat         │ 扁平迭代器                           │
│ strides      │ 各维度步长（字节）                   │
│ base         │ 视图的基础数组（None 表示拥有数据）  │
│ flags        │ 内存布局标志                         │
│ data         │ 数据缓冲区                           │
└──────────────┴──────────────────────────────────────┘
""")
