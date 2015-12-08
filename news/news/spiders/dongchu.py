#-*-coding:utf-8-*-
#Author: Victor
#Date: 2015-6-18
import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import time

from news.items import NewsItem
from news.city import get_province_city

class DongChuSpider(CrawlSpider):
    name = 'dongchu'

    allowed_domains = ['www.hsdcw.com']
    start_urls = ["http://www.hsdcw.com/"]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'http://www.hsdcw.com/html/[0-9]+.*/[0-9]+.htm')),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=(r'http://www.hsdcw.com/.*'))),
        
        )


    def parse_item(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//head/title/text()").extract()[0]
            time_raw = item['link'].split('/')
            item['date'] = time_raw[-2]
            (province, city) = get_province_city(item['title'])
            item["province"] = province
            item["city"] = city
            item['content'] = ''
            content_list = hxs.select("//div[@id='content']/p/text()").extract()
            #if content_list ==[]:
            #    content_list = hxs.select("//div[@class='yjl_fx168_article_zhengwen']/div[@class='TRS_Editor']//p/text()").extract()
            if content_list:
                item['content'] = ''.join(content_list)
            else:
                print 'None'
            if item['content'] == '':
                item['content'] = "null"
            yield item
            time.sleep(0.5)

        except:
            pass
     

        
