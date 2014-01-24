#encoding=utf-8

__author__ = 'zym'
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from spiders.csdn_spider import LoginSpider
from scrapy.utils.project import get_project_settings
import sys
d=['aaa','bbb','ccc']
print d[0:-1]