# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib


class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item

#pipeline模块来执行保存数据的操作
class DoubanPipeline(object):

    #处理完成后要返回 item 供后面的 Pipeline 类继续操作
    def process_item(self, item, spider):
        author=item["author"][0]
        title=item["title"][0].replace('\n','').strip()
        author_homepage=item["author_homepage"][0]
        #路径
        PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))  # 获取项目根目录
        dir=os.path.join(PROJECT_ROOT,"img/")
        print("爬虫数据存储路径："+dir)
        if not os.path.exists(dir):
            os.mkdir(dir)
        author_dir=dir+title
        if not os.path.exists(author_dir):
            os.mkdir(author_dir)

        #用户信息txt
        info=open(author_dir+"/用户信息.txt", "w")
        info.write(author+'\n'+author_homepage)
        info.close()

        #保存图片
        count=1
        for url in item["img_url"]:
            path=author_dir+"/"+str(count)+".jpg"
            urllib.request.urlretrieve(url, filename=path)
            count += 1
        return item
