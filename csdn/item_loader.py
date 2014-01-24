#encoding=utf-8
__author__ = 'zym'
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Compose
import re
def encode_text(item):
    item=item.encode('gbk')
    return item


class UserLoader(ItemLoader):
    default_output_processor = MapCompose(encode_text)
