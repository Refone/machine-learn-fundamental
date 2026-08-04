import numpy as np

# 2.4.2 zeros()、ones()、empty()与zeros_like()、ones_like()、empty_like()
# 2.4.3 full()与full_like()
# 2.4.4 arange()

def zeros_ones_empty():
    '''
    第一组
    极简区分（一眼看懂）
    指定形状分别创建全 0、全 1、空值数组：zeros(形状)、ones(形状)、empty(形状)
    参照数组分别创建全 0、全 1、空值数组：zeros_like(数组)、ones_like(数组)、empty_like(数组)

    总结
    无 _like 的必须指定形状，按需创建数组。
    带 _like 的不用手动写形状，直接抄已有数组的尺寸；
    '''

    # 创建2行3列全0
    a = np.zeros((2,3))
    print(a)
    # 创建2行3列全1
    b = np.ones((2, 3))
    print(b)
    # np.empty 并不保证数组元素被初始化为 0，它只是分配内存空间，
    # 数组中的元素值是未初始化的，可能是内存中的任意值。
    # 3行3列空值（未初始化）
    c = np.empty((3, 3))
    print(c)

    print("*" * 20)

    #a = [1,2]
    a = [[1, 2], [3, 4]];
    #参照a的形状创建
    d = np.zeros_like(a)  # 和a形状一样的全0
    print(d)
    e = np.ones_like(a)  # 和a形状一样的全1
    print(e)
    f = np.empty_like(a)  # 和a形状一样的空值
    print(f)

def full_fulllike():
    '''
    第二组
    full() 是按指定形状 + 自定义值创建数组。|自己定形状，填任意值
    full_like() 照着抄，参照已有数组形状 + 自定义值创建数组。|抄别人形状，填任意值

    极简区分
    指定形状创建：np.full(形状, 填充值)
    参照数组创建：np.full_like(已有数组, 填充值)
    '''
    # 1. full()：指定形状(2,3)，全部填充 8  |自己定形状，填任意值
    a = np.full((2, 3), 8)
    print(a)
    print("*"*30)
    # 2. full_like()：和 a 形状一样，全部填充 7  |抄别人形状，填任意值
    b = np.full_like(a,99)
    print(b)

def myarange():
    '''
    第三组
    一句话总结
    arange() 是按指定 起始值、终止值、步长 生成一维等差数列数组（遵循左闭右开，不包含终止值）。
    极简用法
    np.arange(起始, 终止, 步长)
    '''
    print(np.arange(2,10,3))

    # 复习python原生的range函数
    a = range(1,10,2)
    print("python原生的range函数: ",list(a))

if __name__ == '__main__':
    zeros_ones_empty()

    full_fulllike()

    myarange()