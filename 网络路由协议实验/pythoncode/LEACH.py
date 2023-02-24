import numpy as np
import matplotlib.pyplot as plt
import random

# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class BaseStation:  # 定义基站类
    x=0
    y=0

class SensorNode:  # 定义传感器节点
    xd=0
    yd=0
    d=0
    Rc = 0
    temp_rand=0
    type = 'N'
    selected = 'N'
    power = 0
    CH = 0
    flag = 1
    N = []
    Num_N = 0
    FN = []
    Num_FN = 0
    CN = []
    Num_CN = 0
    num_join = 0

# 初始化参数
xm = 100                          # x轴范围
ym = 100                          # y轴范围
sink = BaseStation()
sink.x = 50                       # 基站x轴
sink.y = 125                      # 基站y轴
n = 400                           # 节点总数
p = 0.08                          # 簇头概率
Eelec = 50*(10**(-9))
Efs=10*(10**(-12))
Emp=0.0013*(10**(-12))
ED=5*(10**(-9))
d0 = 87
packetLength = 4000
ctrPacketLength = 100
rmax = 200                  # 迭代次数
E0 = 0.5                     # 初始能量
Emin = 0.001                 # 节点存活所需的最小能量
Rmax = 15                    # 初始通信距离

## 节点随机分布
fig1 = plt.figure(dpi=80)
plt.grid(linestyle="dotted")
Node = []
plt.scatter(sink.x, sink.y,marker='*',s=200)
for i in range(n):
    node = SensorNode()
    node.xd = random.random()*xm
    node.yd = random.random()*ym         # 随机产生100个点
    node.d = ((node.xd-sink.x)**2+(node.yd-sink.y)**2)**0.5    # 节点距基站的距离
    node.Rc = Rmax                 # 节点的通信距离
    node.temp_rand = random.random()          # rand为(0,1)的随机数
    node.type = 'N'                # 进行选举簇头前先将所有节点设为普通节点
    node.selected = 'N'            # ’O'：当选过簇头，N：没有
    node.power = E0                # 初始能量
    node.CH = 0                    # 保存普通节点的簇头节点，-1代表自己是簇头
    node.flag = 1                  # 1代表存活；0代表死亡
    node.N = [0 for _ in range(n) ]         # 邻居节点集
    node.Num_N = 0                # 邻居节点集个数
    node.FN = [0 for _ in range(n)]        # 前邻节点集
    node.Num_FN = 0               # 前邻节点集个数
    node.CN = [0 for _ in range(n)]         # 前簇头节点集
    node.Num_CN = 0               # 前簇头节点集个数
    Node.append(node)
    plt.scatter(node.xd, node.yd,marker='o')
plt.legend(['基站', '节点'])
plt.xlabel('x', fontdict={"family": "Times New Roman", "size": 15})
plt.ylabel('y', fontdict={"family": "Times New Roman", "size": 15})

