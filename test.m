clc; clear all; tic;
%% ループの回数を指定
seed_min = 50;
seed_max = 53;
lags_min = 2;
lags_max = 3;

% ノックする配列の作成
range_x1 = seed_min:1:seed_max; 
range_x2 = lags_min:1:lags_max;

% ノック配列を結合
[x1_set,x2_set] = ndgrid(range_x1,range_x2); 
knock_set = [x1_set(:),x2_set(:)];

%% Do NOT Touch proc
% waitbarを初期化
hwaitbar = waitbar(0, 'Processing...', 'Name', '無限ノックツール');

% ノックループ開始
for ii = 1:size(knock_set,1)

    % このループで使用するノックセット
    x1 = knock_set(ii,1);
    x2 = knock_set(ii,2);

    % 結果データを作成
    data = rand(10, 5); % 10行×5列のランダム数値データ
    
    % 保存先フォルダ名
    folderName = sprintf('result/result_%d_%d', x1, x2);
    
    % フォルダの存在を確認
    if exist(folderName, 'dir')
        % フォルダが存在する場合、中のファイルを削除
        delete(fullfile(folderName, '*'));
    else
        % フォルダが存在しない場合、新規作成
        mkdir(folderName);
    end
    
    % 保存するExcelファイルのパス
    excelFileName = fullfile(folderName, 'result.xlsx');
    
    % Excelファイルに書き込み
    xlswrite(excelFileName, data)
    
    % waitbarを更新
    waitbar(ii/size(knock_set,1), hwaitbar, sprintf('実行中...%d%%', round(ii/size(knock_set,1)*100)));
end

% waitbarを閉じる
close(hwaitbar);

disp('ノック終了！');
toc;