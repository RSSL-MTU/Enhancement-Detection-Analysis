close all;
clear;
clc;
metrics_csv = 'C:\Users\aawad\Desktop\IEEE Trans Sets\Q-index\RUOD';
outlier_Detection = "median"; %quartiles, check Matlab docs
models = ["Original", "ACDC","TEBCF", "BayesRet", "PCDE", "ICSP", "AutoEnh", "Semi-UIR", "USUIR", "TUDA"];
absolute_max = [-inf,-inf,-inf,-inf];
absolute_min = [inf,inf,inf,inf];

%first loop to get the absolute max and min from all dataset
for i=1 : length(models)
    model = models(i);
    metric = readtable(fullfile(metrics_csv, model));
    metrics(:,1) = metric.UIQM;
    metrics(:,2) = metric.UCIQE;
    metrics(:,3) = metric.CCF;
    metrics(:,4) = metric.Entropy;
    [metrics_rem, ~] = filloutliers(metrics, NaN, sprintf('%s', outlier_Detection));
    temp_max = max(metrics_rem);
    temp_min = min(metrics_rem);
    absolute_max = max(absolute_max,temp_max);
    absolute_min = min(absolute_min,temp_min);
end

%second loop is for Q-index calculations for each model
for i=1 : length(models)
    model = models(i);
    metric = readtable(fullfile(metrics_csv, model));
    metrics(:,1) = metric.UIQM;
    metrics(:,2) = metric.UCIQE;
    metrics(:,3) = metric.CCF;
    metrics(:,4) = metric.Entropy;


    [norm_outliers, ~] = filloutliers(metrics, NaN, sprintf('%s', outlier_Detection));
    [row, col] = find(isnan(norm_outliers));
    for i = 1 : length(row)
        if metrics(row(i),col(i)) > mad(metrics(:,col(i)))
            norm_outliers(row(i),col(i)) = max(norm_outliers(:,col(i)));
        else
            norm_outliers(row(i),col(i)) = min(norm_outliers(:,col(i)));
        end
    end

    norm_nan = rescale(norm_outliers, "InputMin",absolute_min,"InputMax",absolute_max);
    
    predicted_score = mean(norm_nan,2);

    try
        metric = removevars(metric,{'Q_index'});
    catch    
    end
    try
        metric = removevars(metric,{'Q_index_1'});
    catch    
    end
    try
        metric = removevars(metric,{'Q_index_2'});
    catch    
    end
    try
        metric = removevars(metric,{'Qindex'});
    catch    
    end

    metric.('Q-index') = predicted_score;
    writetable(metric,sprintf('%s\\%s.csv', metrics_csv, model),'WriteRowNames',true);
end

