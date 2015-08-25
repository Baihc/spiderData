# -*- coding: utf-8 -*-
'''
Created on 2015年7月7日

@author: Esri
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request 
from scrapy.contrib.loader import ItemLoader

from esfang.items import EsfangDetailItem
  

import json
import os
from twisted.python.text import strFile


fieldNameDict={u"占地面积":u"LandArea",
                    u"建筑面积":u"BldArea",
                    u"环线位置":u"Localtion",
                    u"物业类别":u"PropertyType",
                    u"总户数":u"HouseNum",
                    u"当期户数":u"CurrentNum",
                    u"容积率":u"PoltRate",
                    u"物业费":u"PropertyFee",
                    u"项目特色":u"ProjctFeature",
                    u"邮编":u"Postcode",
                    u"产权描述":u"PropertyRight",
                    u"竣工时间":u"FinsishData",
                    u"建筑结构":u"BuildStructure",
                    u"绿化率":u"GreeningRate"
                    }

class spiderFangDetail(scrapy.Spider):
    name="spiderFangDetail"
    allowed_domains = ["fang.com"]
    
    def start_requests(self):
        resultFolder=ur'E:\workcode\spiderFang\jg'
        for jsonFile in os.listdir(resultFolder):
            if jsonFile[-4:]=='json':
                houseType='houseType'
                houseId='houseId'
                jsonFilePath=os.path.join(resultFolder,jsonFile)
                f=open(jsonFilePath,'r')
                for line in f.readlines():
                    houseDict=json.loads(line[:-1])
                    if houseType not in houseDict:
                        houseType='Type'
                        houseId='Id'
                    if houseDict[houseType] in (u'住宅',u'别墅'):  
                        houseURL=houseDict['houseURL']
                        try:
                            request = Request(houseURL, callback=self.parse_houseURL,meta=houseDict)
                            request.meta['item'] = houseDict
                            yield request                  
                        except:
                            print houseURL,houseDict[houseId]
                        
    def parse_houseURL(self, response):
        houseDict=response.meta['item']
        detailItem=EsfangDetailItem()
        dds=response.xpath('//body[@id="dingbu"]/div[5]/div[1]/dl[3]/dd')
        if 'houseId' not in houseDict:
            detailItem['ID']=houseDict['Id']
            detailItem['Px']=houseDict['Px']
            detailItem['Py']=houseDict['Py']
        else:
            detailItem['ID']=houseDict['houseId']
            detailItem['Px']=houseDict['housePx']
            detailItem['Py']=houseDict['housePy']
        detailItem['DetailURL']=response.url
        detailItem['Name']=response.xpath('//*[@id="dingbu"]/div[2]/div[2]/h1/a/text()').extract()[0]
        
        detailItem['city']=houseDict['city']
        for dd in dds:
            fieldValue=dd.xpath('./text()')
            v='null'
            
            if fieldValue:
                v=self._getStandardtext(fieldValue[0])
            else:
                fieldValue=dd.xpath('./span/text()')
                if fieldValue:
                    v=self._getStandardtext(fieldValue[0])
                    
            
            fieldName=dd.xpath('./strong/text()')
            if fieldName:
                k=self._getStandardtext(fieldName[0])
                if k in fieldNameDict.keys():
                    fieldName=fieldNameDict[k]
                    detailItem[fieldName]=v
        yield detailItem
        
        
    def _getStandardtext(self,htmlText):
        strFilter=[(u'\xa0', u''),(u'：', u''),(u' ',u'')]
        strText=htmlText.extract()
        for i,j in strFilter:
            strText=strText.replace(i,j)
        return strText
    