import numpy as np
import matplotlib.pyplot as plt
import init

## 读取数据
r=init.Parameter()
x = np.load("x.npy")
y = np.load("y.npy")

## 绘制星型拓扑结构
fig = plt.figure(dpi=80)
plt.xlim(0,r.xlim)
plt.ylim(0,r.ylim)
# 绘制网络节点
plt.scatter(x,y)

# 生成中心节点
x_z = np.mean(x)
y_z = np.mean(y)
plt.scatter(x_z,y_z,s=100)

# 网络节点接入
for i in range(r.n):
    plt.plot([x_z,x[i]],[y_z,y[i]])

plt.show()