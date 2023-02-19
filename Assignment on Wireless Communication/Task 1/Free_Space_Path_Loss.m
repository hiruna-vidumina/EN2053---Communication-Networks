R = 10e3;                  % distance in m
freq = (50:1000).'*1e9;    % frequency in Hz
apathloss = 20*(log10(R/1e3)+log10(freq/1e9)) + 92.45;   % free space path loss
plot(freq/1e9,apathloss);
grid on;
xlabel('Frequency (GHz)');
ylabel('Path Loss (dB)')
title('Free Space Path Loss')