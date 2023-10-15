//パート１：変数の定義///////////////////////////////////

//内生変数
var y pi y_obs pi_obs;

//外生変数
varexo ueta upi uy;

//パラメータ
parameters beta gamma kappa phione phitwo phithree phifour;

//パート２：カリブレートするパラメータ（なし）//////////////////

//パート３：モデル///////////////////////////////////////

model(linear);

//線型モデル

y = phione*y(-1)+phitwo*y(-2)+phithree*pi(-1)+phifour*pi(-2)+ueta;
pi-gamma*pi(-1) = beta*(pi(+1)-gamma*pi)+kappa*y;

//観測方程式

y_obs= y+uy; %GDPの観測方程式
pi_obs= pi+upi; %インフレ率の観測方程式

end;

//パート４：推計するパラメータの事前分布(Pfajfar2018)///////////

estimated_params;
beta, normal_pdf, 0.5, 0.5;
gamma, normal_pdf, 0.5, 0.15; 
kappa, normal_pdf, 0.1, 0.1; 
phione, normal_pdf, 1.3, 0.5;
phitwo, normal_pdf, -0.5, 0.5;
phithree, normal_pdf, 0.1, 1.0;
phifour, normal_pdf, 0.1, 1.0;

%以下、各内生変数の観測誤差
stderr uy, inv_gamma_pdf, 0.1, inf; 
stderr ueta, inv_gamma_pdf, 0.1, inf; 
stderr upi, inv_gamma_pdf, 0.1, inf;
end;

//パート５：推計///////////////////////////////////////////////////////////

//観測する変数の指定
varobs y_obs pi_obs;

//推計コマンド(カルマンスムージングなし)//////////////////////////////
estimation(datafile=JPdata, mode_check, mh_replic=100000, mh_nblocks=2, 
mh_drop=0.5, mh_jscale=0.6, bayesian_irf);
////////////////////////////////////////////////////////////////////////


//合理的期待均衡解の導出
stoch_simul;