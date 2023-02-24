%% 清空环境变量
clc;
clear;
close all;

%% 读取数据
r=load('data.mat');
x = r.x;
y = r.y;

%% 绘制环型拓扑结构
figure
axis([0 r.xlim 0 r.ylim]);
% 绘制网络节点
scatter(x,y);
hold on
% 成环
Point = [x;y];
d = [x-mean(x);y-mean(y)]; %各点到中点的连线
angle = atan2(d(2,:),d(1,:)); % 各点中点连线与x轴角度
% 按角度排序
[angle, i] = sort(angle);   
Point = Point(:,i); 
Point = [Point Point(:,1)]; %加入起点到最末，形成闭合图形
plot( Point(1,:), Point(2,:), '*-b');
