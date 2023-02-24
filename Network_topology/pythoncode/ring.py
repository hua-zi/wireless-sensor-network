import numpy as np
import matplotlib.pyplot as plt
import init

## 读取数据
r=init.Parameter()
x = np.load("x.npy")
y = np.load("y.npy")

## 绘制环型拓扑结构
fig = plt.figure(dpi=80)
plt.xlim(0,r.xlim)
plt.ylim(0,r.ylim)
# 绘制网络节点
plt.scatter(x,y)
# 成环
Point = np.stack([x,y])
d = np.array([x-np.mean(x),y-np.mean(y)])   # 各点到中点的连线
angle = np.arctan2(d[1,:],d[0,:])           # 各点中点连线与x轴角度
# 按角度排序
i = np.argsort(angle)
angle= np.sort(angle)
x = Point[0,i].tolist()
y = Point[1,i].tolist()
x.append(x[0]) #加入起点到最末，形成闭合图形
y.append(y[0])
plt.plot(x,y)

plt.show()