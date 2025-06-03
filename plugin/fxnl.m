
function fx_nl = fxnl(fxtype,e,cens)
if fxtype == 1
     fx_nl = max(e, cens);
 elseif fxtype == 2
     fx_nl = e.^2;
 else
     fx_nl = e.^3;
     
 end