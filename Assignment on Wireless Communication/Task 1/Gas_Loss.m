P = 101300;         % dry air pressure in Pa
vapdensity = 0.5;   % water vapour density in g/m^3
gasloss = gaspl(R,freq,T,P,vapdensity);
plot(freq/1e9,gasloss); 
grid on;
xlabel('Frequency (GHz)');
ylabel('Atmospheric Gas Attenuation (dB)')
title('Atmospheric Gas Attenuation');