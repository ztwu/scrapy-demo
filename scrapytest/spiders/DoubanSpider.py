import urllib

import scrapy
import os
from scrapy import Request, FormRequest

import json

from scrapytest.DoubanItem import DoubanItem

#Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。
#其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 item 的方法。
class DoubanSpider(scrapy.Spider):
    #用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字
    name = 'scrapy-demo'

    # 可选，定义爬取区域，超出区域的链接不爬
    allowed_domains = ['douban.com']

    ##包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。
    # 后续的URL则从初始的URL获取到的数据中提取
    start_urls = []

    def start_requests(self):
        yield Request("https://www.douban.com/login", callback=self.parse, meta={"cookiejar":1})

    # 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
    def parse(self, response):
        #xpath Selectors选择器简介,通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分。
        #extract后会把selector对象转换成list类型
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        if len(captcha)>0:
            print("此时有验证码")
            PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))  # 获取项目根目录
            localpath = os.path.join(PROJECT_ROOT,"img/captchar.jpg")
            print("验证码图片的存放路径："+localpath)
            urllib.request.urlretrieve(captcha[0],filename=localpath)
            print("请查看本地验证码图片并输入验证码")
            captcha_value=input()

            data = {
                "form_email": "***",
                "form_password": "***",
                "captcha-solution": str(captcha_value),
                "redir": "https://www.douban.com/group/haixiuzu/discussion?start=0"  # 登录后要返回的页面
            }
        else:
            print("此时没有验证码")
            data = {
                "form_email": "1182517419@qq.com",
                "form_password": "ztwu2#iflytek",
                # "redir": "https://www.douban.com/group/haixiuzu/discussion?start=0"  # 登录后要返回的页面
            }
        print("登陆中...")
        yield FormRequest.from_response(response,meta={"cookiejar": response.meta["cookiejar"]}, formdata=data, callback=self.parse_redirect)

    def parse_redirect(self, response):
        print("已登录豆瓣")
        title = response.xpath('//title//text()').extract()

        baseurl='https://www.douban.com/group/haixiuzu/discussion?start='
        for i in range(0, 625, 25):
            pageUrl=baseurl+str(i)
            yield Request(url=pageUrl, callback=self.parse_process,dont_filter = True)

    def parse_process(self, response):
        title = response.xpath('//title//text()').extract()
        items = response.xpath('//td//a/@href').extract()
        for item in items:
            if 'topic' in item:
                url=item
                yield Request(url=item,callback=self.parse_img)

    def parse_img(self,response):
        img = DoubanItem()
        title=response.xpath('//title//text()').extract()
        img['title']=title
        author=response.xpath('//div[@class="topic-doc"]//h3//a//text()').extract()
        img['author']=author
        author_homepage = response.xpath('//div[@class="topic-doc"]//h3//a/@href').extract()
        img['author_homepage'] = author_homepage
        img_url = response.xpath('//div[@class="image-wrapper"]//img/@src').extract()
        img['img_url'] = img_url
        yield img