# save data
flag = 1
################IMP_LEACH##################
# 迭代
alive_ima_leach = np.zeros((rmax, 1))        # 每轮存活节点数
re_ima_leach = np.zeros((rmax, 1))          # 每轮节点总能量
for r in range(rmax):
    final_CH=[]
    for i in range(n):
        if Node[i].flag != 0:
            re_ima_leach[r] = re_ima_leach[r]+Node[i].power # 更新总能量
            alive_ima_leach[r] = alive_ima_leach[r]+1       # 更新存活节点
    f = 0
    if alive_ima_leach[r] == 0:
        stop = r
        f = 1
        break
    for i in range(n):
        Node[i].type = 'N'               # 进行选举簇头前先将所有节点设为普通节点
        Node[i].selected = 'N'
        Node[i].temp_rand = random.random()         # 节点取一个(0,1)的随机值，与p比较
        Node[i].Rc = Rmax*Node[i].power/E0    # 节点的通信距离
        Node[i].CH = 0
        Node[i].N = np.zeros(n)               # 邻居节点集
        Node[i].Num_N = 0                     # 邻居节点集个数
        Node[i].FN = np.zeros(n)              # 前邻节点集
        Node[i].Num_FN = 0                    # 前邻节点集个数
        Node[i].CN = np.zeros(n)              # 前簇头节点集
        Node[i].Num_CN = 0                    # 前簇头节点集个数
        Node[i].num_join = 1                  # 簇成员的个数
    # 簇头选举
    count = 0  # 簇头个数
    for i in range(n):
        if Node[i].selected == 'N' and Node[i].flag != 0:
            if Node[i].d > d0:
                alpha = 4  # 能量损失指数
            else:
                alpha = 2
            Eavg = 0  # 系统节点平均能量
            m = 0     # 存活节点个数
            for j in range(n):
                if Node[i].flag != 0:
                    Eavg = Eavg + Node[i].power
                    m = m + 1
            if m != 0:
                Eavg = Eavg / n  # 计算系统节点平均能量
            else:
                break
            if Node[i].temp_rand <= (p / (1 - p * (r % round(1 / p)) * (Node[i].power / Eavg) ** (1 / alpha))) and \
                    Node[i].d > Node[i].Rc:
                Node[i].type = 'C'      # 节点类型为簇头
                Node[i].selected = 'O'  # 该节点标记'O'，说明当选过簇头
                Node[i].CH = -1
                count = count + 1
                final_CH.append(i)      # 加入簇头节点集合
                # 广播自成为簇头
                distanceBroad = (Node[i].Rc ** 2 + Node[i].Rc ** 2) ** 0.5
                if (distanceBroad > d0):
                    Node[i].power = Node[i].power - (
                                Eelec * ctrPacketLength + Emp * ctrPacketLength * (distanceBroad ** 4))
                else:
                    Node[i].power = Node[i].power - (
                                Eelec * ctrPacketLength + Efs * ctrPacketLength * distanceBroad ** 2)
            else:
                Node[i].type = 'N'  # 节点类型为普通
    # 计算邻居节点集合
    for i in range(n):
        cnt = 0
        for j in range(n):
            if i != j:
                dist = ((Node[i].xd-Node[j].xd)**2+(Node[i].yd-Node[j].yd)**2)**0.5
                if dist < Node[i].Rc:
                    cnt = cnt + 1
                    Node[i].N[cnt] = j
                    # if len(Node[i].N)<cnt:
                    #     Node[i].N.append(j)
                    # else:
                    #     Node[i].N[cnt-1] = j
            if j == n:
                Node[i].Num_N = cnt
    # 计算前邻节点集
    for i in range(n):
        cnt = 0
        for j in range(Node[i].Num_N):
            ne = Node[i].N[j]
            if Node[ne].d < Node[i].d:
                cnt = cnt + 1
                Node[i].FN[cnt] = ne
            if j == Node[i].Num_N:
                Node[i].Num_FN = cnt
    # 计算前簇头节点集
    for i in range(count):
        cnt = 0
        for j in range(Node[i].Num_FN):
            fne = Node[final_CH[i]].FN[j]
            if fne != 0 and Node[fne].d < Node[final_CH[i]].d and Node[fne].CH == -1:
                cnt = cnt + 1
                Node[final_CH[i]].CN[cnt] = fne
            if j == Node[i].Num_FN:
                Node[final_CH[i]].Num_CN = cnt
    # 加入簇
    for i in range(n):
        if Node[i].type == 'N' and Node[i].power > 0:
            E = np.zeros(count)
            for j in range(count):
                dist = ((Node[i].xd-Node[final_CH[j]].xd)**2+(Node[i].yd-Node[final_CH[j]].yd)**2)**0.5
                if dist < Node[final_CH[j]].Rc:    # 满足条件1
                    E[j] = (Node[final_CH[j]].power-Emin)/Node[final_CH[j]].num_join
            if len(E)>0:
                max_value, max_index = np.max(E),np.argmax(E)
            else:
                max_value, max_index = 0,0
            # 节点发送加入簇的消息
            if len(final_CH) != 0:
                dist = ((Node[i].xd - Node[final_CH[max_index]].xd) ** 2 + (
                            Node[i].yd - Node[final_CH[max_index]].yd) ** 2) ** 0.5
                if dist > Node[final_CH[max_index]].Rc:  # 不满足条件1，选择最近的簇头加入
                    Length = np.zeros(count)
                    for j in range(count):
                        Length[j] = ((Node[i].xd - Node[final_CH[j]].xd) ** 2 + (
                                    Node[i].yd - Node[final_CH[j]].yd) ** 2) ** 0.5
                    min_value, min_index = np.min(Length), np.argmin(Length)
                    Node[i].CH = final_CH[min_index]
                    # 节点发送加入簇的消息
                    Node[i].power = Node[i].power - (Eelec * ctrPacketLength + Efs * ctrPacketLength * (dist ** 2))
                    # 簇头接收消息
                    Node[final_CH[min_index]].power = Node[final_CH[min_index]].power - Eelec * ctrPacketLength
                    Node[final_CH[min_index]].num_join = Node[final_CH[min_index]].num_join + 1
                else:
                    # 节点发送加入簇的消息
                    Node[i].power = Node[i].power - (Eelec * ctrPacketLength + Efs * ctrPacketLength * (dist ** 2))
                    # 簇头接收消息
                    Node[final_CH[max_index]].power = Node[final_CH[max_index]].power - Eelec * ctrPacketLength
                    Node[final_CH[max_index]].Rc = Rmax * Node[final_CH[max_index]].power / E0
                    Node[i].CH = final_CH[max_index]
                    Node[final_CH[max_index]].num_join = Node[final_CH[max_index]].num_join + 1
    # 能量模型
    # 发送数据
    for i in range(n):
        if Node[i].flag != 0:
            if Node[i].type == 'N' and Node[i].CH != 0:  # 普通节点
                dist = ((Node[i].xd - Node[Node[i].CH].xd) ** 2 + (Node[i].yd - Node[Node[i].CH].yd) ** 2) ** 0.5
                if dist > d0:
                    Node[i].power = Node[i].power - (Eelec * packetLength + Emp * packetLength * (dist ** 4))
                else:
                    Node[i].power = Node[i].power - (Eelec * packetLength + Efs * packetLength * (dist ** 2))
            else:  # 簇头节点
                Node[i].power = Node[i].power - (Eelec + ED) * packetLength  # 簇头接收数据
                if Node[i].d <= Node[i].Rc:
                    Node[i].power = Node[i].power - (Eelec * packetLength + Efs * packetLength * (Node[i].d ** 2))
                else:
                    if Node[i].Num_CN == 0:
                        if Node[i].d > d0:
                            Node[i].power = Node[i].power - (
                                        Eelec * packetLength + Emp * packetLength * (Node[i].d ** 4))
                        else:
                            Node[i].power = Node[i].power - (
                                        Eelec * packetLength + Efs * packetLength * (Node[i].d ** 2))
                    else:
                        # 选择中继节点
                        dis = np.zeros((Node[i].Num_CN, 1))
                        # 计算前簇头节点距基站的距离
                        for j in range(Node[i].Num_CN):
                            dis[j] = Node[Node[i].CN[j]].d
                        index = np.argsort(dis)
                        di = dis[index]
                        # 中继转发
                        for j in range(Node[i].Num_CN):
                            Node[i].power = Node[i].power - di[j] / np.sum(di) * (
                                        Eelec * packetLength + Emp * packetLength * (di[Node[i].Num_CN + 1 - j] ** 2))
    for i in range(n):
        if Node[i].power < Emin:
            Node[i].flag = 0
    final_CH = []
