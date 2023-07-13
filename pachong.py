# -*- coding: utf-8 -*- 
# Software: PyCharm
# Author: df
# CreateTime: 2022-08-05 14:29
# file: pachong.py
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定url,获取网页数据 ，
from urllib import parse  # 用来解析web需要的字符串
import json
import pymysql  # mysql操作


def main():
    serach = "java开发"
    # 处理中文字符搜索问题
    # keysword=parse.quote(serach)
    # 再进行转义才能达到链接里的效果：java%25E5%25BC%2580%25E5%258F%2591
    # 二次编码
    # newkeyword=parse.quote(keysword)
    dataList = getData()
    saveDB(dataList)


def askurl(url):
    # 模拟浏览器头部信息，像对应的url发送信息
    # 有时候403就放cookie就好使了
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }
    request = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        reponse = urllib.request.urlopen(request);
        # 这里51job界面是gbk的模式，如果这里用utf-8则报错，为： 'utf-8' codec can't decode byte 0xa1 in position 293: invalid start byte
        html = reponse.read().decode("gbk")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html;


# 获取并解析数据
def getData():
    # htmlx=open("51job.html","r")
    # bs=BeautifulSoup(htmlx,"html.parser")
    # ss=bs.select("div")
    # print(bs)
    serach = "java开发"
    keysword = parse.quote(parse.quote(serach))
    page = 0

    totalDataList = []

    # 循环分页处理，当查询不到数据就跳出循环
    while True:
        page = page + 1;
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99," + keysword + ",2," + str(page) + ".html"
        html = askurl(url)
        print("baseUrl", url)

        # 得到脚本数据里需要的数据,得到的数据就是一整个列表，取出下标0则可以进行遍历
        datas = re.findall('window.__SEARCH_RESULT__ =(.*?)</script>', str(html))[0]
        # 转换json可以根据键值对获取数据
        json_data = json.loads(datas)
        engines = json_data['engine_jds']

        # 跳出死循环
        if len(engines) == 0:
            break

        for engine in engines:
            dataGroup = []
            # 招聘职位
            if engine.get("job_name") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("job_name"))
            # 公司名称
            if engine.get("company_name") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("company_name"))
            # 薪资范围
            if engine.get("providesalary_text") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("providesalary_text"))
            # 地点
            if engine.get("workarea_text") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("workarea_text"))
            # 公司类型
            if engine.get("companytype_text") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("companytype_text"))
            # 学历要求
            if engine.get("degreefrom") == "":
                dataGroup.append("0")
            else:
                dataGroup.append(engine.get("degreefrom"))
            # 工作年限
            if engine.get("workyear") == "":
                dataGroup.append("0")
            else:
                dataGroup.append(engine.get("workyear"))
            # 公司福利
            if engine.get("jobwelf") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("jobwelf"))

            # 公司规模
            if engine.get("companysize_text") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("companysize_text"))

            # 公司经营方向
            if engine.get("companyind_text") == "":
                dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("companyind_text"))

            # 发布时间
            if engine.get("updatedate") == "":
                    dataGroup.append(" ")
            else:
                dataGroup.append(engine.get("updatedate"))


            totalDataList.append(dataGroup)
    return totalDataList


def saveDB(dataList):
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db='spider', charset="utf8")
    cursor = conn.cursor()

    try:
        for data in dataList:
            for index in range(len(data)):
                if index == 6 or index == 5:
                    continue
                data[index] = '"' + str(data[index]) + '"'

            sql = '''insert into 51job (job_name,company_name,providesalary_text,workarea_text,companytype_text,degreefrom,workyear,jobwelf,companysize_text,companyind_text,updatedate)
            values(%s)'''% ",".join(data)
            print(sql)
            cursor.execute(sql)
        print("保存成功")
    except Exception as result:
        print(result)
        conn.rollback()
    finally:
        conn.commit()
        cursor.close()
        conn.close()



def test():
   ss={"name":""}
   print(ss.get("name"))
   if ss.get("name")=="":
       print("pp")


if __name__ == "__main__":
    #test()
    main()
    # parserData("")
