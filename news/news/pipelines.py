# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from os import path
from scrapy import signals

class NewsPipeline(object):
    def __init__(self):
        self.file = codecs.open('raw_data.json', 'w',"utf-8")
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

#class NewsPipeline(object):
    #def __init__(self):
        #self.file = codecs.open('raw_data.doc', 'w','utf-8')
    #def process_item(self, item, spider):        
        #self.file.write(item['title']+"\n")
        #self.file.write(item['link']+"\n")
        #self.file.write(item['province']+"\n")
        #self.file.write(item['city']+"\n")
        #self.file.write(item['date']+"\n")
        #self.file.write(item['content']+"\n")
        #return item
        #file.close()
