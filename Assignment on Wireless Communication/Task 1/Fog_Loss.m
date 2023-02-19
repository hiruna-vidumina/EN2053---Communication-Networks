T = 31;                      % 31 degree Celsius
waterdensity = 0.5;          % liquid water density in g/m^3
fogloss = fogpl(R,freq,T,waterdensity)';
plot(freq/1e9,fogloss); 
grid on;
xlabel('Frequency (GHz)');
ylabel('Fog Attenuation (dB)')
title('Fog Attenuation');