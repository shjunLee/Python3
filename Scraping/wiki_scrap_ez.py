from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
pattern = re.compile("^(/wiki/)((?!:).)*$")  # 正则
for link in bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=pattern):
    # link.attrs是个字典，link在列表中
    # link.attrs表示访问link的attrs属性
    if 'href' in link.attrs:
        print(link.attrs['href'])
