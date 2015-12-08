#-*-coding:utf-8-*-
#Author: Victor
#Date: 2015-6-25
import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import time
from random import random

from news.items import NewsItem
from news.city import get_province_city

class JieYangSpider(CrawlSpider):
    name = 'jieyang'

    allowed_domains = ['www.jynews.net']
    start_urls = ["http://www.jynews.net/Category_1/index.aspx"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www\.jynews\.net/Item/\d+\.aspx'),unique=True),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=('http://www\.jynews\.net/Category_\d+/index(_\d+)?\.aspx'), unique=True)),
        
        )


    def parse_item(self, response):
        
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//head/title/text()").extract()[0]
            time_raw = hxs.select("//font[@style='FONT-SIZE: 9pt; COLOR: #666666']/text()").extract()[0].split()
            item['date'] = time_raw[1][:4] + "-" + time_raw[1][5:7] + "-" + time_raw[1][8:-1]
            (province, city) = get_province_city(item['title'])
            item["province"] = province
            item["city"] = city
            item['content'] = ''
            content_list = hxs.select("//p/text()").extract()
            #if content_list ==[]:
             #   content_list = hxs.select("//div[@id='endtext']//FONT/text()").extract()
            if content_list:
                item['content'] = ''.join(content_list)
            else:
                print 'None'
            if item['content'] == '':
                item['content'] = "null"
            yield item
            time.sleep(random())

        except:
            pass
     

        
