from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from io import BytesIO
import time
from ocr_code import recognize
from PIL import Image


options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("disable-blink-features=AutomationControlled")
options.add_argument(
    'User-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
url = 'https://www.amazon.com/errors/validateCaptcha'
browser = webdriver.Chrome('E:/chrom_dir/chromedriver.exe', options=options)

def getCookie():
    #browser.set_window_size(1920, 1080)
    browser.get(url)
    time.sleep(1)

    '''
    /处理验证码
    '''
    #要截图的元素
    try:
        element = browser.find_elements(By.CLASS_NAME,'a-row.a-text-center')[1]
        # 坐标
        x, y = element.location.values() 
        # 宽高
        h, w = element.size.values()
        #把截图以二进制形式的数据返回
        image_data = browser.get_screenshot_as_png()
        # 以新图片打开返回的数据
        screenshot = Image.open(BytesIO(image_data))
        # 对截图进行裁剪
        result = screenshot.crop((x, y, x + w, y + h))
        # 显示图片
        #result.show()
        # 保存验证码图片
        result.save('VerifyCode.png')
        # 调用recognize方法识别验证码
        code = recognize('VerifyCode.png') 
        # 输入验证码
        browser.find_element(By.ID,'captchacharacters').send_keys(code)
        # 点击确认
        browser.find_element(By.CLASS_NAME,'a-button-text').click()
        time.sleep(1)
        print('success')
    except:
        print('error')


if __name__ == '__main__':
    getCookie()
