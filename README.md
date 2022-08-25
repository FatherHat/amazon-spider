**| Chinese |**

# 文件夹路径说明

config文件夹 | 配置文件夹

selenuim文件夹 | chrome操作内核包

yzm文件夹 | 验证码示例图片资源文件夹

# 主要文件说明 

index.py | 入口文件，做为主要逻辑处理文件

getCookies.py | http请求获取的cookies

parsingCode.py | 验证码识别



## 项目主要说明

[2022年08月23日] 

此脚本主要是爬亚马逊商品评论，以正则写法定位静态元素获取需要的文本，因亚马逊的反爬机制，目前发现有验证码机制，
需要处理验证码获取cookie发起http请求，据网上了解，亚马逊还具备IP限制问题，TCP请求无法进行拟造IP接收response。


## 启动说明 

配置正确的python环境，运行index.py文件即可


 