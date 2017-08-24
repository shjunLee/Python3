import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup


def store(name, star):
    cur.execute('insert into top250 (name,star) values (%s,%s)', (name, star))
    cur.connection.commit()  # 执行储存过程

if __name__ == '__main__':

    # 建立数据库连接
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           charset='utf8mb4', passwd='123456')
    cur = conn.cursor()
    cur.execute("USE scraping")
    cur.execute("DROP TABLE IF EXISTS top250")
    cur.execute(
        "create table top250(id int(9) auto_increment,name varchar(30),star varchar(30),key(id))")
    try:
        for page in range(0, 250, 25):
            url = 'https://movie.douban.com/top250?start=' + \
                str(page)+'&amp;filter='
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            for link in soup.find_all("div", {"class": "info"}):
                name = link.div.a.span.get_text()
                #.next_sibling结果往往是标签之间的顿号和换行符，所以用两个
                star = link.div.next_sibling.next_sibling.find(
                    'span', {'class': 'rating_num'}).get_text()
                store(name, star)
    finally:
        cur.close()  # 关闭连接，不能忘
        conn.close()
