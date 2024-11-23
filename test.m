clc; clear all; 
tic;
%% ループの回数を指定

% ノックする配列の作成
range_x1 = 50:53; % シード
range_x2 = 2:3;   % ラグ

%% Do NOT Touch proc

% ノック配列の作成
[x1_set,x2_set] = ndgrid(range_x1,range_x2); 
knock_set = [x1_set(:),x2_set(:)]; % 結合されたノック配列
loop_num = size(knock_set,1); % ループ回数

% waitbarを初期化
hwaitbar = waitbar(0, 'Processing...', 'Name', '無限ノックツール');

% ノックループ開始
for ii = 1:loop_num

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
    waitbar(ii/loop_num, hwaitbar, sprintf('実行中...%d%%', round(ii/loop_num*100)));
end

% waitbarを閉じる
close(hwaitbar);

% 終了
disp('ノック終了！');
toc;