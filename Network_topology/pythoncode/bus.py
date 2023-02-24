import numpy as np
import matplotlib.pyplot as plt
import init

## 读取数据
r=init.Parameter()
x = np.load("x.npy")
y = np.load("y.npy")

## 绘制总线型拓扑结构
fig = plt.figure(dpi=80)
plt.xlim(0,r.xlim)
plt.ylim(0,r.ylim)
# 绘制网络节点
plt.scatter(x,y)

# 绘制总线
plt.plot([0,r.xlim],[r.ylim/2,r.ylim/2])

# 网络节点接入
for i in range(r.n):
    plt.plot([x[i],x[i]],[r.ylim/2,y[i]])

plt.show()