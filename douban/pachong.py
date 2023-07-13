# -*- coding: utf-8 -*- 
# Software: PyCharm
# Author: df
# CreateTime: 2022-07-22 17:53
# file: pachong.py
import bs4  # 这个包帮助网页解析
from bs4 import BeautifulSoup
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定url,获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作


def main():
    baseUrl = "https://movie.douban.com/top250?start="
    # 1.获取网页,解析网页
    listdata = getData(baseUrl);
    # .是当前文件位置
    savepath = ".\\豆瓣电影250.xls"
    # 3.保存数据到xls
    # saveData(listdata,savepath);
    # 3.保存数据到sqlLite数据库
    dbpath = "movie.db"
    saveDataDB(listdata, dbpath)


# 查找href里的超链接
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则(字符串的模式)
# 查找影片图片的链接
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findReting = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 获取网页解析网页
def getData(baseUrl):
    datalist = []

    # 分页获取网页数据
    for i in range(0, 10):
        url = baseUrl + str(i * 25)
        html = askurl(url)
        # 2.解析数据
        soup = BeautifulSoup(html, "html.parser")
        # soup.find_all查找符合要求的字符串,div class=item的
        for item in soup.find_all("div", class_="item"):
            data = []  # 保存一部电影的所有信息
            item = str(item);
            # 影片详情链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)

            # 查找图片链接,返回列表形式
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)

            # 查找电影名称
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                # print(titles[1].replace("/",""))
                data.append(titles[0])  # 中文标题
                data.append(titles[1].replace("/", ""))  # 外国文字标题
            else:
                data.append(titles[0])
                data.append(' ')  # 占列表位置

            # 评分处理
            rating = re.findall(findReting, item)[0]
            data.append(rating)
            # 评价人数
            judgeNum = re.findall(findJudge, item)
            data.append(judgeNum)

            # 电影概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                data.append(inq[0].replace("。", ""))  # 替换句号
            else:
                data.append(' ')

            # 找到影片相关信息
            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)  # 去掉<br>
            bd = re.sub("/", " ", bd)  # 去掉/
            data.append(bd.strip())  # strip 去掉空格

            datalist.append(data)  # 将电影信息放入datalist列表里
    return datalist


# 得到指定都得url全部网页内容
def askurl(url):
    # 模拟浏览器头部信息，像对应的url发送信息
    # 有时候403就放cookie就好使了
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71",
        "Cookie": 'gr_user_id=2bcec40d-f13a-4f81-9c70-4aba12ddd43a; douban-fav-remind=1; bid=wJLz9aNwr5s; ll="108288"; __gads=ID=129a3248def8f913-2293ee8dcbd300c0:T=1654496070:RT=1654496070:S=ALNI_MbHoq9YqALPBO_UsgIHou-ZZS3VEA; viewed="3354490_35231266"; _vwo_uuid_v2=D9798EAC518ED33DC32733192E9E04616|6dcfcc3902177e8c6f8609fda00b660c; ct=y; dbcl2="260216152:hYzJDNMr7R4"; ck=kv3X; _pk_ref.100001.4cf6=["","",1659185145,"https://accounts.douban.com/"]; _pk_id.100001.4cf6=06f9011a3a51b7da.1658483919.4.1659185145.1658562481.; _pk_ses.100001.4cf6=*; __utma=30149280.724983395.1563864070.1658562305.1659185145.25; __utmb=30149280.0.10.1659185145; __utmc=30149280; __utmz=30149280.1659185145.25.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1153613921.1658483919.1658562305.1659185145.4; __utmb=223695111.0.10.1659185145; __utmc=223695111; __utmz=223695111.1659185145.4.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __gpi=UID=0000066310476515:T=1654496070:RT=1659185144:S=ALNI_MatE7NDm0vlBOlgfHDUz65simmHBg; push_noty_num=0; push_doumail_num=0'
    }
    request = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        reponse = urllib.request.urlopen(request);
        html = reponse.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html;


# 保存数据
def saveData(dataList, path):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)  # cell_overwrite_ok可支持重写
    col = ("电影详情链接", "图片链接", "影片中国名", "影片外国名", "评分", "评价数", "概况", "相关信息");
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 表头

    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = dataList[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(path)  # 保存文件里


# 将爬下来的数据保存数据库
def saveDataDB(dataList, path):
    #初始化数据库并建表
    init_db(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    for data in dataList:
        for index in range(len(data)):
            if index == 4:
                # 数字处理
                continue
            if index == 5:
                # 取出列表数据取出第一个，因为只有一个
                data[index] = data[index][0]
            else:
                data[index] = '"' + str(data[index]) + '"'
        sql = '''
               insert into movie250 (info_link,pic_link,cname,ename,score,rated,instroduction,info)
               values(%s)''' % ",".join(data)
        #print("sql=", sql)
        cur.execute(sql)
        conn.commit()
    print("数据存储库成功")
    cur.close()
    conn.close()


# 连接创建表
def init_db(path):
    sql = """
     create table movie250(
     id integer primary key autoincrement,
     info_link text ,
     pic_link text ,
     cname varchar,
     ename varchar,
     score numeric,
     rated numeric,
     instroduction  text,
     info text 
     )
    """;
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    # saveDataDB("movie.db")
