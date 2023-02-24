import random
import numpy as np

class Parameter:
    ## 设置参数
    n = 15
    xlim = 100
    ylim = 100

if __name__ == '__main__':
    parameter = Parameter()
    ## 生成网络节点
    r = np.random.uniform(0, parameter.xlim, (2, parameter.n))
    x = r[0, :]
    y = r[1, :]
    np.save("x.npy",x)
    np.save("y.npy", y)
