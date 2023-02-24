# 对于2D和3D的Rssi定位算法，画出误差随锚节点数的变化趋势
import random
import math
import numpy as np
import matplotlib.pyplot as plt

import RSSI_2Ds
import RSSI_3Ds

if __name__ == '__main__':
    x = []
    y_2d = []
    y_3d = []
    for i in range(6, 50):
        sum_2d = 0
        sum_3d = 0
        for j in range(10):
            sum_2d += RSSI_2Ds.forecast_2d(i)
            sum_3d += RSSI_3Ds.forecast_3d(i)
        sum_2d /= 10
        sum_3d /= 10
        x.append(i)
        y_2d.append(sum_2d)
        y_3d.append(sum_3d)

    fig1 = plt.figure(dpi=80)
    plt.grid(linestyle="dotted")
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x, y_2d)
    plt.plot(x, y_3d)

    plt.xlabel('锚节点数', fontdict={"size": 15})
    plt.ylabel('误差/m', fontdict={"size": 15})
    plt.tick_params(labelsize=13)
    plt.legend(['2D','3D'],prop={"size": 15})
    plt.title('二维和三维的RSSI定位对比',fontdict={"size": 15})

    plt.show()
