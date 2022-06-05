fileID = fopen('demod_out_A_Normal_2.txt');
C = textscan(fileID, '%s %s');
fclose(fileID);
Time = str2double(C{1}(2:end));
Value = (((str2double(C{2}(2:end)))/5)+1)/2;

n = 1;
X = [];
Y = [];
while n <= length(Value)-15
    if Value(n) == 1 && Value(n+12) == 0 && Value(n+13) == 0 && Value(n+14) == 0 && Value(n+15) == 1
        b = [];
        p = 0;
        for i = 1:10
            b(end+1) = Value(n+i);
            p = p+Value(n+i);
        end
        X(end+1) = Time(n);
        if Value(n+11) == mod(p, 2)
            Y(end+1) = bi2de(b, 'left-msb');
        else
            Y(end+1) = 0;
        end
    end
    n = n+16;
end
Y = (Y/1023)*5;

fc1 = 10;
fc2 = 450;
fc3 = 20;
fs = 2000;
[b1, a1] = butter(4, fc1/(fs/2), 'high');
HPF10 = filtfilt(b1, a1, Y);
[b2, a2] = butter(4, fc2/(fs/2), 'low');
LPF450 = filtfilt(b2, a2, HPF10);
[b3, a3] = butter(2, fc3/(fs/2), 'high');
HPF20 = filtfilt(b3, a3, LPF450);
RS = abs(HPF20);
envelope = sqrt(movmean(RS.^2, 300));

window = 0.3;
m = 1;
SD = [];
u = [];
while window <= X()
    arr = [];
    while X(m) <= window
        arr(end+1) = RS(m);
        m = m+1;
    end
    clear std;
    clear mean;
    SD(end+1) = std(arr);
    u(end+1) = mean(arr);
    window = window + 0.3;
end
SDu = [SD; u];
[M, I] = min(SDu, [], 2, 'linear');
u_m = M(2,:);
h = 3;
SD_m = M(1,:);
Th_m = u_m + (h*SD_m);

l = 1;
ison = 0;
onctr = 0;
offctr = 0;
redline = [];
blueline = [];
while l <= length(envelope)-1
    if envelope(l) > Th_m && envelope(l+1) > Th_m && ison == 0
        onctr = onctr+1;
        if onctr == 74
            redline(end+1) = l;
            ison = 1;
            onctr = 0;
        end
    end
    if envelope(l) < Th_m && envelope(l+1) < Th_m && ison == 1
        offctr = offctr+1;
        if offctr == 74
            blueline(end+1) = l;
            ison = 0;
            offctr = 0;
        end
    end
    l = l+1;
end
RS = RS-Th_m;
for i = 1:length(RS)
    if RS(i) < 0
        RS(i) = 0;
    end
end

plot(X, RS);
xlabel('Time - seconds(s)');
ylabel('Voltage - Volts(V)');
for i = 1:length(redline)
    xline(X(redline(i)), 'r');
end
for i = 1:length(blueline)
    xline(X(blueline(i)), 'b');
end