clear all
clc
dir = 'D:\Matlab_x64\toolbox\eye_tracker\eye_data\try-zapp'
cd 'D:\Matlab_x64\toolbox\eye_tracker\eye_data\try-zapp'
for list_i=1:4;
 
data =[sprintf('%s%d%s','data_block',list_i),'.csv'];
test1 = csvread(data,5,0);
[row1,col1] = size(test1);

test2 = csvread('02_lym.csv',2,0);
[row2,col2] = size(test2);

 for j = 0:49;
    for i = 1: row1-49;
        if test1(row1-49 + j,1) < test1(i,1) && test1(i,1) < test1(row1-49 + j,1) + 2000;
            test1(i,16) = test1(row1-49 + j,15);
        end
     end
 end

for j = 1:row2;
    for i = 1: row1-49;
        if test2(j,3) <= 4 && test1(i,16) == test2(j,1);
        test1(i,16)=201;
        elseif test2(j,3) >= 6 && test1(i,16) == test2(j,1);
        test1(i,16)=202;
        end
    end
        
end

%%

trial = test1;
trial(trial(:,4)<=0,:)=[];
i_pupil=[];
%ipupils =  trial(:,16);
for i=1:length(trial);

Lpupil=trial(:,4);
Lpupil_mean=mean(Lpupil);
Lpupil_deviate_from_mean=mean(abs(Lpupil(i)-Lpupil_mean));
   
i_pupil = [ i_pupil;Lpupil_deviate_from_mean ];

end

i_pupil(:,2)= trial(:,16);
dir = 'D:\Matlab_x64\toolbox\eye_tracker\eye_data\try-zapp'
save(['i_pupil' num2str(list_i)],'i_pupil');

end

pup_end = []
for pup_i = 1:4;
    load([sprintf('%s%d%s','i_pupil',pup_i),'.mat']);
    pup_end = [ pup_end;i_pupil];
end

for pup_all_i = 1:length(pup_end);
    
    if pup_end(pup_all_i,2) ~= 201 && pup_end(pup_all_i,2) ~= 202;
         pup_end(pup_all_i,1) = 0;
    end
end
pup_end(pup_end(:,1)<=0,:)=[];
  
for pup_end_i = 1:length(pup_end);
    if pup_end(pup_end_i,2) == 201;
         data_201 = mean(pup_end(pup_end_i,1));
    elseif pup_end(pup_end_i,2) == 202;
         data_202 = mean(pup_end(pup_end_i,1));
    end
end

 