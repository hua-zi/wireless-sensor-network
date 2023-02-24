function [matrix_UE_BS] = Model_Init(BS_lambda, UE_lambda, R)
clc;close all;
%INPUT: lambda of BS and UEs, the range of BS station
%OUTPUT: the map of UE and its corresponding BS.The first column is the closest BS index, the second column
% is the distance from UE to the closest BS, the third column is the service BS of UE.If the value in the third
%column is 0, that means there is no BS could provide service for UE.
%according to lambda, assign the position of BS and UE.

[BS_pos, BS_num]=poisson2d(BS_lambda);
[UE_pos, UE_num]=poisson2d(UE_lambda);
plot(BS_pos(:, 1), BS_pos(:, 2), 'pr');
hold on;
plot(UE_pos(:, 1), UE_pos(:, 2), '.b');
%compute the distance from BS to every UE
dist = zeros(UE_num,BS_num);
for i= 1:BS_num
    ith_BS_pos=repmat(BS_pos(i,:),UE_num,1);
    d=ith_BS_pos-UE_pos;
    dist(:,i)=sqrt(sum(d.^2,2));
end

%find the minumum distance
[min_dist,index]=min(dist');
%R is the range of BS service. According to the thersold of R,judge UE is in service or not.
matrix_UE_BS=zeros(UE_num,3);
matrix_UE_BS(:,1)=index';
matrix_UE_BS(:,2)=min_dist';
matrix_UE_BS(:,3)=index'.*(R>min_dist');
end


