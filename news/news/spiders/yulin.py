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

class YuLinSpider(CrawlSpider):
    name = 'yulin'

    allowed_domains = ['www.gxylnews.com']
    start_urls = ["http://www.gxylnews.com/news/"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www\.gxylnews\.com/news/html/\d+/\d+\.htm'),unique=True),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=('http:/www\.gxylnews\.com/news/(\d+-\d+\.htm)?'), unique=True)),
        
        )


    def parse_item(self, response):
        
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//head/title/text()").extract()[0]
            time_raw = hxs.select("//div[@class='about']/span/text()").extract()[0].split()
            item['date'] = time_raw[0]
            (province, city) = get_province_city(item['title'])
            item["province"] = province
            item["city"] = city
            item['content'] = ''
            content_list = hxs.select("//dl[@id='content']/dd//p/text()").extract()
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
     

        
