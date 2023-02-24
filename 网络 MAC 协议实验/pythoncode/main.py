import matplotlib.pyplot as plt
import numpy as np
import random

N = 100 # 节点个数
Packet_size = 2000*8 # 包的大小
T = 1000*10**(-3)  # 仿真时间 s
Backoff_St = 5 #退避策略

fig = plt.figure(dpi=80)
plt.grid(linestyle="dotted")
# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.xlabel('节点数(N)', fontdict={"size": 10})
plt.ylabel('网络利用率', fontdict={"size": 10})
plt.title('CSMA/CA with Random Backoff (Packet Size: 2000)')

x = []
utility = []
for i in range(5):
    utility.append([])

for N in range(1,201):
    x.append(N)
    for Backoff_St_i in range(5):
        Backoff_St = Backoff_St_i+1

        if Backoff_St == 1:
            #  Strategy 1 #
            total_time = 0
            count = 0
            good_time = 0
            data_rate = 6 * 10 ** 6  #  6 Mbps #
            packet_time = Packet_size / data_rate
            slot_size = 9 * (10 ** (-6))   # 9us  #
            j = 1
            simulation_count = 0
            CW_min = 15
            CW = 15
            collision_flag = 0
            r = (np.random.randint(0, CW_min, N)) * 10 ** (-6)  # 生成N个随机数并将其放入数组

            while total_time < T:

                M, I = np.min(r), np.argmin(r)  # 查找具有最小计数器和节点索引的节点
                simulation_count = simulation_count + 1

                collision_index = []
                collision_flag = 0
                for i in range(N):  # 检查是否有多个节点具有相同的最小计数器
                    if (M == r[i]):
                        count = count + 1
                        collision_index.append(i)  # 记录产生碰撞的节点
                        j = j + 1

                if count > 1:
                    collision_flag = 1  # 碰撞检测


                if collision_flag != 1:  # if no collision, increase good time  #
                    good_time = good_time + packet_time   # 记录无碰撞时间
                    CW = CW_min   #***
                    r[I] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间
                else:
                    CW = CW * 2   #***
                    for i in range(N):
                        if (M == r[i]):  # for all nodes that collided, choose new rand  #
                            r[i] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间

                total_time = total_time + packet_time

                for i in range(N):
                    for j in range(len(collision_index)):
                        if (i != collision_index[j]):
                            r[i] = r[i] - slot_size  # 等待时间减去一个时隙

                count = 0
                collision_flag = 0

            utility1 = good_time / total_time   # 利用率
            utility[Backoff_St-1].append(utility1)
            # print(utility1)

        if Backoff_St == 2:
          # Strategy 2 #
            total_time = 0
            count = 0   # 节点具有相同的最小计数器 数量
            good_time = 0
            data_rate = 6 * 10**6  # 6 Mbps #
            packet_time = Packet_size / data_rate  # get packet time #
            slot_size = 9 * (10**(-6))  # 9 us #
            j = 1
            simulation_count = 0
            CW_min = 15
            CW = 15
            collision_flag = 0
            r = (np.random.randint(0,CW_min,N)) * 10**(-6)  # 生成N个随机数并将其放入数组generate N random numbers and put them into an array #

            while total_time < T:

                M, I = np.min(r),np.argmin(r)  # 查找具有最小计数器和节点索引的节点
                simulation_count = simulation_count + 1

                collision_index=[]
                collision_flag=0
                for i in range(N):  # 检查是否有多个节点具有相同的最小计数器
                    if (M == r[i]):
                        count = count + 1
                        collision_index.append(i)   # 记录产生碰撞的节点
                        j = j + 1

                if count > 1:
                    collision_flag = 1  # 碰撞检测

                if collision_flag != 1:
                    good_time = good_time + packet_time
                    CW = round(CW, 2)   # 小数点往前提2位
                    CW = int(CW/2)     # ***
                    if CW < 1:
                        CW = 2
                    r[I] = (random.randint(0, CW)) * 10 ** (-6)   # 重置等待时间
                else:
                    CW = CW + 2
                    for i in range(N):
                        if (M == r[i]):
                            r[i] = (random.randint(0, CW)) * 10 ** (-6)   # 重置等待时间

                total_time = total_time + packet_time
                for i in range(N):
                    for j in range(len(collision_index)):
                        if (i != collision_index[j]):
                            r[i] = r[i] - slot_size   # 等待时间减去一个时隙
                count = 0
                collision_flag = 0

            utility2 = good_time / total_time
            # print(utility2)
            utility[Backoff_St-1].append(utility2)

        if Backoff_St == 3:
            # Strategy 3 #
            total_time = 0
            count = 0
            good_time = 0
            data_rate = 6 * 10 ** 6  # 6 Mbps #
            packet_time = Packet_size / data_rate
            slot_size = 9 * (10 ** (-6))  # 9us #
            j = 1
            simulation_count = 0
            CW_min = 15
            CW = 15
            collision_flag = 0
            r = (np.random.randint(0, CW_min, N)) * 10 ** (-6)  # 生成N个随机数并将其放入数组

            while total_time < T:

                M, I = np.min(r), np.argmin(r)  # 查找具有最小计数器和节点索引的节点
                simulation_count = simulation_count + 1

                collision_index = []
                collision_flag = 0
                for i in range(N):  # 检查是否有多个节点具有相同的最小计数器
                    if (M == r[i]):
                        count = count + 1
                        collision_index.append(i)  # 记录产生碰撞的节点
                        j = j + 1

                if count > 1:
                    collision_flag = 1  # 碰撞检测

                if collision_flag != 1:
                    good_time = good_time + packet_time
                    CW = round(CW, 2)  # 四舍五入保留两位小数
                    # CW = int(CW / 2)  # ***
                    # if CW < 1:
                    #     CW = 2
                    r[I] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间
                else:
                    CW = CW * 2
                    for i in range(N):
                        if (M == r[i]):
                            r[i] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间

                total_time = total_time + packet_time
                for i in range(N):
                    for j in range(len(collision_index)):
                        if (i != collision_index[j]):
                            r[i] = r[i] - slot_size  # 等待时间减去一个时隙
                count = 0
                collision_flag = 0

            utility3 = good_time / total_time
            # print(utility3)
            utility[Backoff_St-1].append(utility3)

        if Backoff_St == 4:
            # Strategy 4 #
            total_time = 0
            count = 0  # 节点具有相同的最小计数器 数量
            good_time = 0
            data_rate = 6 * 10 ** 6  # 6 Mbps #
            packet_time = Packet_size / data_rate  # get packet time #
            slot_size = 9 * (10 ** (-6))  # 9 us #
            j = 1
            simulation_count = 0
            CW_min = 15
            CW = 15
            collision_flag = 0
            r = (np.random.randint(0, CW_min, N)) * 10 ** (-6)  # 生成N个随机数并将其放入数组generate N random numbers and put them into an array #

            while total_time < T:

                M, I = np.min(r), np.argmin(r)  # 查找具有最小计数器和节点索引的节点
                simulation_count = simulation_count + 1

                collision_index = []
                collision_flag = 0
                for i in range(N):  # 检查是否有多个节点具有相同的最小计数器
                    if (M == r[i]):
                        count = count + 1
                        collision_index.append(i)  # 记录产生碰撞的节点
                        j = j + 1

                if count > 1:
                    collision_flag = 1  # 碰撞检测

                if collision_flag != 1:
                    good_time = good_time + packet_time
                    CW = CW -2  # 小数点往前提2位
                    if CW<1:
                        CW = 2
                    r[I] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间
                else:
                    CW = CW + 2
                    for i in range(N):
                        if (M == r[i]):
                            r[i] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间

                total_time = total_time + packet_time
                for i in range(N):
                    for j in range(len(collision_index)):
                        if (i != collision_index[j]):
                            r[i] = r[i] - slot_size  # 等待时间减去一个时隙
                count = 0
                collision_flag = 0

            utility4 = good_time / total_time
            # print(utility4)
            utility[Backoff_St - 1].append(utility4)

        if Backoff_St == 5:
            # Strategy 5 #
            total_time = 0
            count = 0  # 节点具有相同的最小计数器 数量
            good_time = 0
            data_rate = 6 * 10 ** 6  # 6 Mbps #
            packet_time = Packet_size / data_rate  # get packet time #
            slot_size = 9 * (10 ** (-6))  # 9 us #
            j = 1
            simulation_count = 0
            CW_min = 15
            CW = 15
            collision_flag = 0
            r = (np.random.randint(0, CW_min, N)) * 10 ** (-6)  # 生成N个随机数并将其放入数组generate N random numbers and put them into an array #

            while total_time < T:

                M, I = np.min(r), np.argmin(r)  # 查找具有最小计数器和节点索引的节点
                simulation_count = simulation_count + 1

                collision_index = []
                collision_flag = 0
                for i in range(N):  # 检查是否有多个节点具有相同的最小计数器
                    if (M == r[i]):
                        count = count + 1
                        collision_index.append(i)  # 记录产生碰撞的节点
                        j = j + 1

                if count > 1:
                    collision_flag = 1  # 碰撞检测

                if collision_flag != 1:
                    good_time = good_time + packet_time
                    CW = CW - 2  # 小数点往前提2位
                    if CW<1:
                        CW = 2
                    r[I] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间
                else:
                    CW = CW * 2
                    for i in range(N):
                        if (M == r[i]):
                            r[i] = (random.randint(0, CW)) * 10 ** (-6)  # 重置等待时间

                total_time = total_time + packet_time
                for i in range(N):
                    for j in range(len(collision_index)):
                        if (i != collision_index[j]):
                            r[i] = r[i] - slot_size  # 等待时间减去一个时隙
                count = 0
                collision_flag = 0

            utility5 = good_time / total_time
            # print(utility5)
            utility[Backoff_St - 1].append(utility5)

print(len(x))

for i in range(5):
    label = 'Strategy '+str(i+1)
    plt.plot(x,utility[i],label=label)
plt.legend()  # 绘制图例
plt.show()