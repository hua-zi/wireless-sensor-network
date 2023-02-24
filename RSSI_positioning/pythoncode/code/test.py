# import matplotlib.pyplot as plt          #导入库
# from mpl_toolkits.mplot3d import Axes3D  #导入库
#
# plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
# plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
#
# ax = plt.subplot(projection='3d')              #设置3D绘图空间
# x = [0, 0, 1, 4, 5]                       #设置x轴坐标
# y = [1, 1, 1, 1, 2]                       #设置y轴坐标
# z = [2, 0, 3, 4, 5]                       #设置z轴坐标
# plt.plot(x, y, z)                         #绘制5个点对应连线的三维线性图
# ax.scatter(x, y, z,linewidths=10)
# # plt.scatter(1, 1, 1,c='b')
# plt.xlabel('x轴')                         #给横轴命名
# plt.ylabel('y轴')                         #给纵轴命名
# plt.title('三维线图')                     #添加标题
# plt.show()

def sayhello():
    print('hello')