if f == 0:
    stop = rmax

# load data.mat 节点复位
for i in range(n):
    # Node[i].temp_rand = random.random()          # rand为(0,1)的随机数
    Node[i].type = 'N'                # 进行选举簇头前先将所有节点设为普通节点
    Node[i].selected = 'N'            # ’O'：当选过簇头，N：没有
    Node[i].power = E0                # 初始能量
    Node[i].CH = 0                    # 保存普通节点的簇头节点，-1代表自己是簇头
    Node[i].flag = 1                  # 1代表存活；0代表死亡
    Node[i].N = [0 for _ in range(n) ]         # 邻居节点集
    Node[i].Num_N = 0                # 邻居节点集个数
    Node[i].FN = [0 for _ in range(n)]        # 前邻节点集
    Node[i].Num_FN = 0               # 前邻节点集个数
    Node[i].CN = [0 for _ in range(n)]         # 前簇头节点集
    Node[i].Num_CN = 0               # 前簇头节点集个数
################LEACH##################
alive_leach = np.zeros((rmax, 1))         # 每轮存活节点数
re_leach = np.zeros((rmax, 1))            # 每轮节点总能量
for r in range(rmax):
    for i in range(n):
        if Node[i].flag != 0:
            re_leach[r] = re_leach[r]+Node[i].power
            alive_leach[r] = alive_leach[r]+1
    f = 0
    if alive_leach[r] == 0:
        stop = r
        f = 1
        break
    for i in range(n):
        Node[i].type = 'N'                   # 进行选举簇头前先将所有节点设为普通节点
        Node[i].selected = 'N'
        Node[i].temp_rand = random.random()   #节点取一个(0,1)的随机值，与p比较
    for i in range(n):
        if  Node[i].selected == 'N' and Node[i].flag != 0:
            # if  Node[i].type=='N' #只对普通节点进行选举，即已经当选簇头的节点不进行再选举
            if Node[i].temp_rand <= (p/(1-p*(r%round(1/p)))): # 选取随机数小于等于阈值，则为簇头
                Node[i].type = 'C'       # 节点类型为蔟头
                Node[i].selected = 'O'   # 该节点标记'O'，说明当选过簇头
                Node[i].CH = -1
                # 广播自成为簇头
                distanceBroad = (xm * xm + ym * ym) ** 0.5
                if distanceBroad > d0:
                    Node[i].power = Node[i].power - (
                                Eelec * ctrPacketLength + Emp * ctrPacketLength * (distanceBroad ** 4))
                else:
                    Node[i].power = Node[i].power - (
                                Eelec * ctrPacketLength + Efs * ctrPacketLength * (distanceBroad ** 2))
            else:
                Node[i].type = 'N'  # 节点类型为普通
    # 判断最近的簇头结点，如何去判断，采用距离矩阵
    yy = np.zeros((n,n))
    Length = np.zeros((n,n))
    for i in range(n):
        if Node[i].type == 'N' and Node[i].flag != 0:
            for j in range(n):
                if Node[j].type == 'C' and Node[j].flag != 0:  # 计算普通节点到簇头的距离
                    Length[i, j] = ((Node[i].xd - Node[j].xd) ** 2 + (Node[i].yd - Node[j].yd) ** 2) ** 0.5
                else:
                    Length[i, j] = float('inf')
            dist, index = np.min(Length[i, :]), np.argmin(Length[i, :])  # 找到距离簇头最近的簇成员节点
            # 加入这个簇
            if Length[i, index] < d0:
                Node[i].power = Node[i].power - (
                            Eelec * ctrPacketLength + Efs * ctrPacketLength * (Length[i, index] ** 2))
            else:
                Node[i].power = Node[i].power - (
                            Eelec * ctrPacketLength + Emp * ctrPacketLength * (Length[i, index] ** 4))
            Node[i].CH = index
            # 接收簇头发来的广播的消耗
            Node[i].power = Node[i].power - Eelec * ctrPacketLength
            # 对应簇头接收确认加入的消息
            Node[index].power = Node[index].power - Eelec * ctrPacketLength
            yy[i, index] = 1
        else:
            Length[i, :] = float('inf')
    for i in range(n):
        if Node[i].flag != 0:
            if Node[i].type == 'C':
                number = np.sum(yy[:, i])      # 统计簇头节点i的成员数量
                # 簇头接收普通节点发来的数据
                Node[i].power = Node[i].power-(Eelec+ED)*packetLength
                # 簇头节点向基站发送数据
                len = ((Node[i].xd-sink.x)**2+(Node[i].yd-sink.y)**2)**0.5
                if len < d0:
                    Node[i].power = Node[i].power-((Eelec+ED)*packetLength+Efs*packetLength*(len**2))
                else:
                    Node[i].power = Node[i].power-((Eelec+ED)*packetLength+Emp*packetLength*len**4)
            else:
                # 普通节点向簇头发数据
                len = Length[i, Node[i].CH]
                if len < d0:
                    Node[i].power = Node[i].power - (Eelec * packetLength + Efs * packetLength * len ** 2)
                else:
                    Node[i].power = Node[i].power - (Eelec * packetLength + Emp * packetLength * len ** 4)
    for i in range(n):
        if Node[i].power < 0:
            Node[i].flag = 0
