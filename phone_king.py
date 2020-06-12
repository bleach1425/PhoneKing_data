import requests
import jieba
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
# 取得bs
client = MongoClient('mongodb+srv://Rubio:bleach0507@cluster0-kvjio.gcp.mongodb.net/news?retryWrites=true&w=majority')
db = client['news']
collection_currency = db['news1']
def get_bs():
    header_data = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    r = requests.get("https://www.sogi.com.tw/articles",
                     headers=header_data,
                     params={

                     }
                     )
    r.encoding = "utf-8"
    bs = BeautifulSoup(r.text, "html.parser")
    return bs

# 取得超連結
def get_href(bs):
    title = get_bs().find_all("a", {"class": "text-black font-weight-bold text-row-2"})
    href = []
    for q in title:
        df = q.get("href")
        href.append(df)
    return href
# 取得標標題
def get_title(bs,href):
    comment_title = []
    for i in href:
        header_data = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        }
        r = requests.get(f"https://www.sogi.com.tw{i}",
                     headers=header_data,
                     params={

                     }
                     )
        r.encoding = "utf-8"
        bs1 = BeautifulSoup(r.text, "html.parser")
        title = bs1.find_all("h1", {"class": "h1"})
        for i in title:
            comment_title.append(i.text)
# print(comment_title)
    return comment_title

def get_bs_content(bs,href):
    content_list=[]
    for i in href:
        header_data = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
        }
        r = requests.get(f"https://www.sogi.com.tw{i}",
                     headers=header_data,
                     params={

                     }
                     )
        r.encoding = "utf-8"
        bs2 = BeautifulSoup(r.text, "html.parser")
        content = bs2.find_all("div",{"class":"editable my-2"})
        for i in content:
            content_list.append(i.text)
    return content_list

def get_picture(bs):
    src_list=[]
    header_data = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    }
    r = requests.get("https://www.sogi.com.tw/article",
                     headers=header_data,
                     params={

                     }
                     )
    r.encoding = "utf-8"
    bs2 = BeautifulSoup(r.text, "html.parser")
    picture = bs.find_all("img",{"class":"card-img card-img-fit js-lazy"})
    # print(picture)
    for d in picture:
        src_list.append(d.get("data-original"))
    return src_list

def __main__():
    bs = get_bs()
    href = get_href(bs)
    href_list=[]
    for q in href:
        final = f"https://www.sogi.com.tw{q}"
        href_list.append(final)
    # url = https://www.sogi.com.tw/articles
    title = get_title(bs,href)
    content = get_bs_content(bs,href)
    picture = get_picture(bs)

    dict = {
        "title":title[0:10],
        "content":content[0:10],
        "href":href_list[0:10],
        "picture":picture[0:10]
    }
    return dict


if __name__ == '__main__':
    x = __main__()
    collection_currency.insert_one(x)


