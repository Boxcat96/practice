#################データセットの作成#####################
################データがある場合は下まで飛ばしてよい##############

data <- new.env()

# 推計開始時期と終了時期
date.start <- "1997-04-01"
date.end <- "2019-06-30"


#賃金、株価、個人消費、物価（PCE デフレータ）

tickers <- c( "LES1252881600Q"    #Employed full time: Median usual weekly real earnings
              #: Wage and salary workers: 16 years and over #W"
             ,"SPASTT01USQ661N" #Total Share Prices for All Shares for US
             ,"PCECC96"          #Real Personal Consumption Expenditures #C
             ,"DPCERD3Q086SBEA")  #PCE deflator



# quantmodパッケージを使ってFREDのデータベースにアクセス
if (!require("quantmod")) {install.packages("quantmod"); library("quantmod")}
getSymbols( tickers
            , src = "FRED"
            , from = date.start 
            , to = date.end  
            , env = data)

# データセットの作成
dtx1 <- data$LES1252881600Q
x1 <- dtx1[paste(date.start,date.end,sep="/")]
dtx2 <- data$SPASTT01USQ661N
x2 <- dtx2[paste(date.start,date.end,sep="/")]
dtx3 <- data$PCECC96
x3 <- dtx3[paste(date.start,date.end,sep="/")]
dtx4 <- data$DPCERD3Q086SBEA
x4 <- dtx4[paste(date.start,date.end,sep="/")]


#対数をとる（必要なら）
L1 <- log(x1)
L2 <- log(x2)
L3 <- log(x3)
L4 <- log(x4)

#前期比をとる（パーセンテージ）＆１列目を削除
lag1 <- (L1/lag(L1))*100
c1 <- lag1[-1, ]

lag2 <- (L2/lag(L2))*100
c2 <- lag2[-1, ]

lag3 <- (L3/lag(L3))*100
c3 <- lag3[-1, ]

lag4 <- (L4/lag(L4))*100
c4 <- lag4[-1, ]


#データフレームの作成
out <- cbind(c1, c2, c3, c4)
colnames(out) <- c("wage", "stockprice", "cousumption", "price")
head(out)


###################################################################
#######データセットがある場合はこっからでよい！####################
###################################################################

#時系列ライブラリの起動
if (!require("vars")) {install.packages("vars"); library("vars")}
if (!require("tseries")) {install.packages("tseries"); library("tseries")}

#ADFテスト
adf.test(c1)
adf.test(c2)
adf.test(c3)
adf.test(c4)


#AIC（望ましいラグ項を求める。AICが小さい方がよい）
select_VAR <- VARselect(out, lag.max = 6)
select_VAR

#VARのパラメータ推計
VAR_parameter <- VAR(out,p=select_VAR$selection[1])
#上のAICのうち、最も望ましいものでVARをやってくれる

#結果
summary(VAR_parameter)


#グレンジャー因果
causality(VAR_parameter,cause = "wage")

#ヒストリカル分解
if (!require("svars")) {install.packages("svars"); library("svars")}
p1 <- id.dc(VAR_parameter)
p2 <- hd(p1, series = 4)

#plot(p2)で一応グラフは出るけど見にくいのでExcelに出力してから書く

###########Excelに出力#############################
write.csv(p2$hidec, "C:/cat/consumption.csv", row.names = T)
###########保存場所は適当にいじってください##############


#IRF（インパルス反応）の導出
#信頼区間…68.4%（１標準誤差バンド）

t <- 8 #IRFの表示期間設定
impulse_func <- irf(VAR_parameter,n.ahead = t ,ci = 0.684,ortho = FALSE)
ortho_impulse_func <- irf(VAR_parameter,n.ahead = t ,ci = 0.684, ortho = TRUE)
#plot(impulse_func)
#plot(ortho_impulse_func)

#描画
number_ticks <- function(n) {function(limits) pretty(limits, n)}
lags <- c(0:t)

irf1<-data.frame(ortho_impulse_func$irf$stockprice[,1],ortho_impulse_func$Lower$stockprice[,1],
                 ortho_impulse_func$Upper$stockprice[,1], lags)
irf2<-data.frame(ortho_impulse_func$irf$stockprice[,2],ortho_impulse_func$Lower$stockprice[,2],
                 ortho_impulse_func$Upper$stockprice[,2], lags)
irf3<-data.frame(ortho_impulse_func$irf$stockprice[,3],ortho_impulse_func$Lower$stockprice[,3],
                 ortho_impulse_func$Upper$stockprice[,3])
irf4<-data.frame(ortho_impulse_func$irf$stockprice[,4],ortho_impulse_func$Lower$stockprice[,4],
                 ortho_impulse_func$Upper$stockprice[,4])

#ggplot2
if (!require("ggplot2")) {install.packages("ggplot2"); library("ggplit2")}
if (!require("gridExtra")) {install.packages("gridExtra"); library("gridExtra")}

#フォント変更（Windows版、消しても問題なし）
windowsFonts("AR"=windowsFont("Arial"))

