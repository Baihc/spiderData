# -*- coding: utf-8 -*-
'''
Created on 2015年7月7日

@author: Esri
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from esfang.items import bbhjItem


import sys



class spiderBaobeihuijia(CrawlSpider):
    name="Baobeihuijia"
    allowed_domains = ["baobeihuijia.com"]
    
    start_urls = [
        "http://www.baobeihuijia.com/list.aspx?tid=2"
    ]
    rules = [
        
        Rule(LinkExtractor(allow=("/list.aspx\?tid=2&sex=&photo=&page="),restrict_xpaths=('//div[@class="pg"]')),
             follow=True),
        Rule(LinkExtractor(allow=("/view.aspx\?type=2&id="),restrict_xpaths=('//div[@id="ti1" and @class="pic_bot"]')),
             follow=True,
             callback='getInfo')
        
    ]
    
    def getInfo(self,response):
        try:
            item=bbhjItem()
            liList=response.xpath('//div[@id="table_1_normaldivr"]/ul/li')
            item['id']=self._getID(liList)
            item['name']=self._getName(liList)
            item['sex']=self._getSex(liList)
            item['brithDate']=self._getBrithDate(liList)
            item['missimgDate']=self._getMissingDate(liList)
            item['liveAddress'],item['liveProvince'],item['liveCity']=self._getLiveLocation(liList)
            item['missingLocal'],item['missingProvince'],item['missingCity']=self._getMissLocation(liList)
            item['missInfo']=self._getMissInfo(liList)+'.'+self._getMissDetail(liList)
            yield item
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % ( s[1], s[2].tb_lineno )
            print response.url
            yield item
    
    def _getText(self,liList,i):
        infoText=liList[i].xpath('./text()').extract()
        if infoText:
            return infoText[0]
        else:
            return 'null'
    
    def _getID(self,liList):
        return liList[1].xpath('string(./a)').extract()[0]
    
    def _getName(self,liList):
        return self._getText(liList, 2)
    
    def _getSex(self,liList):
        return self._getText(liList, 3)
    
    def _getBrithDate(self,liList):
        return self._getText(liList, 4)
    
    def _getMissingDate(self,liList):
        return self._getText(liList, 6)
        
    def _getLiveLocation(self,liList,i=7):
        address= liList[i].xpath('./text()').extract()
        if not address:
            return 'null','null','null'
        addList=address[0].split(u',')
        if len(addList)==0:
            return 'null','null','null'
        if len(addList)==1:
            return address,'null','null'
        if len(addList)==2:
            return address,addList[0],'null'
        else:
            return address,addList[0],addList[1]
    
    def _getMissLocation(self,liList):
        return self._getLiveLocation(liList, i=8)
        
    
    def _getMissInfo(self,liList):
        return self._getText(liList, 9)
    
    def _getMissDetail(self,liList):
        return self._getText(liList, 10)
 