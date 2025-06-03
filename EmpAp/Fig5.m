% This code replicates Figure 5 in Goncalves, Herrera, Kilian and
% Pesavento (2021), forthcoming in Journal of Econometrics
% Note that the dynamic system needs to be stationary
% This code calls the matlab functions plugin.m, strucest.m, fxnl.m
% lagnc.m olss.m and dif.m



clear all

%% Define Globals

p=1;         % Number of lags in structural model
delta=1;     % Size of the shock
cens=0;      % censoring value for f(x)=max(cens,x); set equal to zero for other f(x)@
nl=3;        % Number of variables in y 
nk=nl+1;     % Total number of variables in z=[x y]
H=20;        % Horizon for IRF
dgp_x=1;     % dgp_x=1 for x~iid; dgp_x=1 for x~AR(p); dgp_x=3 for x predetermined w.r.t y

%% Read and transform data

ydata=xlsread('data_empap'); 
gdp1 = ydata(:,1); % GDP data
cpi = ydata(:,2); % CPI
ffr = ydata(:,3); % Federal Funds Rate
shocks = ydata(:,4); % Monetary Policy Shocks

% Detrend GDP
y = log(gdp1);
cons = ones(size(y,1),1); 
t=1:1:length(y); % linear trend
tsq=t.^2; % quadratic trend
X= [cons t'];
b0 = olss(y,t');

beta = (X'*X)\(X'*y); % OLS Regression Coefficients
e0 =  y - t'*beta(2,:); % residual
gdp = 100*e0(2:end,:);
inf = dif(log(cpi))*100; % First differences in log of CPI


%% Define variables and arrange

inf=inf(1:end,:); %Inflation
ffr = ffr(2:end,:);%Federal Funds Rate
e = shocks(2:end,:); % i.i.d. monetary policy shocks 


%% Estimate IRF using Plug-in Estimator
X= e ;                                      % Variable to be shocked, 
Y= [ffr gdp inf];                           % Other variables in the system

% IRFs: row are responses, columns horizons 
irf_0=plugin(X,Y,H,delta,cens,p,dgp_x,0);   % Linear: fxtype=0
irf_1=plugin(X,Y,H,delta,cens,p,dgp_x,1);   % f(x)=max(0,x): fxtype=1
irf_3=plugin(X,Y,H,delta,cens,p,dgp_x,3);   % f(x)=x^3: fxtype=3

%% Plot responses (Figure 5)

horizon = 21; % Horizon for Impulse Response including h=0
kk=zeros(1,horizon);
set(0,'DefaultAxesTitleFontWeight','normal');

figure;
orient(figure,'landscape')

% Top panel plots responses when f(x)=max(x,0) and when model is linear
subplot(2,3,1)
plot(1:1:horizon, irf_1(1,:), 'b', 'LineWidth',1); hold on;
plot(1:1:horizon, irf_0(1,:),':r', 'LineWidth',1); hold on;
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.5 2.5])
% yticks([-0.002 0 0.002 0.004 0.005])
ylabel('Percent','Interpreter','latex')
xlabel('Quarters','Interpreter','latex')
title('Fed Funds Rate','Interpreter','latex')
legend('Non-Linear','Linear','Location','NorthEast', 'Orientation','vertical', 'Interpreter','latex','FontSize',10, 'FontName','Helvetia') %SouthOutside % You may change the location manually
set(gca,'FontSize',11,'FontName','Helvetia')

subplot(2,3,2)
plot(1:1:horizon, irf_1(2,:), 'b', 'LineWidth',1); hold on;
plot(1:1:horizon, irf_0(2,:), ':r', 'LineWidth',1); hold on;
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.6 0.4])
xlabel('Quarters','Interpreter','latex')
title('Log Real GDP','Interpreter','latex')
set(gca,'FontSize',11,'FontName','Helvetia')
  
  
subplot(2,3,3)
plot(1:1:horizon, irf_1(3,:), 'b', 'LineWidth',1); hold on;
plot(1:1:horizon, irf_0(3,:), ':r', 'LineWidth',1) % '.r'
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.6 0.4])
xlabel('Quarters','Interpreter','latex')
title('PCE Inflation','Interpreter','latex')
set(gca,'FontSize',11,'FontName','Helvetia')

% Bottom panelplots responses when f(x)=x^3 and when model is linear
subplot(2,3,4)
plot(1:1:horizon, irf_3(1,:),'b','LineWidth',1); hold on;
plot(1:1:horizon, irf_0(1,:), ':r', 'LineWidth',1) % '.r'
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.5 2.5])
ylabel('Percent','Interpreter','latex')
xlabel('Quarters','Interpreter','latex')
title('Fed Funds Rate','Interpreter','latex')
set(gca,'FontSize',11,'FontName','Helvetia')


subplot(2,3,5)
plot(1:1:horizon, irf_3(2,:),'b','LineWidth',1); hold on;
plot(1:1:horizon, irf_0(2,:),':r', 'LineWidth',1) % '.r'
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.6 0.4])
xlabel('Quarters','Interpreter','latex')
title('Log Real GDP','Interpreter','latex')
set(gca,'FontSize',11,'FontName','Helvetia')
  
  
subplot(2,3,6)
plot(1:1:horizon, irf_3(3,:), 'b','LineWidth',1); hold on;
plot(1:1:horizon, irf_0(3,:), ':r', 'LineWidth',1) % '.r'
yline(0,'k','LineWidth',1);
xlim([1 20])
xticks([0 5 10 15 20])
ylim([-0.6 0.4])
xlabel('Quarters','Interpreter','latex')
title('PCE Inflation','Interpreter','latex')
set(gca,'FontSize',11,'FontName','Helvetia')
