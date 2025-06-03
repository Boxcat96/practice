function [AA,GG,B0inv_1,xx,fx,fxd] = strucest(x,y,cens,p,fxtype,dgp_x,delta);

% PURPOSE: Estimate structural parameters required for computation of 
%           IRF via plug-in estimator of Goncalves, Herrera, Kilian and Pesavento (JoE, forthcoming)
%   
% ------------------------------------------------------------------------------------------
% INPUTS:
% x: Tx1 vector -> variable to be shocked and assumed predetermined wrt y
% y: Txn1 matrix -> other variables in model 
% cens: scalar -> censoring value in nonlinear transformation
%       f(x)=max(x,cens)
% p: lag length
% fxtype: 1 if f(x)=max(0,cens); 2 if f(x)=x^2; 3 if f(x)=x^3
% dgp_x: DGP for x -> Set =1 if x is iid; =2 if x~AR(p); =3 if x is
%        predetermined
%--------------------------------------------------------------------------------------------
% OUTPUTS:
% AA: (n1+1)×((nx1)×p) matrix of autoregressive coefficients
% GG: (n1+1)×(p+1)matrix of coefficients on nonlinear transformation and
%      its lags
% B0inv_1: (n1+1)x1 vector -> first column of B0inverse
% xx: (T-p)x1 vector of x observations to be used in computation of IRF
% fx: (T-p)x1 vector of f(x)
% fxd: (T-p)x1 vector of f(x+delta)
% -------------------------------------------------------------------------------------------

%% Arrange variables in matrix

n1=size(y,2);
nk=n1+1;
x0=x;
y0=y;
z0 = [x0 y0]; % Monetary Shocks, Federal Funds Rate, GDP, inflation Rate
con = ones(size(z0,1),1); 
ke = z0(:,1);
z = z0(p+1:end,:);
x = x0(p+1:end,:);xx=x;
y = y0(p+1:end,:);

%% Create Lags

[t,n]=size(x0);
T=t-p;
xlag = con;

for i = 1:p
    xlag = [xlag lagnc(x0,i)];
end
xlag = xlag(p+1:end,2:end);

zlag = con;
for i = 1:p
    zlag = [zlag lagnc(z0,i)];
end
zlag = zlag(p+1:end,:);

if fxtype>0
fx0 = fxnl(fxtype,x0,cens);      %Nonlinear transformation of x
fxd0=fxnl(fxtype,x0+delta,cens); % now allow for delta
fxlag=fxnl(fxtype,xlag(1:end,:),cens);% Use the ITR1Y shock lag variables and censor
fx = fx0(p+1:end,:);
fxd = fxd0(p+1:end,:);
else;
fx = x0(p+1:end,:);
fxd = fx+delta;
end

%% Estimate structural parameters and form relevant matrices

if dgp_x==1                   % Define regressors for first block depending on DGP
   w1=ones(T,1);
 elseif dgp_x==2
   w1=xlag;
else
   w1=zlag;
end   

b_x = inv(w1'*w1)*w1'*x;     % Parameters for first block
%resid1 = x-b_x*x;
resid1 = x;

if dgp_x==1
   AA=zeros(1,nk*p);
elseif dgp_x==2
   A1=[b_x(2:end) zeros(p,p*n1)];
   AA=(reshape(A1,[],1))'; 
else
   A1= b_x(2:end);
   AA=(reshape(A1,[],1))'; 
end   
B0inv_1=1;
GG= zeros(1,p+1);

if fxtype>0
  w2 = [zlag fx fxlag resid1];  % Regressors for second block
else  
  w2 = [zlag resid1];  % Regressors for second block
end
for i=1:n1
    b_y = inv(w2'*w2)*w2'*y(:,i);      % Paramters for second block
    B0inv_1 = [B0inv_1 ; b_y(end,1)];
    AA = [AA ; b_y(2:nk*p+1,1)'];
    if fxtype>0
    GG = [GG ; b_y(nk*p+2:end-1,1)'];
    else
    GG = zeros(nk,p+1);
    end
end

disp('Autoregressive Coefficients- Plug-in IRF Estimation')
disp(AA)

disp('B0inv Matrix (First Column) for NonLinear Model- Plug-in IRF Estimation')
disp(B0inv_1)

disp('Nonlinear Coefficients- Plug-in IRF Estimation')
disp(GG)
