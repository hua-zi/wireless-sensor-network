%% 清空环境变量
clc;
clear;
close all;

%% 读取数据
r=load('data.mat');
x = r.x;
y = r.y;

%% 绘制总线型拓扑结构
figure
axis([0 r.xlim 0 r.ylim]);
% 绘制网络节点
scatter(x,y);
hold on
% 绘制总线
line([0,r.xlim],[r.ylim/2,r.ylim/2]);
hold on

% 网络节点接入
for i=1:r.n
    line([x(i),x(i)],[r.ylim/2,y(i)]);
end
