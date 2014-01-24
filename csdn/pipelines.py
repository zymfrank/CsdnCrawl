# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from DBHelper import OracleDB
from scrapy.contrib.exporter import CsvItemExporter
from scrapy import log
from scrapy.exceptions import DropItem


class CsdnPipeline(object):
    users={}
    def __init__(self):
        self.file=None
        self.exporter=None
    def set_file(self,filename):
        self.file=open(filename,'wb')
        self.exporter=CsvItemExporter(self.file)

    def process_item(self, item, spider):
        if spider.name=="csdn.user":
            if self.file is None:
                self.set_file("export_users.csv")
            else:
                self.exporter.export_item(item)
        if spider.name=="csdn.login":
            if item['username']:
                sql='update t_csdn_users set real_password=:password,real_email=:email where username=:username';
                username=item['username']
                password=item['password']
                email=item['email']
                param={'username':username,'password':password,'email':email}
                spider.oracle_db.execute_sql(sql,param,False)
                log.msg("username:"+username+"\tpassword:"+password,level=log.INFO)
        return item