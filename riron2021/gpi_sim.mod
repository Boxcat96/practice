//パート１：変数の定義///////////////////////////////////

//内生変数
var y pi epi gpi r y_obs pi_obs epi_obs gpi_obs r_obs;

//外生変数
varexo ugpi uy upi uepi ugpi ur;

//パラメータ
parameters theta alpha phipi phiy zeta gamma;

//パート２：カリブレートするパラメータ//////////////////

theta =   1.50         ; %消費の代替弾力性
alpha =   0.10         ; %NKPCのGDPgap項
phipi =   1.70         ; %Taylor ruleのインフレ率項
phiy  =   0.08         ; %Taylor ruleのGDPgap項

//zeta  =   0.50         ; %生鮮食品インフレ率に反応する家計の割合
//gamma =   0.70         ; %生鮮食品インフレ率の持続項(AR1)

//パート３：モデル///////////////////////////////////////

model(linear);

//線型モデル

y   = y(+1) - theta*(r-epi(+1))      ;
epi = (1-zeta)*pi + zeta*gpi(-1) ;
gpi = gamma*gpi(-1) + ugpi           ;
pi  = epi(+1)+ alpha*y               ;
r   = phipi*pi + phiy*y              ;

//観測方程式

y_obs=y+uy; %GDPの観測方程式
pi_obs=pi+upi; %インフレ率の観測方程式
epi_obs=epi+uepi; 
gpi_obs=gpi+ugpi; 
r_obs=r+ur; 

end;

//パート４：推計するパラメータの事前分布(江口2011、廣瀬2012、鎌田2009など)///////////

estimated_params;
zeta, normal_pdf, 0.5, 0.2; 
gamma, beta_pdf, 0.5, 0.2; 
stderr uy, inv_gamma_pdf, 0.1, inf; %以下、各内生変数の観測誤差
stderr upi, inv_gamma_pdf, 0.1, inf;
stderr ugpi, inv_gamma_pdf, 0.1, inf;
stderr ur, inv_gamma_pdf, 0.1, inf;
stderr uepi, inv_gamma_pdf, 0.1, inf;
end;

//パート５：推計///////////////////////////////////////////////////////////

//観測する変数の指定
varobs y_obs pi_obs epi_obs gpi_obs r_obs;

//推計コマンド(カルマンスムージングなし)//////////////////////////////
estimation(datafile=df, mode_check, mh_replic=100000, mh_nblocks=2, 
mh_drop=0.5, mh_jscale=0.89, bayesian_irf);
////////////////////////////////////////////////////////////////////////


//合理的期待均衡解の導出
stoch_simul;

//ヒストリカル分解を行うコマンド
shock_decomposition(parameter_set=posterior_mean) pi_obs;