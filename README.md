# 文本查重小程序
## 1.运行环境
>win10

>python 3.x

>gensim 3.4.0

>python-docx 0.8.7

>jieba 0.39

## 2.程序截图

<div align=center><img width="600" height="300" src="https://github.com/DQ0408/ArticleChecking/blob/master/imgs/Fig1.jpg"/></div>

#### <div align=center> Fig1.主界面 </div>

<div align=center><img width="600" height="300" src="https://github.com/DQ0408/ArticleChecking/blob/master/imgs/Fig2.jpg"/></div>

#### <div align=center> Fig2.查重结果界面 </div>

<div align=center><img width="600" height="300" src="https://github.com/DQ0408/ArticleChecking/blob/master/imgs/Fig3.jpg"/></div>

#### <div align=center> Fig3.导出的csv截图 </div>

## 3.思路

#### 读取.txt或.docx文档，提取其中的文字，丢弃文档中的图片，将所有文字20个一组切分，然后丢入百度查询。

<div align=center><img width="600" height="300" src="https://github.com/DQ0408/ArticleChecking/blob/master/imgs/Fig4.jpg"/></div>

#### <div align=center> Fig4.百度查询结果示例 </div>

#### 爬取查询结果中的每一段红字及其超链接，用tfidf模型计算与原句子的相似度，达到粗略查重的目的



