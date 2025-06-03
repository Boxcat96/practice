% Computes the OLS estimator


% y = T x k matrix -- LHS of the VAR
% ly = T x k*p+1 matrix -- constant + lags of y


function b=ols(y,ly);

b=inv(ly'*ly)*ly'*y;
