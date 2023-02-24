fileID = fopen('input_network.txt','r');
formatSpec = '%f';
Input = fscanf(fileID,formatSpec); % Input about relevant info read % 
fclose(fileID);

N = Input(1); % get number of nodes *
Packet_size = Input(2) * 8; % get the packet size in bits % 
T = Input(3) * 10^-3; % get simulation time in s %
Backoff_St = Input(4); %退避策略 get the random backoff strategy %

if Backoff_St == 1 
% Strategy 1 %
    total_time = 0;
    count = 0;
    good_time = 0;
    data_rate = 6 * 10^6; % 6 Mbps %
    packet_time = Packet_size / data_rate; % get packet time %
    slot_size = 9 * (10^-6); % 9 us %
    j = 1;
    simulation_count = 0;
    CW_min = 15; % 竞争窗口，节点随机回退计数值的范围
    CW = 15;
    collision_flag = 0;
    r = (randi([0,CW_min],N,1)) * 10^-6; % generate N random numbers and put them into an array %
   
    while total_time < T
        
        [M,I] = min(r); % find the node with the minimum counter and index of node %
        simulation_count = simulation_count + 1;
        
        for i = 1:N   % check if there are more than one nodes with same minimum counter %
            if (M == r(i))
                count = count + 1;
                collision_index(j) = i;
                j = j + 1;
            end
        end
        
        if count > 1
            collision_flag = 1; % collision occured %
        end
        
        if collision_flag ~= 1 % if no collision, increase good time %
            good_time = good_time + packet_time; % 记录无碰撞时间
            CW = CW_min;
            r(I) = (randi([0,CW],1,1)) * 10^-6;
        else
            CW = CW * 2;
            for i = 1:N
                if (M == r(i)) % for all nodes that collided, choose new rand %
                    r(i) = (randi([0,CW],1,1)) * 10^-6;
                end
            end
        end
        
        total_time = total_time + packet_time;
        
        for i = 1:N
            for j = 1:size(collision_index)
                if(i ~= collision_index(j))
                    r(i) = r(i) - slot_size;
                end
            end
        end
        count = 0;
        collision_flag = 0;
    end
    
    utility = good_time / total_time; % 利用率
end

if Backoff_St == 2
  % Strategy 2 %
    total_time = 0;
    count = 0;  % 节点具有相同的最小计数器 数量
    good_time = 0;
    data_rate = 6 * 10^6; % 6 Mbps %
    packet_time = Packet_size / data_rate; % get packet time %
    slot_size = 9 * (10^-6); % 9 us %
    j = 1;
    simulation_count = 0;
    CW_min = 15;
    CW = 15;
    collision_flag = 0;
    r = (randi([0,CW_min],N,1)) * 10^-6; % 生成N个随机数并将其放入数组generate N random numbers and put them into an array %
   
    while total_time < T
        
        [M,I] = min(r); %查找具有最小计数器和节点索引的节点 find the node with the minimum counter and index of node %
        simulation_count = simulation_count + 1;
        
        for i = 1:N   % 检查是否有多个节点具有相同的最小计数器check if there are more than one nodes with same minimum counter %
            if (M == r(i))
                count = count + 1;
                collision_index(j) = i;% 记录产生碰撞的节点
                j = j + 1;
            end
        end
        
        if count > 1
            collision_flag = 1; % collision occured %
        end
        
        if collision_flag ~= 1
            good_time = good_time + packet_time;
            CW = round(CW,2); 
            r(I) = (randi([0,CW],1,1)) * 10^-6; % 重置等待时间
        else
            CW = CW + 2;
            for i = 1:N
                if (M == r(i))
                    r(i) = (randi([0,CW],1,1)) * 10^-6;% 重置等待时间
                end
            end
        end
        
        total_time = total_time + packet_time; 
        for i = 1:N
            for j = 1:size(collision_index)
                if(i ~= collision_index(j))
                    r(i) = r(i) - slot_size; % 等待时间减去一个时隙
                end
            end
        end
        count = 0;
        collision_flag = 0;
    end
    
    utility = good_time / total_time;
end


