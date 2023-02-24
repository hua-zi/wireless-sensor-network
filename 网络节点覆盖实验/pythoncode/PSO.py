import numpy as np
import matplotlib.pyplot as plt
import random

# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# input：(x,y)圆心坐标，L区域边长，R通信半径，data离散粒度
# output：scale覆盖率
def fun(x,y,L,R,data):
    N = len(x)
    n = np.arange(0,L,data)
    m = np.arange(0,L,data)
    row = n.shape[0]
    col = m.shape[0]
    flag = np.zeros(row*col)
    m, n = np.meshgrid(m, n)  # x,y分别为坐标的横纵坐标，都是二维数组
    m = m.flatten()           # 变成一维
    n = n.flatten()

    for i in range(N):
        D = ((m-x[i])**2+(n-y[i])**2)**0.5
        D = D<=R
        flag = np.maximum(flag, D)
    scale = np.sum(flag)/(row*col)
    return scale

if __name__ == '__main__':
    # 网络参数
    L = 50          # 区域边长
    n = 35          # 节点个数
    R = 5           # 通信半径
    data = 1        # 离散粒度
    # 粒子群参数
    maxgen = 2000    # 迭代次数
    sizepop = 20     # 粒子规模
    Wmax = 0.9
    Wmin = 0.4
    # 参数初始化
    c1 = 2          # 自我认知参数
    c2 = 2          # 社会认知参数
    Vmax = 2        # 最大速度
    Vmin = -2       # 最小速度
    popmax = 50     # 位置最大值
    popmin = 0      # 位置最小值
    gbest = np.zeros((n,2))  # 最优解
    # 随机生成群体位置、速度和对应的适应度值
    nodes_position = []
    nodes_v = []
    fitness = []
    for i in range(sizepop):
        position = np.random.uniform(0, L, (2, n)) # 初始化种群位置
        v = np.random.uniform(0, 2, (2, n))        # 初始化速度
        nodes_position.append(position)
        nodes_v.append(v)
        # print(position[0])
        fit = fun(position[0],position[1],L,R,data)
        fitness.append(fit)
    # print(fitness)
    fitness = np.array(fitness)
    bestfitness, bestindex = np.max(fitness),np.argmax(fitness)
    gbest = nodes_position[bestindex]   # 群体最优极值
    pbest_position = nodes_position
    pbest_v = nodes_v
    fitnessgbest = bestfitness          # 种群最优适应度值
    fitnesspbest = fitness              # 个体最优适应度值

    # 初始结果显示
    # 设置图像大小，格式
    fig1 = plt.figure(dpi=80)
    plt.grid(linestyle="dotted")
    axes = plt.gca()
    axes.set_aspect(1)
    # 设置坐标范围
    plt.xlim(0, L)
    plt.ylim(0, L)
    for i in range(n):
        x = gbest[0,i]
        y = gbest[1,i]
        draw_circle = plt.Circle((x, y), R, fill=True, color="yellow")
        plt.gcf().gca().add_artist(draw_circle)
    plt.title('初始图像，覆盖率'+str(fitnessgbest))
    plt.scatter(gbest[0,:],gbest[1,:],c='r',linewidths=0.1,zorder=2)

    # 迭代寻优
    zz = np.zeros(maxgen)
    for i in range(maxgen):
        W = Wmax - ((Wmax - Wmin) / maxgen) * i
        for j in range(sizepop):
            # 速度更新
            nodes_v[j]= W * nodes_v[j] + c1 * random.random() * (pbest_position[j] - nodes_position[j]) + c2 * random.random() * (gbest - nodes_position[j])
            # 边界处理
            nodes_v[j] = np.maximum(nodes_v[j], Vmin)
            nodes_v[j] = np.minimum(nodes_v[j], Vmax)
            # 位置更新
            nodes_position[j] = nodes_position[j] + nodes_v[j]
            # 边界处理
            nodes_position[j] = np.maximum(nodes_position[j], popmin)
            nodes_position[j] = np.minimum(nodes_position[j], popmax)
            # 适应度值更新
            fitness[j] = fun(nodes_position[j][0], nodes_position[j][1], L, R, data)

        # 个体和群体极值更新
        for j in range(sizepop):
            # 个体极值更新
            if fitness[j] > fitnesspbest[j]:
                pbest_position[j] = nodes_position[j]
                fitnesspbest[j] = fitness[j]
            # 群体极值更新
            if fitness[j] > fitnessgbest:
                gbest = nodes_position[j]
                fitnessgbest = fitness[j]
        # 每一代群体最优值存入zz数组
        zz[i] = fitnessgbest
    # 结果显示
    fig2 = plt.figure(dpi=80)
    plt.grid(linestyle="dotted")
    axes = plt.gca()
    # print(np.array(zz))
    plt.plot(np.arange(maxgen),np.array(zz))
    plt.title('训练过程')
    plt.xlabel('迭代次数',fontdict={"size": 10})
    plt.ylabel('覆盖率', fontdict={"size": 10})
    # 最终结果显示
    # 设置图像大小，格式
    fig3 = plt.figure(dpi=80)
    plt.grid(linestyle="dotted")
    axes = plt.gca()
    axes.set_aspect(1)
    # 设置坐标范围
    plt.xlim(0, L)
    plt.ylim(0, L)
    for i in range(n):
        x = gbest[0, i]
        y = gbest[1, i]
        draw_circle = plt.Circle((x, y), R, fill=True, color="green")
        plt.gcf().gca().add_artist(draw_circle)
    plt.title('最终图像，覆盖率' + str(fitnessgbest))
    plt.scatter(gbest[0, :], gbest[1, :], c='r',linewidths=0.1, zorder=2)

    plt.show()
