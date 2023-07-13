# -*- coding: utf-8 -*- 
# Software: PyCharm
# Author: df
# CreateTime: 2022-07-31 12:33
# file: app.py
import sqlite3

from flask import Flask, render_template

# render_template渲染网页的
app = Flask(__name__)  # 这是两条短线


# 路由解析，通过用户访问的路径，匹配相应的函数
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/movie')
def movie():
    dataList = []
    con = sqlite3.connect("../movie.db")
    cur = con.cursor()
    sql = "select * from movie250"
    datas = cur.execute(sql);
    for data in datas:
        dataList.append(data)
    cur.close()
    con.close()
    return render_template("movie.html", movies=dataList)


@app.route('/score')
def score():
    scores = []
    mNums = []
    con = sqlite3.connect("../movie.db")
    cur = con.cursor()
    sql = "select score,count(score) as count from movie250 group by score"
    datas = cur.execute(sql);
    for data in datas:
        scores.append(data[0])
        mNums.append(data[1])
    cur.close()
    con.close()
    return render_template("score.html", scores=scores, mNums=mNums)


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/word')
def word():
    return render_template("word.html")


if __name__ == '__main__':
    app.run(debug=True)
