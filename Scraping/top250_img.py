import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

directory = 'C:/Users/lishe/Desktop/Top250_imgs/'
rank = 0
if not os.path.exists(directory):
    os.makedirs(directory)
if __name__ == "__main__":
    for page in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start='+str(page)+'&amp;filter='
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.find_all("div", {"class": "info"}):
            rank += 1
            names = link.div.a.span.get_text()
            img_src = link.previous_sibling.previous_sibling.img.get('src')            
            urlretrieve(img_src, directory+str(rank)+'_'+names+'.jpg')