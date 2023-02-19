% Free Space Path Loss Vs Freqency
R = 10e3;                  % distance in m
freq = (50:1000).'*1e9;    % frequency in Hz
apathloss = 20*(log10(R/1e3)+log10(freq/1e9)) + 92.45;   % free space path los
% Rain Attenuation Vs Freqency
R = 10e3;                % 10 km range
rainrate = 20;           % rain rate in mm/h
el = 0;                  % 0 degree elevation
tau = 0;                 % horizontal polarization
rainloss = rainpl(R,freq,rainrate,el,tau)';
% Fog Attenuation Vs Freqency
T = 31;                      % 31 degree Celsius
waterdensity = 0.5;          % liquid water density in g/m^3
fogloss = fogpl(R,freq,T,waterdensity)';
% Atmospheric Gas Attenuation Vs Freqency
P = 101300;         % dry air pressure in Pa
vapdensity = 0.5;   % water vapour density in g/m^3
gasloss = gaspl(R,freq,T,P,vapdensity);
% Total Path Loss Vs Frequency
totalloss = apathloss + rainloss + fogloss + gasloss;      %total path loss   
plot(freq/1e9,totalloss);
grid on;
xlabel("Frequency (GHz)");
ylabel("Total Path Loss (dB)");
title("Total Path Loss");
totalloss(1,1)
totalloss(2,1)
totalloss(50,1)
totalloss(51,1)
min(totalloss)
max(totalloss)
