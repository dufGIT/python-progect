# -*- coding: utf-8 -*- 
# Software: PyCharm
# Author: df
# CreateTime: 2022-07-31 12:33
# file: app.py
import sqlite3

from flask import Flask, render_template
import pymysql  # mysql操作

# render_template渲染网页的
app = Flask(__name__)  # 这是两条短线


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/list', methods=["GET"])
def list():
    dataList = []
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db='spider', charset="utf8")
    # 默认以元组方式返回，pymysql.cursors.DictCursor添加参数以字典方式返回
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from 51job"
    cursor.execute(sql)
    datas = cursor.fetchall()
    print(datas)
    for data in datas:
        dataList.append(data)
    cursor.close()
    conn.close()
    return render_template("list.html", dataList=dataList)


@app.route('/echart', methods=["GET"])
def echart():
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, db='spider', charset="utf8")
    # 默认以元组方式返回，pymysql.cursors.DictCursor添加参数以字典方式返回
    cursor = conn.cursor()
    #  where workarea_text like '%丰台%'
    sql = "select count(id),updatedate from 51job group by updatedate order by updatedate desc limit 30"
    cursor.execute(sql)
    datas = cursor.fetchall()

    sql1 = ''' 
SELECT
COUNT( CASE WHEN workyear = 1  THEN 1 ELSE NULL END ) AS '应届',
COUNT( CASE WHEN workyear = 2  THEN 1 ELSE NULL END ) AS '初级',
COUNT( CASE WHEN workyear = 3  THEN 1 ELSE NULL END ) AS '中级',
COUNT( CASE WHEN workyear = 4  or  workyear=7 THEN 1 ELSE NULL END ) AS '高级',
COUNT( CASE WHEN workyear = 5  THEN 1 ELSE NULL END ) AS '资深',
COUNT( CASE WHEN workyear = 6  THEN 1 ELSE NULL END ) AS '不限经验'
FROM 51job
    '''
    cursor.execute(sql1)
    datas1 = cursor.fetchall()

    updateNum = []
    updateDate = []
    for data in datas:
        updateNum.append(data[0])
        updateDate.append(data[1])

    grades = ["应届", "初级", "中级", "高级", "资深", "不限经验"]
    pies=[]
    index = 0;
    for data in datas1[0]:
        info = {}
        info["name"] = grades[index]
        info["value"] = data
        pies.append(info)
        index = index + 1

    print(pies)
    cursor.close()
    conn.close()
    return render_template("echart.html", updateNum=updateNum,
                           updateDate=updateDate,grades=grades,pies=pies)

if __name__ == '__main__':
    app.run(debug=True)
