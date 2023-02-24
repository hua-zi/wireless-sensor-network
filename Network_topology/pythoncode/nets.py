import numpy as np
import matplotlib.pyplot as plt
import init

## 读取数据
r=init.Parameter()
x = np.load("x.npy")
y = np.load("y.npy")

## 绘制网状拓扑结构
fig = plt.figure(dpi=80)
plt.xlim(0,r.xlim)
plt.ylim(0,r.ylim)
# 绘制网络节点
plt.scatter(x,y)

# 网络节点接入
for i in range(r.n):
    for j in range(r.n):
        plt.plot([x[i],x[j]],[y[i],y[j]])

plt.show()