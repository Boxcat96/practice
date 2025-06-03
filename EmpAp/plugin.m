function irf = plugin(x,y,H,delta,cens,p,dgp_x,fxtype);

%---------------------------------------------------------------------------------------------------
% PURPOSE: Estimate impulse response function via plug-in estimator of Goncalves, Herrera, Kilian
%          and Pesavento (JoE, forthcoming)
%
%---------------------------------------------------------------------------------------------------
% INPUTS: 
% x: Tx1 vector -> variable to be shocked and assumed predetermined wrt y
% y: Txn1 matrix -> other variables in model 
% cens: scalar -> censoring value in nonlinear transformation
%       f(x)=max(x,cens)
% p: lag length
% fxtype: 1 if f(x)=max(x,cens); 2 if f(x)=x^2; 3 if f(x)=x^3
% dgp_x: DGP for x -> Set =1 if x is iid; =2 if x~AR(p); =3 if x is
%        predetermined
% H: maximum horizon for IRF
% 
% OUTPUT:
% irf: n1 x (H+1) matrix of impulse response function
%
%------------------------------------------------------------------------------------------------------------

[AA,GG,B0inv_1,xx,fx,fxd] = strucest(x,y,cens,p,fxtype,dgp_x,delta);

x=xx;
NN = size(x,1);
nv = size(y,2)+1;
xd = x+delta;
dif_fx = fxnl(fxtype,xd,cens)-fxnl(fxtype,x,cens);
A_hdel = (1/NN)*(sum(fxd)-sum(fx));
psiL_e=eye(nv);

ke_m = zeros((p-1).*nv,nv);
if p>1
   psiP_e = [psiL_e; ke_m];    
else
   psiP_e = psiL_e; 
end
     
psiL_e= [psiL_e zeros(nv,p*nv)];
psi_bet_e=psiL_e(1:nv,1:nv)*B0inv_1;
psi_gam_e=psiL_e(1:nv,1:nv*(p+1))*GG(:);
psi_gam11_e=psi_gam_e(1,1);
irf= (psi_bet_e(2:nv,1)*delta)+psi_gam_e(2:nv,:)*A_hdel;

j =2;
while j<= H+1
  psiL_e = [(AA*psiP_e(1:nv*p,:)) psiL_e]; 
  psiP_e = [AA*psiP_e(1:nv*p,:); psiP_e]; 
  psi_bet_e = psiP_e(1:nv,1:nv)*B0inv_1;
  
  psi_gam_e = [psi_gam_e psiL_e(1:nv,1:nv*(p+1))*GG(:)];  
  psi_gam11_e = [ psi_gam11_e  psi_gam_e(1,1)];

  xd = x(j:NN,1)+psi_bet_e(1,1)*delta*ones(NN-j+1,1)+dif_fx(1:size(dif_fx,1)-1,:)*psi_gam11_e(1:size(psi_gam11_e,2)-1)'; 
  dif_fx = [(fxnl(fxtype,xd,cens)-fxnl(fxtype,x(j:NN,1),cens)) dif_fx(1:size(dif_fx,1)-1,:)]; 
  A_hdel = [(mean(fxnl(fxtype,xd,cens))-mean(fxnl(fxtype,x,cens)));A_hdel]; 
  irf = [irf (psi_bet_e(2:nv,1)*delta)+psi_gam_e(2:nv,:)*A_hdel];
  
  j = j+1;
end










