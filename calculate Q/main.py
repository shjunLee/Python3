import matplotlib.pyplot as plt
from numpy import sqrt
from info_extra import LorentzData, MzData
from info_extra import lorentz

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


def main(lam=lda):
    lorentz_path = "D:/Temp/q/1569.3_Ch1.csv"
    lorentz_data = LorentzData(lorentz_path)
    mz_path = "D:/Temp/q/1569.3_Ch3.csv"
    mz_data = MzData(mz_path)
    # mz_data.spectrum()
    t = mz_data.mz_time(6, 4000, 'low')
    print(t)
    # mz_data.spectrum()
    alp = abs(lam*lam*1e-9/(2.88*t))
    x_convert, y_convert, a_n, w_n, y0_n, xc_n = lorentz_data.lorentz_new(alp)
    yvals = lorentz(x_convert, a_n, w_n, 1, xc_n)
    T = round(lorentz(xc_n, a_n, w_n, 1, xc_n), 3)
    Q = 2*lam/(w_n*(1 + sqrt(T)))
    Q = round(Q/1e8, 3)
    plt.plot(x_convert, y_convert, 'ro', color='red',
             markersize=1, label="Original Data")
    plt.plot(x_convert, yvals, 'r', color='black', label='Fitting Curve')
    plt.legend(loc='lower right')
    plt.xlabel(r'$\Delta\,\lambda\ (nm)$')
    plt.ylabel('T')
    plt.title('result')
    plt.text(min(x_convert), T, "T_mz = {}ms\nQ = {}$\\times10^8$".format(
        round(t*1000, 2), Q), size=15, alpha=0.7)
    plt.show()


if __name__ == '__main__':
    main()
