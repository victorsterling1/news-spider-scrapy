#-*-coding:utf-8-*-
#Author: Victor
#Date: 2015-6-15
#It's just a test.
import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import time

from news.items import NewsItem

class TestSpider(CrawlSpider):
    name = 'test'

    allowed_domains = ['fx168.com']
    start_urls = ["http://news.fx168.com/top/index.shtml"]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'http://[a-zA-Z]+.fx168.com/.*/[0-9]+/[0-9]+.shtml')),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=(r'http://news.fx168.com/.*.shtml'))),
        
        )


    def parse_item(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//head/title/text()").extract()[0]
            time_raw = hxs.select("//div[@class='yjl_fx168_article_time']/b[@class='shijian']/text()").extract()[0]
            item['date'] = time_raw.split()[0]
            item['content'] = ''
            content_list = hxs.select("//div[@id='yjl_fx168_article_zhengwen']/div[@class='TRS_Editor']//p/text()").extract()
            if content_list ==[]:
                content_list = hxs.select("//div[@class='yjl_fx168_article_zhengwen']/div[@class='TRS_Editor']//p/text()").extract()
            if content_list:
                item['content'] = ''.join(content_list)
            else:
                print 'None'
            if item['content'] == '':
                item['content'] = "null"
            yield item
            time.sleep(1)

        except:
            pass
     

        
