% Lags (leads) data by "period" periods

function laggedseries = lagn(fyo,period)

% data is a column vector.
% period is an integer.
% If period < 0 ==> lead operator

[T2,N2] = size(fyo);

if period > 0

    lowerlaggedseries		= fyo(1:T2-period,:);
    topoflaggedseries		= NaN*ones(period,N2);
    laggedseries			= [topoflaggedseries;lowerlaggedseries];

else
   
    period=abs(period);   
    topoflaggedseries		= fyo(period+1:T2,:);
    lowerlaggedseries		= NaN*ones(period,N2);
    laggedseries			= [topoflaggedseries;lowerlaggedseries];

end