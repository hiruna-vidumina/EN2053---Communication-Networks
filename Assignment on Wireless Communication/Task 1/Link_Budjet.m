R = (0:10000)';       %distance in m
freq = 50e9;          %frequency in Hz
rainrate = 20;        %in mm/hr
el = 0;               % 0 degree elevation angle
tau = 0;              % horizontal polarization
T = 31;               % ambient temperature of 31 degree Celsius
waterdensity = 0.5;   % liquid water density in g/m^3
vapdensity = 0.5;     % water vapour density in g/m^3
P = 101300;           % dry air pressure in Pa
apathloss = 20*(log10(R/1e3)+log10(freq/1e9)) + 92.45;
rainloss = rainpl(R,freq,rainrate,el,tau);
fogloss = fogpl(R,freq,T,waterdensity);
gasloss = gaspl(R,freq,T,P,vapdensity);
totalloss = apathloss + rainloss + fogloss + gasloss;
totalgain = 46.99+30+24.77;
cableloss = 7;
receivedpower=totalgain-cableloss-totalloss;
plot(R/1e3,receivedpower);
xlabel("Distance (km)");
ylabel("Received Power (dB)");
title("Received Power vs Distance");
