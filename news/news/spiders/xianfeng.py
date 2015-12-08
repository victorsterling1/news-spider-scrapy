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

class XianFengSpider(CrawlSpider):
    name = 'xianfeng'

    allowed_domains = ['www.xfxw.com.cn']
    start_urls = ["http://www.xfxw.com.cn/news/xwpd/index.html"]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'http://www.xfxw.com.cn/news.*/[0-9]+.*/[0-9]+.html')),callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=(r'http://www.xfxw.com.cn/news/.*.html'))),
        
        )


    def parse_item(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            item = NewsItem()
            item['link'] = response.url
            item['title'] = hxs.select("//div[@class='contentbody']/div[@class='contentleft']/div[@class='NewsContent']/h3/text()").extract()[0]

            time_raw = item['link'].split('/')[-2]
            if len(time_raw) == 6:
                item['date'] = time_raw[:4] + '-' + time_raw[-2] + '-' + time_raw[-1]
            if len(time_raw) == 8:
                item['date'] = time_raw[:4] + '-' + time_raw[-4:-2] + '-' + time_raw[-2:]
            if len(time_raw) == 7:
                if time_raw[4] > 2:
                    item['date'] = time_raw[:4] + '-' + time_raw[-3] + '-' + time_raw[-2:]
                elif time_raw[5] == 0:
                    item['date'] = time_raw[:4] + '-' + time_raw[-4:-2] + '-' + time_raw[-1]
                else:
                    item['date'] = time_raw[:4] + '-' + time_raw[-3] + '-' + time_raw[-2:]
                    
            
            (province, city) = get_province_city(item['title'])
            item["province"] = province
            item["city"] = city
            item['content'] = ''
            content_list = hxs.select("//div[@id='content']/div[@class='nr']/p/text()").extract()
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
     

        
