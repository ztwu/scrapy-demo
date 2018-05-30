import scrapy

#Item 是保存爬取到的数据的容器；其使用方法和python字典类似。
# 虽然您也可以在Scrapy中直接使用dict，但是 Item 提供了额外保护机制来避免拼写错误导致的未定义字段错误
#定义类型为 scrapy.Field 的类属性来定义一个Item
class DoubanItem(scrapy.Item):
    # define the fields for your item here like:

    title=scrapy.Field()
    author=scrapy.Field()
    author_homepage=scrapy.Field()
    img_url=scrapy.Field()
    pass