import numpy as np
import matplotlib.pyplot as plt
import init
#从Scikit-Learn库导入聚类模型中的K-means聚类算法
from sklearn.cluster import KMeans

## 读取数据
r=init.Parameter()
x = np.load("x.npy")
y = np.load("y.npy")
k = 4  # 聚类数
# k=r.n # 退化成星型拓扑

## 绘制树型拓扑结构
fig = plt.figure(dpi=80)
plt.xlim(0,r.xlim)
plt.ylim(0,r.ylim)
# 绘制网络节点
plt.scatter(x,y)
# 聚类
p=np.stack([x,y])
p=np.transpose(p)
kmeans =KMeans(n_clusters=k).fit(p)
# 画聚类中心
x_z = np.mean(x)
y_z = np.mean(y)
plt.scatter(x_z,y_z,s=100)
# print(kmeans.cluster_centers_)
for i in range(k):
    plt.scatter(kmeans.cluster_centers_[i,0],kmeans.cluster_centers_[i,1])
    plt.plot([kmeans.cluster_centers_[i,0],x_z],[kmeans.cluster_centers_[i,1],y_z])

print(kmeans.labels_)
idx = kmeans.labels_
# 网络节点接入
for i in range(r.n):
    plt.plot([kmeans.cluster_centers_[idx[i], 0], p[i,0]], [kmeans.cluster_centers_[idx[i], 1], p[i,1]])

plt.show()