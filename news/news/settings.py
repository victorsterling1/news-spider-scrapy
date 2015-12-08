# -*- coding: utf-8 -*-

# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news'


SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'
ITEM_PIPELINES = [
    'news.pipelines.NewsPipeline']

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'    

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'
