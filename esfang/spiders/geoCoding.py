# -*- coding: utf-8 -*-
'''
Created on 2015年7月10日

@author: Esri
'''
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.http import FormRequest

import sys

class geoCoding(Spider):
    start_urls='http://192.168.120.60:8080/gt_lbs/rest/services/singleservice/single'
    
    def getCity(self,address):
        if address.find(u'亚洲')>0 and len(address)<=6:
            return None
        if address.find(u'不知')>0:
            return None
        
        data={'queryStr':address.encode('utf-8') ,'f':'json'}
        r={}
        if r['status']=='OK' and r["count"]>=1:
            return r["results"][0]["provincename"],r["results"][0]["cityname"]
        else:
            return None
        
    def parse(self, response):
        Spider.parse(self, response)