from ast import Not
from cgitb import html 
from email import header
from http import cookies
from importlib.util import decode_source
from msilib.schema import Class
from pydoc import classname
from socket import timeout
import sys
import math
from time import sleep, time
from wsgiref import headers
from bs4 import BeautifulSoup  #网页解析,获取数据
import re #正则表达式,进行文字匹配
import urllib.request,urllib.error
import requests
from pip import main #制定URL,获取网页数据
from getCookies import getCookie  
from core.RedisModel import connection

findName = re.compile(r'<span class="a-profile-name">(.*?)</span>') #评价用户名称
findStarts = re.compile(r'<span class="a-icon-alt">(.*?)</span>') #评价星级
findTitle = re.compile(r'<span>(.*?)</span>') #评价标题
findTime = re.compile(r'<span.+review-date[^>]*>([^<]*)</span>') #评价时间
findGoodsConfig = re.compile(r'<a.+format-strip[^>]*>([^<]*)</a>') #评价商品配置
findContent = re.compile(r'data-hook="review-body.*[\n]*<span>(.*?)</span>') #评价内容
findReviewsTotal = re.compile(r'.*ratings,(.*?)with reviews') #评论总数

theOriginalUrl = 'https://www.amazon.com';
#redis cookie key 
cookieKey = 'SPIDER:COOKIES'
#page num
pageNum = 10

def main():
    objUrl = 'https://www.amazon.com/Hiseeu-%E5%A4%9A%E5%8A%9F%E8%83%BD%E6%A9%9F%E9%AB%94%EF%BC%8C12-%E8%9E%A2%E5%B9%95%E7%84%A1%E7%B7%9A%E5%AE%89%E5%85%A8%E6%94%9D%E5%BD%B1%E6%A9%9F%E7%B3%BB%E7%B5%B1%EF%BC%8C%E5%AE%B6%E5%BA%AD%E5%95%86%E5%8B%99-1080P-%E5%A4%9C%E9%96%93%E9%98%B2%E6%B0%B4%EF%BC%8C3TB/dp/B07T8ZDTTP/ref=sr_1_2_sspa?keywords=hiseeu&qid=1659496451&sr=8-2-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFGOU40Q0lTMFRPOVQmZW5jcnlwdGVkSWQ9QTA4MjA4MzUyWlo2NlFEVFFUT0dVJmVuY3J5cHRlZEFkSWQ9QTAwNTM4MDgxSzgwN1hETzhBM1I1JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1';
    #1、获取商品页html
    html = askUrl(objUrl) 
    soup = BeautifulSoup(html,'html.parser') 
    #2、获取商品标识ASIN
    asin = getGoodAsin(soup)
    if not asin:
        print('asin get fail ! update cookie')
        #更新cookie
        updateCookies() 
        #重新获取商品标识
        asin = getGoodAsin(soup)
        if not asin:
            sys.exit('asin get fail!')
    #3、获取更多评论的url
    moreUrl = getMoreUrl(html)
    if not moreUrl:
        sys.exit('moreUrl get fail!')
    #4、爬取所有评论信息
    getData(moreUrl)

def getData(url,i=1):
    """
    开始爬取需要存库的评论信息
    """
    html = askUrl(url)
    soup = BeautifulSoup(html,'html.parser')
    #评论总数
    reviewsTotal = soup.find('div',class_='a-row a-spacing-base a-size-base')
    reviewsTotal = re.findall(findReviewsTotal,str(reviewsTotal))[0]
    if reviewsTotal:
        reviewsTotal = reviewsTotal.strip().replace(',','')
    else:
        print('not defind reviewsTotal!')
        return
    #评论总页数
    pageTotal = math.ceil(int(reviewsTotal)/10)
    #所有评论
    for item in soup.find_all('div',class_='a-section review aok-relative'):
        #转为字符串
        item = str(item) 
        #查找用户名称
        name = re.findall(findName,item)[0]
        #查找评价星级
        starts = re.findall(findStarts,item)[0]
        #查找评价标题
        title = re.findall(findTitle,item)[0]
        #查找评价时间
        time = re.findall(findTime,item)
        #查找商品配置
        goodsConfig = re.findall(findGoodsConfig,item)
        #查找用户评价
        content = re.findall(findContent,item)
        #print(name,starts)
    #获取下一页url
    nextUrl = getNextUrl(soup)
    if 'None' == nextUrl :
        #没有下页,结束
        print('no next page!')
    else:
        sleep(0.5) 
        #还有下一页,递归获取下一页
        i += 1
        getData(nextUrl,i)
    
def getGoodAsin(soup):
    """
    获取商品标识
    """
    try:    
        #获取页面下部份html
        asin = soup.find('input', attrs={'id':'ASIN'})['value']
        return asin
    except:
        return False

#获取商品页的更多商品评论url
def getMoreUrl(html): 
    try:  
        soup = BeautifulSoup(html,'html.parser') 
        #获取页面下部份html
        bottom =  soup.find('div',id='reviews-medley-footer')
        sort = bottom.find('a',class_='a-link-emphasis a-text-bold')
        moreUrl = sort.get('href')
        print(moreUrl)
        return (theOriginalUrl+moreUrl)
    except:
         return False

#获取下一页url
def getNextUrl(soup):
    try:
        list = soup.find('div',id='cm_cr-pagination_bar')
        nextList = list.find('li',class_='a-last')
        nextATag = nextList.find('a')
        nextUrl = nextATag.get('href')
        return nextUrl
    except:
        return False

#获取指定url的html代码
def askUrl(url): 
    #redis有问题
    print('staring to get cookie...')
    cookies = getCookies() 
    print('cookie:',cookies)
    #头部信息
    head = { 
        'cookie' : cookies,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }  
    try:
        res = requests.get(url,headers=head,verify=False,timeout=10)  
        return res.text
    except requests.exceptions.RequestException as e:
        sys.exit(e)

def updateCookies():
    """
    更新cookie
    """
    cookies = getCookie()
    #连接redis
    redis = connection() 
    res = redis.set(cookieKey,cookies,ex=30) 
    if not res:
        sys.exit('update cookie fail!')

def getCookies():
    """
    获取cookie
    """
    redis = connection()
    cookies = redis.get(cookieKey) 
    print('to get cookies...:',cookies)
    if None == cookies:  
        print('refetching get cookie...')
        cookies = getCookie()
        redis.set(cookieKey,cookies,ex=30)
    return cookies


if __name__ == '__main__':
    print('start...')
    #调用main方法   
    main()
    print('end...')