if Backoff_St == 3
   % Strategy 3 %
    total_time = 0;
    count = 0;
    good_time = 0;
    data_rate = 6 * 10^6; % 6 Mbps %
    packet_time = Packet_size / data_rate; % get packet time %
    slot_size = 9 * (10^-6); % 9 us %
    j = 1;
    simulation_count = 0;
    CW_min = 15;
    CW = 15;
    collision_flag = 0;
    r = (randi([0,CW_min],N,1)) * 10^-6; % generate N random numbers and put them into an array %
   
    while total_time < T
        
        [M,I] = min(r); % find the node with the minimum counter and index of node %
        simulation_count = simulation_count + 1;
        
        for i = 1:N   % check if there are more than one nodes with same minimum counter %
            if (M == r(i))
                count = count + 1;
                collision_index(j) = i;
                j = j + 1;
            end
        end
        
        if count > 1
            collision_flag = 1; % collision occured %
        end
        
        if collision_flag ~= 1
            good_time = good_time + packet_time;
            CW = round(CW,2);
            r(I) = (randi([0,CW],1,1)) * 10^-6;
        else
            CW = CW * 2;
            for i = 1:N
                if (M == r(i))
                    r(i) = (randi([0,CW],1,1)) * 10^-6;
                end
            end
        end
        
        total_time = total_time + packet_time;
        for i = 1:N
            for j = 1:size(collision_index)
                if(i ~= collision_index(j))
                    r(i) = r(i) - slot_size;
                end
            end
        end
        count = 0;
        collision_flag = 0;
    end
    
    utility = good_time / total_time;
end

if Backoff_St == 4
% Strategy 4 %
    total_time = 0;
    count = 0;
    good_time = 0;
    data_rate = 6 * 10^6; % 6 Mbps %
    packet_time = Packet_size / data_rate; % get packet time %
    slot_size = 9 * (10^-6); % 9 us %
    j = 1;
    simulation_count = 0;
    CW_min = 15;
    CW = 15;
    collision_flag = 0;
    r = (randi([0,CW_min],N,1)) * 10^-6; % generate N random numbers and put them into an array %
   
    while total_time < T
        
        [M,I] = min(r); % find the node with the minimum counter and index of node %
        simulation_count = simulation_count + 1;
        
        for i = 1:N   % check if there are more than one nodes with same minimum counter %
            if (M == r(i))
                count = count + 1;
                collision_index(j) = i;
                j = j + 1;
            end
        end
        
        if count > 1
            collision_flag = 1; % collision occured %
        end
        
        if collision_flag ~= 1
            good_time = good_time + packet_time;
            CW = CW - 2;
            if CW < 1
                CW = 2;
            end
            r(I) = (randi([0,CW],1,1)) * 10^-6;
        else
            CW = CW + 2;
            for i = 1:N
                if (M == r(i))
                    r(i) = (randi([0,CW],1,1)) * 10^-6;
                end
            end
        end
        
        total_time = total_time + packet_time;
        for i = 1:N
            for j = 1:size(collision_index)
                if(i ~= collision_index(j))
                    r(i) = r(i) - slot_size;
                end
            end
        end
        count = 0;
        collision_flag = 0;
    end
    
    utility = good_time / total_time;
end

if Backoff_St == 5
    % strategy 5 %
    total_time = 0;
    count = 0;
    good_time = 0;
    data_rate = 6 * 10^6; % 6 Mbps %
    packet_time = Packet_size / data_rate; % get packet time %
    slot_size = 9 * (10^-6); % 9 us %
    j = 1;
    simulation_count = 0;
    CW_min = 15;
    CW = 15;
    collision_flag = 0;
    r = (randi([0,CW_min],N,1)) * 10^-6; % generate N random numbers and put them into an array %
   
    while total_time < T
        
        [M,I] = min(r); % find the node with the minimum counter and index of node %
        simulation_count = simulation_count + 1;
        
        for i = 1:N   % check if there are more than one nodes with same minimum counter %
            if (M == r(i))
                count = count + 1;
                collision_index(j) = i;
                j = j + 1;
            end
        end
        
        if count > 1
            collision_flag = 1; % collision occured %
        end
        
        if collision_flag ~= 1
            good_time = good_time + packet_time;
            CW = CW - 2;
            if CW < 1
                CW = 2;
            end
            r(I) = (randi([0,CW],1,1)) * 10^-6;
        else
            CW = CW * 2;
            for i = 1:N
                if (M == r(i))
                    r(i) = (randi([0,CW],1,1)) * 10^-6;
                end
            end
        end
        
        total_time = total_time + packet_time;
        for i = 1:N
            for j = 1:size(collision_index)
                if(i ~= collision_index(j))
                    r(i) = r(i) - slot_size;
                end
            end
        end
        count = 0;
        collision_flag = 0;
    end
    
    utility = good_time / total_time;
end


fprintf('Number of Nodes: %d ; Packet Size: %d ; Simulation Time(s): %d ; Backoff Strategy: %d \n Utilization: ', N, Input(2), T, Backoff_St);
disp(utility);

