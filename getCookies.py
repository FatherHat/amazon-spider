
from urllib import request
import requests
from bs4 import BeautifulSoup
from config.headers import getHeaders 
import ddddocr
from time import sleep

#请求头
header = getHeaders()
#验证界面地址
validateUrl = 'https://www.amazon.com/errors/validateCaptcha'

def getCookie():
    """
    获取Cookies
    """
    #请求验证码界面
    html = askUrl(validateUrl).content; 
    soup = BeautifulSoup(html,'html.parser')
    #获取验证码图片地址
    codeSrc = getCodeUrl(soup)
    #获取图片二进制流
    sleep(0.5)
    img_bytes = askUrl(codeSrc).content 
    #解析验证码
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(img_bytes) 
    #获取验证码发送地址
    requestVerifyUrl = getSendUrl(soup,code)
    #发送验证码
    sleep(1.5)
    verifyRes = askUrl(requestVerifyUrl)

    if 200 != verifyRes.status_code:
        #验证失败
        print('validation fails,return error code:'+verifyRes.status_code)
        return False
        
    #返回的cookie
    setCookie = verifyRes.headers['Set-Cookie']
    return setCookie

def getCodeUrl(soup):
    """
    获取验证码图片地址
    """
    #验证码图片路径
    codeSrc = soup.find('div',class_='a-row a-text-center').find('img').get('src')
    return codeSrc

def getSendUrl(soup,code):
    """
    拼接发送验证码url
    """
    amzn = soup.find('input', attrs={'name':'amzn'})['value']
    amznR = soup.find('input', attrs={'name':'amzn-r'})['value']
    requestVerifyUrl = validateUrl+'?amzn='+amzn+'&amzn-r='+amznR+'&field-keywords='+code 
    return requestVerifyUrl

def askUrl(url):
    """
    发送http请求
    """
    try:
        res = requests.get(url,headers=header,verify=False,timeout=10)  
        # res = requests.get(url,headers=header,timeout=20)
        return res
    except requests.exceptions.RequestException as e:
        print(e)
    