rm(list = ls())
graphics.off()

library(vars)
library(openxlsx)
library(svars)

# read data
dat <- read.xlsx("C:/Users/tkero/OneDrive/経済ファイル/02_分析/03_Blanchar_Quah_1989/US/BQdata.xlsx")
data_start = 1948

#yt <- 100 * log(dat$y)
#dyt <- diff(yt)
dyt <- dat$y
unt <- dat$u

#demean(optional)
dyt <- dyt - mean(dyt)
unt <- unt - mean(unt)

dyt <- ts(dyt, start = c(data_start, 2), frequency = 4)
unt <- ts(unt, start = c(data_start, 2), frequency = 4)
vardat0 <- cbind(dyt, unt)

plot.ts(vardat0, main = "")

#VAR model
model0 <- VAR(vardat0, p = 8, type = "none")
summary(model0)

#Blanchard and Quah (1989) decomposition
model1 <- BQ(model0)
summary(model1)

#historical decomposition
p1 <- id.dc(model1$var)
p2 <- hd(p1, series = 1)

write.xlsx(p2$hidec, "C:/Users/tkero/OneDrive/経済ファイル/02_分析/03_Blanchar_Quah_1989/DECOMP.xlsx", rowNames = T)

#prediction
pred<-predict(model1$var,n.ahead=20,ci=0.684)
write.xlsx(pred$fcst, "C:/Users/tkero/OneDrive/経済ファイル/02_分析/03_Blanchar_Quah_1989/PRED.xlsx", rowNames = T)
plot(pred)

#draw IRF
irf.dyt <- irf(model1, impulse = "dyt", boot = FALSE, n.ahead = 40)
irf.unt <- irf(model1, impulse = "unt", boot = FALSE, n.ahead = 40)

supply <- cbind(cumsum(irf.dyt$irf$dyt[, 1]), irf.dyt$irf$dyt[, 2])

demand <- cbind(-1 * cumsum(irf.unt$irf$unt[, 1]), -1 * irf.unt$irf$unt[, 2])

#Demand Shock
plot.ts(demand[, 1], col = "black", lwd = 2, ylab = "", 
        xlab = "", main = "Demand Shock", xlim = c(1, 40), ylim = c(-0.6, 1.4))

lines(demand[, 2], col = "blue", lwd = 2)
abline(h = 0)
legend(x = "topright", c("Output response", "Unemployment response"), 
       col = c("black", "blue"), lwd = 2, bty = "n")

#Supply Shock
plot.ts(supply[, 1], col = "black", lwd = 2, ylab = "", 
        xlab = "", main = "Supply Shock", xlim = c(1, 40), ylim = c(-0.6, 1))

lines(supply[, 2], col = "blue", lwd = 2)
abline(h = 0)
legend(x = "topright", c("Output response", "Unemployment response"), 
       col = c("black", "blue"), lwd = 2, bty = "n")
