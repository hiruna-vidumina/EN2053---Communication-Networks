R = 10e3;                % 10 km range
rainrate = 20;           % rain rate in mm/h
el = 0;                  % 0 degree elevation
tau = 0;                 % horizontal polarization
rainloss = rainpl(R,freq,rainrate,el,tau)';
plot(freq/1e9,rainloss); 
grid on;
xlabel('Frequency (GHz)');
ylabel('Rain Attenuation (dB)')
title('Rain Attenuation ');