%% 清空环境变量
clc;
clear;
close all;

%% 读取数据
r=load('data.mat');
x = r.x;
y = r.y;

%% 绘制星型拓扑结构
figure
axis([0 r.xlim 0 r.ylim]);
% 绘制网络节点
scatter(x,y);
hold on

% 生成中心节点
x_z = mean(x(:));
y_z = mean(y(:));
plot(x_z,y_z,'ko','Markerface','r','MarkerSize',10);
hold on

% 网络节点接入
for i=1:r.n
    line([x_z,x(i)],[y_z,y(i)]);
end





