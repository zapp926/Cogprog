%% clear the mark
clear all
clc
test1 = importdata('01_xlb.ev2');
[row1,col1] = size(test1);
test2 = csvread('01_xlb.csv',2,0);
[row2,col2] = size(test2);

for i = 1:row1;
    for j = 1:row2;
    if test2(j,2) <= 3 && test1(i,2) == test2(j,1)
       test1(i,2)=200
    elseif test2(j,2) >= 7 && test1(i,2) == test2(j,1)
        test1(i,2)=201
    %elseif j+3>row2
     %   break 
    end
   end
end

fileID=fopen('01_xlb.ev2','w');
for i=1:row1;
 fprintf(fileID,'%3d     %3d  %1d    %1d   %6.4f %6d \r\n',test1(i,1),test1(i,2),test1(i,3),test1(i,4),test1(i,5),test1(i,6));
end


