%% startup

softwarefolder='D:\Matlab_x64\toolbox\fieldtrip-20170628';
addpath(softwarefolder)
ft_defaults;
cd 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
clc;
clear all;

%% step1 input data

dir = 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
nsubjects = [1:19];
for j=1:length (nsubjects) 
    i=nsubjects(j);
    cfg = [];
        cfg.dataset=['sub' num2str(i) '.eeg']; %the file name
        cfg= ft_definetrial(cfg);
        cfg.continuous='no';
        cfg.channel      = 'all';
        data_pre = ft_preprocessing(cfg);
        
        outfil = fullfile(dir,strcat('data_pre_sub', sprintf('%02d', i)));
        save(outfil, 'data_pre');
end

%% step2 

dir = 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
nsubjects = [1:19];
for j=1:length (nsubjects)    
    i=nsubjects(1,j);
    load (fullfile(dir,strcat('data_pre_sub',sprintf('%02d', i))));
    
   % TFR hanning taper, fixed time window, for the low frequency band (2-30Hz)
    cfg              = [];
    cfg.output       = 'pow';
    cfg.channel      = {'all','-HEO','-VEO','-REF','-GFP','-M1','-M2'};
    cfg.method       = 'mtmconvol';
    cfg.taper        = 'hanning';
    cfg.foi          = 3:1:30;                         % analysis 2 to 30 Hz in steps of 2 Hz 
    cfg.t_ftimwin    = ones(length(cfg.foi),1).*0.7;   % length of time window = 0.5 sec
    cfg.toi          = -0.5:0.05:1.1;                  % time window "slides" from -0.7 to 1.7 sec in steps of 0.05 sec (50 ms)

    cfg.trials = find(data_pre.trialinfo(:,1) == 246);
    condition_246 = ft_freqanalysis(cfg, data_pre);

    cfg.trials = find(data_pre.trialinfo(:,1) == 247);
    condition_247 = ft_freqanalysis(cfg, data_pre);

    cfg.trials = find(data_pre.trialinfo(:,1) == 248);
    condition_248 = ft_freqanalysis(cfg, data_pre);

    outfil = fullfile(dir,strcat('data_condition_sub', sprintf('%02d', i)));
    save(outfil, 'condition_246','condition_247','condition_248');
end
%% Baseline correction

clear;
dir = 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
nsubjects = [1:19];
for j=1:length (nsubjects)    
    i=nsubjects(1,j);
    load(fullfile(dir,strcat('data_condition_sub', sprintf('%02d', i))));
    cfg.baseline = [-0.6 -0.2];
    cfg.baselinetype = 'db';
    Baseline_246 = ft_freqbaseline(cfg, condition_246);
    Baseline_247 = ft_freqbaseline(cfg, condition_247);
    Baseline_248 = ft_freqbaseline(cfg, condition_248);
    outfil = fullfile(dir,strcat('TFRbase_sub', sprintf('%02d', i)));
    save(outfil, 'Baseline_246','Baseline_247','Baseline_248');
end
%% step3 grand average with non-keepindividual
clear all
dir = 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
nsubjects = [1:19];
for j=1:length (nsubjects)
    i=nsubjects(1,j);
    
    load(fullfile(dir,strcat('TFRbase_sub', sprintf('%02d', i))));
    sub_1(j).condition = Baseline_246;
    sub_2(j).condition = Baseline_247;
    sub_3(j).condition = Baseline_248;
    
end
cfg = [];
cfg.keepindividual = 'no';
grandTFRbase_246 = ft_freqgrandaverage(cfg, sub_1(:).condition);
grandTFRbase_247 = ft_freqgrandaverage(cfg, sub_2(:).condition);
grandTFRbase_248 = ft_freqgrandaverage(cfg, sub_3(:).condition);

outfil = fullfile(dir,strcat('grandTFRbase_non_ki'));
save(outfil, 'grandTFRbase_246', 'grandTFRbase_247','grandTFRbase_248');

%% step4 grand average with keepindividual

clear all
dir = 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
nsubjects = [1:19];
for j=1:length (nsubjects)
    i=nsubjects(1,j);
   
    load(fullfile(dir,strcat('TFRbase_sub', sprintf('%02d', i))));
    sub_1(j).condition = Baseline_246;
    sub_2(j).condition = Baseline_247;
    sub_3(j).condition = Baseline_248;
    
end
cfg = [];
cfg.keepindividual = 'yes';
grandTFRbase_246 = ft_freqgrandaverage(cfg, sub_1(:).condition);
grandTFRbase_247 = ft_freqgrandaverage(cfg, sub_2(:).condition);
grandTFRbase_248 = ft_freqgrandaverage(cfg, sub_3(:).condition);

outfil = fullfile(dir,strcat('grandTFRbase_ki'));
save(outfil, 'grandTFRbase_246', 'grandTFRbase_247','grandTFRbase_248');

%% step5 multiplotTFR

cd D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF
load grandTFRbase_non_ki;
cfg = [];
cfg.showlabels   = 'yes';	
cfg.layout       = 'quickcap64.mat';
cfg.channel      = 'all';
cfg.zlim = [-2.5 2.5];
figure;ft_multiplotTFR(cfg, grandTFRbase_246);
figure;ft_multiplotTFR(cfg, grandTFRbase_247);
figure;ft_multiplotTFR(cfg, grandTFRbase_248);

%% step6.1 parametric statistics

