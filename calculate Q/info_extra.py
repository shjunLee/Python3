from scipy.optimize import curve_fit
from scipy import signal
import numpy as np
from numpy import fft, linspace
from math import pi
import csv
import matplotlib.pyplot as plt
T_WIDTH_MIN = 1e-6
T_WIDTH_MAX = 2e-4


def lorentz(x, a, w, y0, xc):
    '''
    洛伦兹函数
    '''
    return y0 + (2*a/pi)*w/(4*(x-xc)**2+w**2)


def line(x, a, b):
    '''
    线性函数
    '''
    return a*x + b


class CsvData:

    def __init__(self, format_path):
        with open(format_path) as f:
            f_csv = csv.reader(f)
            x = np.array([float(row[3]) for row in f_csv])
            f.seek(0)
            y = np.array([float(row[4]) for row in f_csv])
            self.x = x
            self.y = y

    def plot(self, mark='ro'):
        plt.plot(self.x, self.y, mark, markersize=1)
        hight = max(self.y) - min(self.y)
        ymin = min(self.y) - hight/10
        ymax = max(self.y) + hight/10
        plt.ylim(ymin, ymax, '.')
        plt.xlabel('time(s)')
        plt.ylabel('voltage(V)')
        plt.show()

    def spectrum(self):
        N = len(self.x)
        dt = self.x[1] - self.x[0]
        fs = 1/dt
        yf = fft.fft(self.y)
        yf_abs = fft.fftshift(abs(yf))
        axis_yf = linspace(-fs/2, fs/2, num=N)
        plt.plot(axis_yf, yf_abs)
        plt.xlabel('Frequency/Hz')
        plt.ylabel('Amplitude')
        plt.title('Spectrum figure')
        plt.show()

    def filter(self, order, fc, mode='low'):
        N = len(self.x)
        fs = 1/(self.x[1]-self.x[0])
        if mode == 'low':
            b, a = signal.butter(order, fc*2/fs, 'low')
            sf = signal.filtfilt(b, a, self.y)
        elif mode == 'high':
            b, a = signal.butter(4, 0.0003, 'high')
            sf = signal.filtfilt(b, a, self.y)
        elif mode == 'bandpass':
            b, a = signal.butter(order, 0.00096, 'low')
            sf = signal.filtfilt(b, a, self.y)
            b, a = signal.butter(4, 0.0003, 'high')
            sf = signal.filtfilt(b, a, sf)
        else:
            print('无效的‘mode’值')
            return None
        self.y = sf
        return 1


class LorentzData(CsvData):

    def lorentz_curve(self):
        ymax = max(self.y)
        ymin = min(self.y)
        wmin = T_WIDTH_MIN
        wmax = T_WIDTH_MAX
        amax = (ymin - ymax)*pi*wmin/2
        amin = (ymin - ymax)*pi*wmax/2
        n0 = np.where(self.y == ymin)[0][0]
        xcmin = self.x[n0] - wmax
        xcmax = self.x[n0] + wmax
        popt, pcov = curve_fit(lorentz, self.x, self.y, bounds=(
            [amin, wmin, (ymin+ymax)/2, xcmin], [amax, wmax, ymax, xcmax]))
        a = popt[0]
        w = popt[1]
        y0 = popt[2]
        xc = popt[3]
        return a, w, y0, xc

    def cut_xy(self, w, xc, width=20):
        '''
        裁剪出x在xc附近的部分
        x是等差的
        '''
        x_left = self.x[0] if (
            xc - width*w/2) < self.x[0] else (xc - width*w/2)
        x_right = (xc + width*w/2) if (xc + width *
                                       w/2) < self.x[-1] else self.x[-1]
        p_left = int((x_left - self.x[0])//(self.x[1]-self.x[0]))
        p_right = int((x_right - self.x[0])//(self.x[1]-self.x[0]))
        self.x, self.y = self.x[p_left:p_right], self.y[p_left:p_right]

    def lorentz_new(self, alp=0.04):
        a, w, y0, xc = self.lorentz_curve()
        x_convert = alp*self.x
        y_convert = self.y/y0
        a_n = a*alp/y0
        w_n = alp*w
        y0_n = 1
        xc_n = alp*xc
        self.x, self.y = x_convert, y_convert
        self.cut_xy(w=w_n, xc=xc_n, width=20)
        a_n, w_n, y0_n, xc_n = self.lorentz_curve()
        return self.x, self.y, a_n, w_n, y0_n, xc_n


class MzData(CsvData):

    def mz_time(self, order, fc, mode='low'):
        self.filter(order, fc, mode)
        N = len(self.x)
        mid = int(N/2)
        dt = (max(self.x)-min(self.x))/(N-1)
        fs = 1/dt
        i = 1
        peak_index = []
        while i < N-1:
            if (self.y[i] > self.y[i-1]) and (self.y[i] > self.y[i+1]):
                peak_index.append(i)
                plt.plot(self.x[i], self.y[i], 'ro', color='red')
            i += 1
        t = (peak_index[-1] - peak_index[0]) * dt / (len(peak_index)-1)
        print('peak_index={}'.format(peak_index))
        plt.plot(self.x, self.y, '.', color='blue', markersize=0.5)
        plt.xlabel('Time(s)')
        plt.ylabel('Voltage(V)')
        plt.title('MZ data')
        plt.show()
        return t
