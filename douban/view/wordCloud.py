# -*- coding: utf-8 -*- 
# Software: PyCharm
# Author: df
# CreateTime: 2022-08-03 18:01
# file: testimg.py

import sqlite3

import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化，生成图片
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算


# 词云的应用
def word():
    con = sqlite3.connect("../movie.db")
    cur = con.cursor()
    sql = "select instroduction from movie250"
    datas = cur.execute(sql);
    text = ""
    # 查询出来以后是元组
    for data in datas:
        text = text + data[0]

    cur.close()
    con.close()

    # 将中文分词
    cut=jieba.cut(text);
    string=" ".join(cut)

    img=Image.open(r".\static\assets\img\tree.jpg") # 打开需要词云填充的背景图片
    img_array=np.array(img) # 将图片转换为数组
    # backgroud_color：背景色为白色
    # mask:遮罩物为图片数组
    # font_path：显示字体
    wc=WordCloud(
        background_color='white',
        mask=img_array,
        font_path='simfang.ttf'  # 去c:\Windows\Fonts
    )
    # 测试中一直在 wc.generate_from_text(string)报错打开不了资源，原因是字体路径问题,字体路径去c:\Windows\Fonts选中一个图片右键属性就能查到英文名字

    # 根据分词生成想要的遮罩物
    wc.generate_from_text(string)
    #绘制图片
    fig=plt.figure(1)
    # 用词云方式显示
    plt.imshow(wc) # 用plt显示图片
    plt.axis('off') # 不显示坐标轴
    #plt.show() # 显示图片
    # 保存图片，dpi=500是分辨率
    plt.savefig(r".\static\assets\img\word.jpg",dpi=500)


word()
