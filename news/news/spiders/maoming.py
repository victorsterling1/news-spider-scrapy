#-*-coding:utf-8-*-
#Author: Victor
#Date: 2015-6-24
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

class MaoMingSpider(CrawlSpider):
    name = 'maoming'

    allowed_domains = ['www.mm111.net']
    start_urls = ["http://www.mm111.net/news/"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www\.mm111\.net/show/[0-9]+\.html'),unique=True),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=('http://www\.mm111\.net/news/.*'), unique=True)),
        
        )


    def parse_item(self, response):
        
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//head/title/text()").extract()[0]
            time_raw = hxs.select("//div[@id='content_head']/h2/span/text()").extract()[0].split()
            item['date'] = time_raw[0]
            (province, city) = get_province_city(item['title'])
            item["province"] = province
            item["city"] = city
            item['content'] = ''
            content_list = hxs.select("//div[@id='endtext']//p/span/text()").extract()
            if content_list ==[]:
                content_list = hxs.select("//div[@id='endtext']//span/text()").extract()
            if content_list ==[]:
                content_list = hxs.select("//div[@id='endtext']//p/text()").extract()
            if content_list ==[]:
                content_list = hxs.select("//div[@id='endtext']//FONT/text()").extract()
                
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
     

        
