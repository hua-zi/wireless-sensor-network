# Rssi 2D 定位算法, 画出误差随锚节点数的变化趋势
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# 锚节点
class node:
    x=0
    y=0
    D=0

# 观察目标
class target:
    x=0
    y=0

# 计算A,B两点的距离
def Get_DIST(A,B):
    dist = ((A.x - B.x) ** 2 + (A.y - B.y) ** 2)**0.5
    return dist

# 当距离为d时，采用得到Rssi的值
def GetRssiValue(d):
    A = -42
    n = 2  # A, n在不同的硬件系统取值不一样
    Q = 5  # 噪声方差，由于Rssi测量时噪声非常大
    value = A - 10 * n * math.log10(d) + (Q**0.5) * random.gauss(0,1)
    return value

# 由Rssi的值计算距离d
def GetDistByRssi(rssi):
    A = -42
    n = 2   # A, n在不同的硬件系统取值不一样
    d = 10 ** ((A - rssi) / 10 / n)
    return d

# Node_number:观测站个数，至少3个
def forecast_2d(Node_number):
    # 参数设置
    Length=100
    Width=100               #初始化场地
    Node=[]
    for i in range(Node_number):
        tmp_node = node()
        tmp_node.x=Width*random.random()
        tmp_node.y=Length*random.random() #观测站位置初始化
        tmp_node.D=tmp_node.x**2+tmp_node.y**2
        Node.append(tmp_node)

    Target=target()
    Target.x=Width*random.random()
    Target.y=Length*random.random() #目标真实位置，随机

    #各观测站对目标探测10次，取平均值作为Rssi值
    Z=[]
    #各观测站对目标探测10次Rssi值
    Rssi = np.zeros((Node_number,10))
    for i in range(Node_number):
        for t in range(10):
            d = Get_DIST(Node[i],Target) #观测站与目标的真实距离
            Rssi[i,t] = GetRssiValue(d)   #得到Rssi的值

    ZZ=np.zeros(Node_number) #储存十次观测的平均值
    for i in range(Node_number):
        ZZ[i] = np.sum(Rssi[i,:])/10

    #根据Rssi求观测距离
    Zd=np.zeros(Node_number) #计算的距离
    for i in range(Node_number):
        Zd[i]=GetDistByRssi(ZZ[i])

    # 根据观测距离用最小二乘法估计目标位置
    H=np.zeros((Node_number-1,2))
    b=np.zeros(Node_number-1)
    for i in range(1,Node_number):
        # A 矩阵 和 B 矩阵
        H[i-1]=[2*(Node[i].x-Node[1].x),2*(Node[i].y-Node[1].y)]
        b[i-1]=Zd[1]**2-Zd[i]**2+Node[i].D-Node[1].D

    H_zhuanzhi = np.transpose(H) # H'
    HHH = np.dot( np.linalg.inv(np.dot( np.transpose(H), H)), H_zhuanzhi) # inv(H'*H)*H'

    Estimate = np.dot(HHH,b)
    Est_Target = target()
    Est_Target.x=Estimate[0]
    Est_Target.y=Estimate[1]

    Error_Dist=Get_DIST(Est_Target,Target)
    # print(Error_Dist)
    return Error_Dist   # 返回预测误差

def plot_error_curve(start,end):
    x=[]
    y=[]
    for i in range(start,end):
        sum=0
        for j in range(10):
            sum += forecast_2d(i)
        sum /= 10
        x.append(i)
        y.append(sum)

    fig1 = plt.figure(dpi=80)
    plt.grid(linestyle="dotted")
    # 解决中文显示问题
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x,y)

    plt.xlabel('锚节点数', fontdict={"size": 15})
    plt.ylabel('误差/m', fontdict={"size": 15})
    plt.tick_params(labelsize=13)
    plt.title('二维RSSI定位',fontdict={"size": 15})

    plt.show()

if __name__ == '__main__':
    # plot_error_curve(2, 20)     # 报错，二维定位观察站至少3个
    plot_error_curve(4,40)        # 观测站数4~39，从4开始是为了画图好看