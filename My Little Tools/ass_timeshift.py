import re
import codecs  # 防止中文乱码
import os


def add_60(num, step=0):
    '''
    60进制加法
    '''
    num += step
    step = 0
    while True:
        if num >= 0 and num < 60:
            break
        else:
            if num < 0:
                num += 60
                step -= 1
            elif num >= 60:
                num -= 60
                step += 1
    return (num, step)


def two_num(num=0):
    '''
    1-->'01'
    59-->'59'
    '''
    if num < 10:
        return '0'+str(num)
    else:
        return str(num)


def time_add(timestr, shift=0):
    '''
    time_add是时分秒加法函数
    -60.0<shif<60.0,timestr时间字符串'x:xx:xx.xx'
    返回新时间字符串
    '''
    sec = float(timestr[-5:])
    (newsec, step) = add_60(sec, shift)
    newsec = round(newsec, 2)
    mini = int(timestr[-8:-6])
    (newmin, step) = add_60(mini, step)
    newhour = int(timestr[:-9]) + step
    newsec_str = two_num(newsec)
    newmin_str = two_num(newmin)
    if len(newsec_str) == 4:  # 防止出现54.0这种情况
        newsec_str = newsec_str + '0'
    return str(newhour) + ':' + newmin_str + ':' + newsec_str


def adjust(line, pattern, shift):
    '''
    adjust是用新的时间字符替换原字符串中旧的时间字符函数
    lines:输入的字符串
    pattern:正则表达式
    shift:加的秒数
    '''
    timelist = re.findall(pattern, line, flags=0)
    for timestr in timelist:
        new_timestr = time_add(timestr, shift)
        line = line.replace(timestr, new_timestr, 1)
    return line


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
    return formatpath


def get_newpath(formatpath):
    '''
    得到修改后字幕的保存路径
    '''
    pathlist = formatpath.split('/')
    newname = 'new_' + pathlist[-1]
    pathlist.pop(-1)
    pathlist.append(newname)
    newpath = '/'.join(pathlist)
    return newpath

if __name__ == '__main__':
    pattern = '[0-1]{1,2}:[0-5][0-9]:[0-5][0-9]\.[0-9]{2}'
    path = input('把字幕文件拖入:')
    path = windows_path(path)
    newpath = get_newpath(path)
    shift = float(input('输入字幕时间轴位移秒数:'))
    try:
        f = codecs.open(path, 'r', 'utf_8_sig')
        nf = codecs.open(newpath, 'w', 'utf_8_sig')
        for line in f:
            newline = adjust(line, pattern, shift)
            nf.write(newline)
    except Exception as e:
        print('Failed!')
        print(e)
    else:
        print('Successed!')
    finally:
        f.close()
        nf.close()
    os.system('pause')