cd 'D:\Matlab_x64\toolbox\fieldtrip-20170628\TFR_lx\TFR_lF';
clear all
load grandTFRbase_ki.mat
data_abstract_Fz = grandTFRbase_246.powspctrm(:,10,2:4,23:29);
data_abstract_Cz = grandTFRbase_246.powspctrm(:,28,2:4,23:29);
data_subtraction = data_abstract_Cz - data_abstract_Fz
%data_abstract = grandTFRbase_248.powspctrm(:,[9,10,11,18,19,20],2:4,23:31);
data11 = mean(data_abstract,2);
data21 = squeeze(data11);
data31 = mean(data21,2);
data41 = squeeze(data31);
data51 = mean(data41,2);
data_248 = squeeze(data51);
%save('data_end_l','data_l')

data_abstract = grandTFRbase_246.powspctrm(:,12,2:4,23:27);
%data_abstract = grandTFRbase_246.powspctrm(:,12,[4,5],11:31);
data12 = mean(data_abstract,2);
data22 = squeeze(data12);
data32 = mean(data22,2);
data42 = squeeze(data32);
data52 = mean(data42,2);
data_r = squeeze(data52);
data_spss_246 = [(data_l - data_r)/(data_l + data_r)]*100;
%data_spss_246 = log(data_r) - log(data_l);
save('data_246','data_spss_246')

%% step6.2 parametric statistics

clear all
load grandTFRbase_ki.mat
data_abstract = grandTFRbase_247.powspctrm(:,8,2:4,23:27);
%data_abstract = grandTFRbase_247.powspctrm(:,[7,8,9],3,21:31);
%data_abstract = grandTFRbase_247.powspctrm(:,8,[4,5],11:31);
%data_abstract = grandTFRbase_247.powspctrm(:,[8,12,15,28],4:6,11:31);
data11 = mean(data_abstract,2);
data21 = squeeze(data11);
data31 = mean(data21,2);
data41 = squeeze(data31);
data51 = mean(data41,2);
data_l = squeeze(data51);
%save('data_end_l','data_l')

data_abstract = grandTFRbase_247.powspctrm(:,12,2:4,23:27);
%data_abstract = grandTFRbase_247.powspctrm(:,12,[4,5],11:31);
data12 = mean(data_abstract,2);
data22 = squeeze(data12);
data32 = mean(data22,2);
data42 = squeeze(data32);
data52 = mean(data42,2);
data_r = squeeze(data52);
data_spss_247 = [(data_l - data_r)/(data_l + data_r)]*100;
save('data_247','data_spss_247')

%% step6.3 parametric statistics
clear all
load grandTFRbase_ki.mat
data_abstract = grandTFRbase_248.powspctrm(:,8,2:4,23:27);
%data_abstract = grandTFRbase_248.powspctrm(:,[7,8,9],3,21:31);
%data_abstract = grandTFRbase_248.powspctrm(:,8,[4,5],11:31);
%data_abstract = grandTFRbase_248.powspctrm(:,[8,12,15,28],4:6,11:31);
data11 = mean(data_abstract,2);
data21 = squeeze(data11);
data31 = mean(data21,2);
data41 = squeeze(data31);
data51 = mean(data41,2);
data_l = squeeze(data51);
%save('data_end_l','data_l')

data_abstract = grandTFRbase_248.powspctrm(:,12,2:4,23:27);
%data_abstract = grandTFRbase_248.powspctrm(:,12,[4,5],11:31);
data12 = mean(data_abstract,2);
data22 = squeeze(data12);
data32 = mean(data22,2);
data42 = squeeze(data32);
data52 = mean(data42,2);
data_r = squeeze(data52);
data_spss_248 = [(data_l - data_r)/(data_l + data_r)]*100;
%A1 = log(data_r);
%B1 = log(data_l);
%data_spss_248 = A1 - B1;
save('data_248','data_spss_248')

%% step7 singleplotTFR
load grandTFRbase_non_ki;
cfg = [];
cfg.maskstyle    = 'opacity'; 
%cfg.maskstyle   = 'saturation';
cfg.layout       = 'quickcap64.mat';
cfg.channel      = 'FZ';
%cfg.channel     = ft_channelselection({'FCZ','F3','F4'},data_pre.label);%multi channel 
cfg.parameter    = 'powspctrm';
figure;ft_singleplotTFR(cfg, grandTFRbase_246);
colorbar
% new TFR plot with interpolation 
figure
pcolor(grandTFRbase_246.time,grandTFRbase_246.freq,squeeze(grandTFRbase_246.powspctrm(10,:,:)));
shading interp %deal the color 
colorbar

figure
pcolor(grandTFRbase_247.time,grandTFRbase_247.freq,squeeze(grandTFRbase_247.powspctrm(10,:,:)));
shading interp %deal the color 
colorbar

figure
pcolor(grandTFRbase_248.time,grandTFRbase_248.freq,squeeze(grandTFRbase_248.powspctrm(10,:,:)));
shading interp %deal the color 
colorbar
%% step8 topoplotTFR
clear all
cfg = [];
load 'grandTFRbase_non_ki.mat';
cfg.xlim = [0.3 0.8];
cfg.ylim = [8 12];
cfg.parameter = 'powspctrm';
cfg.layout       = 'quickcap64.mat';
cfg.operation = 'subtract';
%grandTFRbase_1_2 = ft_math(cfg,grandTFRbase_246,grandTFRbase_247);
figure;ft_topoplotTFR(cfg, grandTFRbase_248);colorbar
%figure;ft_topoplotTFR(cfg, grandTFRbase_1_2);colorbar