wage_stockprice <- ggplot(data = irf1,aes(lags,ortho_impulse_func.irf.stockprice...1.)) +
  geom_line(aes(y = ortho_impulse_func.Upper.stockprice...1.), colour = 'lightblue2') +
  geom_line(aes(y = ortho_impulse_func.Lower.stockprice...1.), colour = 'lightblue')+
  geom_line(aes(y = ortho_impulse_func.irf.stockprice...1.), size = 1.1, alpha = 0.8)+
  geom_ribbon(aes(x=lags, ymax=ortho_impulse_func.Upper.stockprice...1.
                  , ymin=ortho_impulse_func.Lower.stockprice...1.)
              , fill="cyan", alpha=.1) +
  xlab("") + ylab("wage") + ggtitle("IRF from stock price")+
  theme(axis.title.x=element_blank(),
        #           axis.text.x=element_blank(),                    
        #           axis.ticks.x=element_blank(),
        plot.margin = unit(c(-10,10,4,10), "mm"))+
  scale_x_continuous(breaks=number_ticks(10)) +
  geom_line(colour = 'steelblue')+ theme_bw(base_size = 14, base_family = "AR")+
  geom_hline(yintercept=0, linetype="dashed", colour="steelblue") 

stockprice_stockprice <- ggplot(data = irf2,aes(lags,ortho_impulse_func.irf.stockprice...2.)) +
  geom_line(aes(y = ortho_impulse_func.Upper.stockprice...2.), colour = 'lightblue2') +
  geom_line(aes(y = ortho_impulse_func.Lower.stockprice...2.), colour = 'lightblue')+
  geom_line(aes(y = ortho_impulse_func.irf.stockprice...2.), size = 1.1, alpha = 0.8)+
  geom_ribbon(aes(x=lags, ymax=ortho_impulse_func.Upper.stockprice...2., 
                  ymin=ortho_impulse_func.Lower.stockprice...2.), fill="cyan", alpha=.1) +
  xlab("") + ylab("stockprice")  + ggtitle("IRF from stock price (with 1 std.err band)")+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),                    
        axis.ticks.x=element_blank(),
        plot.margin = unit(c(2,10,2,10), "mm"))+
  scale_x_continuous(breaks=number_ticks(10)) +
  geom_line(colour = 'steelblue')+ theme_bw(base_size = 14, base_family = "AR") +
  geom_hline(yintercept=0, linetype="dashed", colour="steelblue") 

consumption_stockprice <- ggplot(data = irf3,aes(lags,ortho_impulse_func.irf.stockprice...3.)) +
  geom_line(aes(y = ortho_impulse_func.Upper.stockprice...3.), colour = 'lightblue2') +
  geom_line(aes(y = ortho_impulse_func.Lower.stockprice...3.), colour = 'lightblue')+
  geom_line(aes(y = ortho_impulse_func.irf.stockprice...3.), size = 1.1, alpha = 0.8)+
  geom_ribbon(aes(x=lags, ymax=ortho_impulse_func.Upper.stockprice...3.
                  , ymin=ortho_impulse_func.Lower.stockprice...3.)
              , fill="cyan", alpha=.1) +
  xlab("") + ylab("consumption")  +
  theme(axis.title.x=element_blank(),
        #           axis.text.x=element_blank(),                    
        #           axis.ticks.x=element_blank(),
        plot.margin = unit(c(-10,10,4,10), "mm"))+
  scale_x_continuous(breaks=number_ticks(10)) +
  geom_line(colour = 'steelblue')+ theme_bw(base_size = 14, base_family = "AR")+
  geom_hline(yintercept=0, linetype="dashed", colour="steelblue") 

price_stockprice <- ggplot(data = irf4,aes(lags,ortho_impulse_func.irf.stockprice...4.)) +
  geom_line(aes(y = ortho_impulse_func.Upper.stockprice...4.), colour = 'lightblue2') +
  geom_line(aes(y = ortho_impulse_func.Lower.stockprice...4.), colour = 'lightblue')+
  geom_line(aes(y = ortho_impulse_func.irf.stockprice...4.), size = 1.1, alpha = 0.8)+
  geom_ribbon(aes(x=lags, ymax=ortho_impulse_func.Upper.stockprice...4.
                  , ymin=ortho_impulse_func.Lower.stockprice...4.)
              , fill="cyan", alpha=.1) +
  xlab("") + ylab("price") +
  theme(axis.title.x=element_blank(),
        #           axis.text.x=element_blank(),                    
        #           axis.ticks.x=element_blank(),
        plot.margin = unit(c(-10,10,4,10), "mm"))+
  scale_x_continuous(breaks=number_ticks(10)) +
  geom_line(colour = 'steelblue')+ theme_bw(base_size = 14, base_family = "AR")+
  geom_hline(yintercept=0, linetype="dashed", colour="steelblue") 


grid.arrange(stockprice_stockprice,consumption_stockprice,price_stockprice, nrow=3)

#予測
#pred<-predict(VAR_parameter,n.ahead=20,ci=0.684)
#plot(pred)

