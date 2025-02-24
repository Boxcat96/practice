library(plm)
library(panelvar)
library(tictoc)

tic()

data(EmplUK)

# 先に対数をとっておく
for(i in 4:7){
  EmplUK[,i] <- log(EmplUK[,i])
}

# Windowsではこれを入れないと回らない
options(mc.cores = 1)

# パネルVAR
pvar.1<- pvargmm(dependent_vars = c('emp','wage','capital','output'),
                 lags = 2,                       # 内生変数のラグ次数
                 transformation = "fod",         # fdなら一階階差、fodならFOD変換
                 #predet_vars = c('',''),        # 先決内生変数
                 #exog_vars = c('',''),          # 外生変数
                 data = EmplUK,                   # 分析するデータフレーム
                 panel_identifier=c('firm','year'),  # 個体＆時間変数の指定
                 steps = c("twostep"),           # 1-stepか2-stepか
                 system_instruments = T,         # TRUEだとシステムGMM
                 max_instr_dependent_vars = 3,   # 内生変数の操作変数の最大ラグ
                 max_instr_predet_vars = 3,      # 先決変数の操作変数の最大ラグ
                 min_instr_dependent_vars = 2,  # 内生変数の操作変数の最小ラグ
                 min_instr_predet_vars = 2      # 内生変数の操作変数の最小ラグ
)

# 結果表示
summ.1 <- summary(pvar.1)
summary(pvar.1)

# インパルス
irf.1 <- oirf(pvar.1, n.ahead=10)
plot(irf.1)

boot.1 <- bootstrap_irf(pvar.1, typeof_irf = c("OIRF"),
                        n.ahead=10, 
                        nof_Nstar_draws=100, 
                        confidence.band = 0.95)



toc()