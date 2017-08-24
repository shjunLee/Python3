from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
pages = set()
"""
创建一个爬虫来收集页面标题、正文的第一个段落，
以及编辑页面的链接（如果有的话）这些信息。

1.所有的标题（所有页面上，不论是词条页面、编辑历史页面还是其他页面）都是在
h1→span标签里，而且页面上只有一个h1标签。
2.前面提到过，所有的正文文字都在div#bodyContent标签里。但是，如果我们想更
进一步获取第一段文字，可能用div#mw-content-text→p更好（只选择第一段的标签）。
这个规则对所有页面都适用，除了文件页面（例如，https://en.wikipedia.org/wiki/
File:Orbit_of_274301_Wikipedia.svg），页面不包含内容文字（content text）的部
分内容。
3.编辑链接只出现在词条页面上。如果有编辑链接，都位于li#ca-edit标签的
li#caedit→span→a里面。
"""


def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("页面缺少一些属性！不过不用担心！")

    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 我们遇到了新页面
                newPage = link.attrs['href']
                print("----------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")
