%% 清空环境变量
clc;
clear;
close all;

%% 读取数据
r=load('data.mat');
x = r.x;
y = r.y;
k=4;     %聚类数
% k=r.n;

%% 绘制树型拓扑结构
figure
axis([0 r.xlim 0 r.ylim]);
% 绘制网络节点
scatter(x,y);
hold on
% 聚类
p=[x;y];
p=p';
[idx,c]=kmeans(p,k);
% 画聚类中心
c=c';
p=p';
scatter(c(1,:),c(2,:));
hold on
% 聚类中心相连
x_z = mean(x(:));
y_z = mean(y(:));
plot(x_z,y_z,'ko','Markerface','r','MarkerSize',10);
hold on
for i=1:k
    line([x_z,c(1,i)],[y_z,c(2,i)]);
end
hold on

% 网络节点接入
for i=1:r.n
    line([c(1,idx(i)),p(1,i)],[c(2,idx(i)),p(2,i)]);
end
hold on
    