if f == 0:
    stop = rmax
## 绘图显示
fig4 = plt.figure(dpi=80)
plt.plot(range(rmax), alive_ima_leach, c='r',linewidth=2)
plt.plot(range(rmax), alive_leach, c='b', linewidth=2)
plt.legend(['IMP_LEACH', 'LEACH'])
plt.xlabel('轮数')
plt.ylabel('存活节点数')
fig5 = plt.figure(dpi=80)
plt.plot(range(rmax), re_ima_leach, c='r',linewidth=2)
plt.plot(range(rmax), re_leach, c='b', linewidth=2)
plt.legend(['IMP_LEACH', 'LEACH'])
plt.xlabel('轮数')
plt.ylabel('系统总能量')
fig6 = plt.figure(dpi=80)
for r in range(rmax):
    if alive_ima_leach[r] >= n:
        a1 = r
    if alive_leach[r] >= n:
        a2 = r
    if alive_ima_leach[r] >= (1-0.1)*n:
        b1 = r
    if alive_leach[r] >= (1-0.1)*n:
        b2 = r
    if alive_ima_leach[r] >= (1-0.2)*n:
        c1 = r
    if alive_leach[r] >= (1-0.2)*n:
        c2 = r
    if alive_ima_leach[r] >= (1-0.5)*n:
        d1 = r
    if alive_leach[r] >= (1-0.5)*n:
        d2 = r
    if alive_ima_leach[r] > 0:
        e1 = r
    if alive_leach[r] > 0:
        e2 = r
y=[[a1, a2],[b1, b2],[c1, c2],[d1, d2],[e1, e2]]
y=np.array(y)
x=np.arange(5)
width = 0.36
plt.bar(x-width/2,y[:,0],width=width)
plt.bar(x+width/2,y[:,1],width=width)
plt.xticks(range(5),['0', '10', '20', '50', '100'])
plt.legend(['IMP_LEACH', 'LEACH'])
plt.xlabel('死亡比例')
plt.ylabel('循环轮数')

plt.show()