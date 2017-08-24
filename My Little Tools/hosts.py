import os
import shutil
"""
把hosts文件从桌面移动到windows系统hosts文件指定位置

"""

pass_old = 'C:\\Users\\lishe\\Desktop\\hosts'
pass_new = 'C:\\Windows\\System32\\drivers\\etc\\hosts'

try:
    shutil.move(pass_old, pass_new)
except Exception as e:
    print('Failed!')
    print(e)
else:
    print('Move hosts successfully!')
finally:
    del pass_new
    del pass_old

os.system("pause")
