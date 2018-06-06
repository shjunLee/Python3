import matplotlib.pyplot as plt
import numpy as np
import csv
from info_extra import AnisData, lorentz

try:
    lda = input('输入波长(默认值为1560):')
    lda = lda.strip()
    lda = round(float(lda), 2)
except Exception as e:
    print(e)
    print('已默认波长为1560nm')
    lda = 1560


def remove_empety(alist):
    '''
    去除列表中的空元素
    '''
    while '' in alist:
        alist.remove('')
    return alist


def windows_path(path):
    '''
    格式化windows系统下文件路径
    '''
    path = path.strip()  # 去掉两端空格
    pathlist = path.split('\\')
    pathlist = remove_empety(pathlist)
    newpath = '/'.join(pathlist)
    pathlist = newpath.split('/')
    pathlist = remove_empety(pathlist)
    formatpath = '/'.join(pathlist)
    try:
        formatpath = eval(formatpath)
    except Exception as e:
        pass
    finally:
        return formatpath


def lorentz_data():
    # location = input('拖入洛伦兹线型csv文件或输入其地址:')
    location = "D:/Temp/q/1569.3_Ch1.csv"
    location =  windows_path(location)   
    print(location)
    with open(location) as f:
        f_csv = csv.reader(f)
        x = np.array([float(row[3]) for row in f_csv])
        f.seek(0)
        y = np.array([float(row[4]) for row in f_csv])
        return x, y


def line_data():
    # location = input('拖入锯齿波线型csv文件或输入其地址:')
    location = "D:/Temp/q/1569.3_Ch2.csv"
    location =  windows_path(location) 
    with open(location) as f:
        f_csv = csv.reader(f)
        x = np.array([float(row[3]) for row in f_csv])
        f.seek(0)
        y = np.array([float(row[4]) for row in f_csv])
        return x, y


def mz_data():
    # location = input('拖入mz干涉仪波形csv文件或输入其地址:')
    location = "D:/Temp/q/1569.3_Ch3.csv"
    location =  windows_path(location) 
    with open(location) as f:
        f_csv = csv.reader(f)
        x = np.array([float(row[3]) for row in f_csv])
        f.seek(0)
        y = np.array([float(row[4]) for row in f_csv])
        return x, y


def cut_xy(x, y, w, xc, width=20):
    '''
    裁剪出x在xc附近的部分
    x是等差的
    '''
    x_left = x[0] if (xc - width*w/2) < x[0] else (xc - width*w/2)
    x_right = (xc + width*w/2) if (xc + width*w/2) < x[-1] else x[-1]
    p_left = int((x_left - x[0])//(x[1]-x[0]))
    p_right = int((x_right - x[0])//(x[1]-x[0]))
    return x[p_left:p_right], y[p_left:p_right]


x_l, y_l = lorentz_data()
peak = AnisData(x_l, y_l)
a, w, y0, xc = peak.lorentz_curve()
x_l, y_l = cut_xy(x=x_l, y=y_l, w=w, xc=xc, width=20)
peak = AnisData(x_l, y_l)
a, w, y0, xc = peak.lorentz_curve()

x, y = line_data()
line = AnisData(x, y)
k, b = line.line_curve()

x, y = mz_data()
mz = AnisData(x, y)
t = mz.mz_time()


def piezoelectric(lam=lda):
    '''
    求压电系数
    '''
    return abs(lam*lam*1e-9/(2.88*k*t))


def lorentz_new(alp=0.04):
    x_convert = alp*k*x_l
    y_convert = y_l/y0
    a_n = a*alp*k/y0
    w_n = alp*k*w
    y0_n = 1
    xc_n = alp*k*xc
    return x_convert, y_convert, a_n, w_n, y0_n, xc_n


def main(lam=lda):
    alp = piezoelectric()
    x_convert, y_convert, a_n, w_n, y0_n, xc_n = lorentz_new(alp)
    yvals = lorentz(x_convert, a_n, w_n, 1, xc_n)
    plt.plot(x_convert, y_convert, 'ro', color='red',
             markersize=1, label="Original Data")
    plt.plot(x_convert, yvals, 'r', color='black', label='Fitting Curve')
    plt.legend(loc='lower right')
    plt.xlabel(r'$\Delta\,\lambda\ (nm)$')
    plt.ylabel('T')
    plt.title('result')
    T = round(lorentz(xc_n, a_n, w_n, 1, xc_n), 3)
    Q = 2*lam/(w_n*(1+np.sqrt(T)))
    Q = round(Q/1e8, 2)
    plt.text(min(x_convert), T, "T = {}\nPiezo = {}\nk = {}\nQ = {}$\\times10^8$".format(
        T, round(alp, 4), round(k, 2), Q), size=15, alpha=0.7)
    print('Tmz={}, alp={}'.format(t, alp))
    plt.show()


if __name__ == '__main__':
    main()
