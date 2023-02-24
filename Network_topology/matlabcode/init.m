%% 清空环境变量
clc;
clear;
close all;

%% 设置参数
n = 15;
xlim = 100;
ylim = 100;

%% 生成网络节点
r = randi([0,xlim],[2,n]);
x = r(1,:);
y = r(2,:);
save data