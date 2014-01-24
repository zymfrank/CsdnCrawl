#encoding=utf-8

__author__ = 'zym'
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from spiders.csdn_spider import LoginSpider
from scrapy.utils.project import get_project_settings

logfile='../login5.log'
spider=LoginSpider(id_from=240000,id_to=250000)
settings=get_project_settings()
crawler=Crawler(settings)
crawler.signals.connect(reactor.stop,signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start(logfile=logfile,crawler=crawler)
reactor.run()