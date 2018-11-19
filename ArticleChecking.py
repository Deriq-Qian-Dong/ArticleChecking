# -*- coding: utf-8 -*-
"""
Created on 2018/11/18 23:16
@author: Eric
@email: qian.dong.2018@gmail.com
"""
from gensim import corpora, models, similarities
from urllib.request import quote, urlopen
import tkinter.filedialog
from lxml import etree
from tkinter import *
import pandas as pd
import numpy as np
import tkinter
import jieba
import docx
import re
import os


def cut_text(text,lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr


def get_html(url1):
    ret1 = quote(url1, safe=";/?:@&=+$,", encoding="utf-8")
    res = urlopen(ret1)
    html = res.read().decode('utf-8')
    return html


def get_similarity_rate(all_doc, doc_test):
    p = ',.＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。''＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
    _doc_test = re.sub("[%s]+" % p, "", doc_test)
    _all_doc = [re.sub("[%s]+" % p, "", doc) for doc in all_doc]
    all_doc_list = []
    for doc in _all_doc:
        doc_list = [word for word in jieba.cut(doc)]
        all_doc_list.append(doc_list)
    doc_test_list = [word for word in jieba.cut(_doc_test)]
    dictionary = corpora.Dictionary([doc_test_list])
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    if max(sim) < 1e-5 and _all_doc[sim.tolist().index(max(sim))] in _doc_test:
        return [doc_test, all_doc[sim.tolist().index(max(sim))],
                round(len(_all_doc[sim.tolist().index(max(sim))]) / len(_doc_test), 3)]
    return [doc_test, all_doc[sim.tolist().index(max(sim))], round(max(sim), 3)]


def main():
    global file_name
    global similarity_rates
    try:
        f = open(file_name, encoding='utf-8')
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = "".join(lines)
        # lines = lines.split('。')
    except:
        document = docx.Document(file_name)
        lines = []
        for paragraph in document.paragraphs:
            if (len(paragraph.text.strip()) == 0):
                continue
            lines.append(paragraph.text.strip())  # 打印各段落内容文本
        lines = "".join(lines)
        # lines = lines.split('。')
    lines = cut_text(lines, 20)
    header = "http://www.baidu.com/s?wd="
    similarity_rates = []
    for line in lines:
        if (len(line) == 0):
            continue
        print(line)
        html = get_html(header + line)
        et_html = etree.HTML(html)
        # match_texts = et_html.xpath("//*[@id]/div[1]/em")
        urls = et_html.xpath('//*[@id]/h3/a/@href')
        url_no = len(urls)
        match_texts = {}
        for No in range(1, url_no+1):
            matchs = et_html.xpath('//*[@id="%d"]/div[1]/em' % No)
            for m in matchs:
                match_texts[m.text] = No-1
        ems = []
        for m_txt in match_texts:
            ems.append(m_txt)
        print(ems)
        try:
            tmp = get_similarity_rate(ems, line)
            match_em = tmp[1]
            tmp.insert(2, urls[match_texts[match_em]])
            similarity_rates.append(tmp)
        except:
            similarity_rates.append([line, str(ems), "无匹配链接", 0])
    similarity_rates = pd.DataFrame(similarity_rates)
    similarity_rates.columns = ['原句子', '最佳匹配', "最佳匹配链接", '相似度']


def select_file():
    global file_name
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text="您选择的文件是：" + filename)
        file_name = filename
    else:
        lb.config(text="您没有选择任何文件")


def save_result():
    global file_name
    global similarity_rates
    similarity_rates.to_csv(str(os.path.basename(file_name).split(".")[0])+"_查重结果.csv")
    print('done')


def show_result():
    global similarity_rates
    height = len(similarity_rates)
    width = 4
    temp = tkinter.Tk(className="result")
    temp.iconbitmap("icon.ico")
    print(similarity_rates)
    titles = ['原句子', '最佳匹配', '最佳匹配链接', '相似度']
    for j in range(width):  # Columns
        b = Label(temp, text=titles[j])
        b.grid(row=0, column=j)
    for i in range(1, height + 1):  # Rows
        for j in range(width):  # Columns
            if j == 3:
                b = Label(temp, text=str(np.array(similarity_rates)[i - 1][j])[0:4])
            else:
                b = Label(temp, text=str(np.array(similarity_rates)[i - 1][j]))
            b.grid(row=i, column=j)
    temp.mainloop()


if __name__ == "__main__":
    file_name = ""
    similarity_rates = None
    root = tkinter.Tk(className="文本查重")
    root.iconbitmap("icon.ico")
    root.geometry('500x200+500+200')
    lb = Label(root, text='')
    lb.pack()
    selectBtn = Button(root, text="选择文件", command=select_file)
    selectBtn.pack()
    checkBtn = Button(root, text="开始查重", command=main)
    checkBtn.pack()
    showBtn = Button(root, text="展示结果", command=show_result)
    showBtn.pack()
    saveBtn = Button(root, text="导出结果", command=save_result)
    saveBtn.pack()
    root.mainloop()
