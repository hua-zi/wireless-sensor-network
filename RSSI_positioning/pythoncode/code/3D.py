#  Rssi 3D定位算法
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 锚节点
class node:
    x=0
    y=0
    z=0
    D=0

# 观察目标
class target:
    x=0
    y=0
    z=0

# 两点之间距离
def Get_DIST(A,B):
    dist = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2 + (A.z - B.z) ** 2)**0.5
    return dist

# 当距离为d时，采用得到Rssi的值
def GetRssiValue(d):
    A = -42
    n = 2   # A, n在不同的硬件系统取值不一样
    Q = 5   # 噪声方差，由于Rssi测量时噪声非常大
    value = A - 10 * n * math.log10(d) + (Q**0.5) * random.gauss(0,1)
    return value

# 由Rssi的值计算距离d
def GetDistByRssi(rssi):
    A = -42
    n = 2  # A, n在不同的硬件系统取值不一样
    d = 10 ** ((A - rssi) / 10 / n)
    return d

# 参数设置
Length=100
Width=100
Hight=100               #初始化场地
Node_number=5           #观测站个数，至少4个
Node=[]
for i in range(Node_number):
    tmp_node = node()
    tmp_node.x = Width * random.random()
    tmp_node.y=Length*random.random()
    tmp_node.z=Hight*random.random()
    #观测站位置初始化
    tmp_node.D=tmp_node.x**2+tmp_node.y**2+tmp_node.z**2
    Node.append(tmp_node)

Target = target()
Target.x=Width*random.random()
Target.y=Length*random.random()
Target.z=Hight*random.random()    #目标真实位置，随机
#各观测站对目标探测10次，取平均值作为Rssi值
Z=[]
#各观测站对目标探测20次Rssi值
Rssi = np.zeros((Node_number,20))
for i in range(Node_number):
    for t in range(20):
        d=Get_DIST(Node[i],Target)  #观测站与目标的真实距离
        Rssi[i,t]=GetRssiValue(d)    #得到Rssi的值

ZZ=np.zeros(Node_number)  #储存十次观测的平均值
for i in range(Node_number):
    ZZ[i]=np.sum(Rssi[i,:])/20

#根据Rssi求观测距离
Zd=np.zeros(Node_number)  #计算的距离
for i in range(Node_number):
    Zd[i]=GetDistByRssi(ZZ[i])

#根据观测距离用最小二乘法估计目标位置
H=np.zeros((Node_number-1,3))
b=np.zeros(Node_number-1)
for i in range(1,Node_number):
    # A 矩阵 和 B 矩阵
    H[i-1]=[2*(Node[i].x-Node[1].x),2*(Node[i].y-Node[1].y),2*(Node[i].z-Node[1].z)]
    b[i-1]=Zd[1]**2-Zd[i]**2+Node[i].D-Node[1].D

# Estimate=inv(H'*H)*H'*b #估计目标位置
H_zhuanzhi = np.transpose(H) # H'
# np.dot( np.transpose(H), H ) # (H'*H)
# np.linalg.inv(np.dot( np.transpose(H), H))  # inv(H'*H)
HHH = np.dot( np.linalg.inv(np.dot( np.transpose(H), H)), H_zhuanzhi) # inv(H'*H)*H'
Estimate = np.dot(HHH,b)

Est_Target = target()
Est_Target.x=Estimate[0]
Est_Target.y=Estimate[1]
Est_Target.z=Estimate[2]

########画图########
fig1 = plt.figure(dpi=80)
ax = plt.subplot(projection='3d')  #设置3D绘图空间
plt.grid(linestyle="dotted")
# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 设置坐标范围
ax.set_xlim3d(0,Width)
ax.set_ylim3d(0,Length)
ax.set_zlim3d(0,Hight)
# 画锚节点
for i in range(Node_number):
    print(Node[i].x,Node[i].y,Node[i].z)
    a=ax.scatter(Node[i].x,Node[i].y,Node[i].z,linewidths=5)
# 画目标节点 真实值和预测值
b=ax.scatter(Target.x,Target.y,Target.z,marker='*',s=100)
c=ax.scatter(Est_Target.x,Est_Target.y,Est_Target.z,marker='D',s=80)
ax.plot([Est_Target.x,Target.x],[Est_Target.y,Target.y],[Est_Target.z,Target.z], color='r')

plt.tick_params(labelsize=13)
ax.legend([a,b,c],['观测站','目标位置','估计位置'],prop={"size": 15})
Error_Dist=Get_DIST(Est_Target,Target)  # 计算误差
plt.title('锚节点数：'+str(Node_number)+'\nerror='+str(Error_Dist)+'m',fontdict={"size": 15})

plt.show()

