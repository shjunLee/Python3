from urllib.request import urlopen
from bs4 import BeautifulSoup


num = 0
top250 = []
if __name__ == '__main__':
    for page in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start='+str(page)+'&amp;filter='
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.find_all("div", {"class": "info"}):
            names = link.div.a.span.get_text()
            #.next_sibling结果往往是标签之间的顿号和换行符，所以用两个
            stars = link.div.next_sibling.next_sibling.find(
                'span', {'class': 'rating_num'}).get_text()
            top250.append((stars, names))

    top250.sort()
    top250.sort(reverse=True)
    for (star, name) in top250:
        num += 1
        print('Top'+str(num)+':'+name+' '+star)
