rm(list=ls()) # 変数のクリア
graphics.off() # 図表のクリア

# 必要なパッケージ
library(tsDyn)       # 閾値VAR (TVAR)
library(KFAS)        # 状態空間モデル (TV-VAR)
library(tidyverse)       # データ処理

# 1. データ生成: インフレ率とインフレ予想の時系列データ (擬似データ
set.seed(22)
time_series_length <- 100
inflation <- rnorm(time_series_length, mean=1.0, sd=0.5)
inflation_expectations <- rnorm(time_series_length, mean=1.0, sd=0.5)

df <- data.frame(
  time = 1:time_series_length,
  inflation = inflation,
  inflation_expectations = inflation_expectations
)

# データフレームを整形
df_long <- df %>%
  select(time, inflation, inflation_expectations) %>%
  pivot_longer(cols = c(inflation, inflation_expectations),
               names_to = "variable", values_to = "value")

# 折れ線グラフの描画
ggplot(df_long, aes(x = time, y = value, color = variable)) +
  geom_line(linewidth = 1) +
  theme_minimal() +
  labs(title = "インフレ率とインフレ予想の推移",
       x = "時間", y = "値", color = "指標") +
  scale_color_manual(values = c("inflation" = "red", "inflation_expectations" = "blue")) +
  theme(legend.position = "top")

# 2. 閾値VAR (TVAR) の推定: 閾値を自動検出
tvar_model <- TVAR(df[, c("inflation", "inflation_expectations")],
                   lag = 2, nthresh = 1,
                   thVar = df$inflation, trim = 0.1, mTh = 1)

# 検出された閾値の取得
threshold <- tvar_model$model.specific$Thresh

# インパルス応答関数の計算
irf_tvar <- irf(tvar_model, n.ahead = 10, boot = FALSE)

# IRFのプロット
# plot(irf_tvar, main = "閾値VAR: インフレ率がインフレ予想に与える影響",
#      col = c("blue", "red"), lty = c(1, 2))
# legend("topright", legend = c("低インフレ", "高インフレ"), col = c("blue", "red"), lty = c(1, 2))

# 高インフレ（high regime）と低インフレ（low regime）に分ける
high_inflation_data <- df[df$inflation >= threshold, ]
low_inflation_data <- df[df$inflation < threshold, ]

# 高インフレレジームのIRF計算
tvar_high <- TVAR(high_inflation_data[, c("inflation", "inflation_expectations")], 
                  lag = 2, nthresh = 1, thVar = high_inflation_data$inflation)
irf_high <- irf(tvar_high, n.ahead = 10, boot = FALSE)

# 低インフレレジームのIRF計算
tvar_low <- TVAR(low_inflation_data[, c("inflation", "inflation_expectations")], 
                 lag = 2, nthresh = 1, thVar = low_inflation_data$inflation)
irf_low <- irf(tvar_low, n.ahead = 10, boot = FALSE)

# 高インフレレジームのIRFプロット
# plot(irf_high, main = "高インフレレジーム: インフレ率 → インフレ予想のIRF", 
#      col = c("blue", "red"), lty = c(1, 2))

# 低インフレレジームのIRFプロット
# plot(irf_low, main = "低インフレレジーム: インフレ率 → インフレ予想のIRF", 
#      col = c("blue", "red"), lty = c(1, 2))


# 3. 時変VAR (TV-VAR) の推定
# 状態空間モデルの構築 (KFAS を使用)
model <- SSModel(df$inflation_expectations ~ SSMtrend(1, Q = list(matrix(0.1))) +
                   SSMregression(~ df$inflation, Q = matrix(0.1)), H = matrix(0.1))

# カルマンフィルタの適用
fit <- fitSSM(model, inits = rep(0.01, 2), method = "BFGS")
out <- KFS(fit$model, smoothing = "state")

# 推定された係数をデータフレーム化
df_coef <- data.frame(
  time = df$time,
  coef = out$alphahat[, 2]  # インフレ率の係数
)

# 時変計数のプロット
ggplot(df_coef, aes(x = time, y = coef)) +
  geom_line(color = "blue", size = 1) +
  labs(title = "時変VAR: インフレ率がインフレ予想に与える影響の時間推移",
       x = "時間", y = "影響の大きさ") +
  theme_minimal()

# 4. ヒートマップの描画
df_coef$regime <- ifelse(df$inflation >= threshold, "高インフレ", "低インフレ")

ggplot(df_coef, aes(x = time, y = regime, fill = as.numeric(coef))) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = median(df_coef$coef, na.rm = TRUE)) +
  theme_minimal() +
  labs(title = "時変VAR×閾値VAR: インフレ率がインフレ予想に与える影響の時間推移",
       x = "時間", y = "レジーム", fill = "影響度")

# 閾値の表示
print(paste("検出された閾値:", threshold))

