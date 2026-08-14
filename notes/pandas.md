# Pandas

## Series

### 核心API

```python
s = pd.Series([1, 2, 3, 4, 5])
s = pd.Series({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5})
s = pd.Series(s, index=['A', 'C'])

s['A']
s[s<3]

s.head()
s.tail(3)

s.std() # pandas 标准差为样本标准差，除 n-1
s.quantile(0.6)
s.mean()
s.describe()

s.count()
s.keys()
s.index

s.isna()            # [..., False, True, ...]
s.isna().sum()
s.isin([4, 5, 6])   # [..., False, True, ...]

s.sort_values(ascending='False')
s.drop_duplicates()
s.unique()

s.diff().abs()
s.nlargest
```

## DataFrame

### 核心 API

```python
df = pd.DataFrame({"第一列":s2, '第二列':s1})
df['第一列']
df = pd.DataFrame(
    {
        "name":['Tom', 'Jack', 'Alice', 'Bob', 'Charlie'],
        'age':[15, 17, 20, 26, 30],
        'score':[60.5, 80, 30.6, 70, 83.5]
    }, index= [1, 2, 3, 4, 5],
    columns=['name', 'age', 'score']
)

df.types
df.info()
df.shape
df.size
df[:, 'name']
df[(df.score > 70) & (df.age < 20)]
df[['数学', '语文', '英语']].sum(axis=1)
df.nlargest(1, columns=['总销售额'])

df.sample(5)

df.value_counts()
df.sort_values(by=['age','score'], ascending=[False, True], inplace=True)
```

# 数据分析

```python
# 1. 导入库
import numpy as np
import pandas as pd

# 2. 导入数据
df = read_csv('...')

# 3. 数据清洗
df.isna().sum()
df['sleep_disorder'].value_count()
df.drop(columns='sleep_disorder')

# 4. 特征重构
df['gender'] = df['gender'].astype('category')
df[['high', 'low']] = df['blood_presure'].str.split('/', expand=True)
df['quality_level'] = pd.cut([df['sleep_quality']], bins=3, labels=['good','ok','bad'])
df['age_level'] = pd.cut(df['age'], bins=[0,18,60,np.inf], labels=['youth','adult', 'older'])

def is_zxs(s):
    if s in ['北京','天津','上海','重庆']:
        return True
    else:
        return False
df['is_zxs'] = df['city'].apply(is_zxs) # apply 里面还可以用匿名函数 lambda


# 5. 数据统计
df.groupby(['age_level']).agg({
    'sleep_quality': ['mean', 'median', 'max', 'min'],
    'sleep_duration': ['mean', 'median', 'max', 'min']
}).round(2)
```
