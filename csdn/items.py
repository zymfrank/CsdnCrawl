# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UserItem(Item):
    # define the fields for your item here like:
    # name = Field()
    userid=Field()
    username=Field()
    rank=Field()
    score=Field()
    regdate=Field()
    downloadcount=Field()
    uploadcount=Field()
    grade=Field()

class LoginItem(Item):
    username=Field()
    password=Field()
    email=Field()
