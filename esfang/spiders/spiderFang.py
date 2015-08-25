# -*- coding: utf-8 -*-
'''
Created on 2015年6月30日

@author: Esri
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request 
from scrapy import log
from esfang.items import EsfangItem
 
import re
import sys 
from unbd import Offset
import datetime

class spiderFang(CrawlSpider):
    name="spiderFang"
    allowed_domains = ["fang.com"]
    
    start_urls = [
        "http://esf.fang.com/newsecond/esfcities.aspx"
    ]
    rules = [
        
        Rule(LinkExtractor(allow=(ur"fang.com"),restrict_xpaths=('//div[@id="c01"]//a[@class="red"]')),
             follow=True),
        Rule(LinkExtractor(allow=(ur"fang.com/housing/"),restrict_xpaths=('//div[@id="dsy_H01_04"]')),
             follow=True),
        Rule(LinkExtractor(allow=(ur"housing/[\d]+"),restrict_xpaths=('//div[@class="qxName"]/a')),
             follow=True),
        Rule(LinkExtractor(allow=(ur"housing/[\d]+_[\d]+"),restrict_xpaths=('//p[@id="shangQuancontain"]/a')),
             callback='parse_subarea',
             follow=True),
        Rule(LinkExtractor(allow=(ur"housing/[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+"),restrict_xpaths=('//a[@id="PageControl1_hlk_next"]')),
             callback='parse_subarea',
             follow=True),
    ]
    
    
    
   
    
    def parse_subarea(self, response):
        """解析区县和商圈名称"""
        areatexts=response.xpath('//div[@id="list_38"]//a[@class="org bold"]/text()')
        if areatexts:
            if len(areatexts)==2:
                areaName,subareaName=[aText for aText in areatexts.extract()]
            else:
                areaName=areatexts[0].extract()
                subareaName=areaName
        """解析houseList"""
        houseList=response.xpath('//div[@id="Div1" and @class="list rel"]')
        for house in houseList:
            item=EsfangItem()
            '''房屋信息列表'''
            item['city']=self._getHouseCity(house)
            item['Price']=self._getprice(house)
            item['houseURL']=self._getdetail(house)
            item['Name']=self._getHouseName(house)
            item['Type']=self._getHouseType(house)
            item["Address"]=self._getAddress(house)
            item["Onsale"]=self._getForsale(house)
            item["Lease"]=self._getLease(house)
            item["area"]=areaName
            item['subArea']=subareaName
            item['collectDate']=str(datetime.date.today())
            geomUrl, item["Id"]=self._getGeomURL(house)
            
            if geomUrl!='null':
                request = Request(geomUrl,
                             callback=self._getGeom)
                request.meta['item'] = item
                yield request
            else:
                item['Geom']='null'
                yield item
    
    '''解析房价'''
    def _getprice(self,house):
        price= house.xpath('string(.//span[@class="price"])').extract()
        if price:
            return price[0]
        else:
            return -1

    '''解析名称'''
    def _getHouseCity(self,house):
        cityname=house.xpath('string(//*[@id="dsy_H01_01"]/div[1]/a)').extract()
        if cityname:
            return cityname[0]
        else:
            return 'null'
       
    def _getHouseName(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        housenameList=div.xpath('string(./dl/dt/a)').extract()
        if housenameList:
            return housenameList[0]
        else:
            return "null"  
    
    def _getHouseType(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        housenameList=div.xpath('string(./dl/dt/span)').extract()
        if housenameList:
            return housenameList[0][1:-1]
        else:
            return "null"  
        
    def _getAddress(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        address=''.join(div.xpath('string(./dl/dd[1])').extract())
        
        return address.strip()
    
    def _getForsale(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        saleNum=''.join(div.xpath('string(./dl/dd[2]/a[1])').extract())
        return saleNum.replace(u"套",'').strip()
    
    def _getLease(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        leaseNum=''.join(div.xpath('string(./dl/dd[2]/a[2])').extract())
        return leaseNum.replace(u"套",'').strip()
    
#     def _getLeasePrice(self,house):
#         div=house.xpath('.//div[@class="info rel floatl ml15"]')
#         leaseURL=div.xpath('string(./dl/dd[2]/a[2]@href)').extract()
#         if leaseURL:
#             request = Request(leaseURL[0],
#                              callback=self._LeasePrice)
#             
#     def _LeasePrice(self,response):
#         roomPrice={}
#         dictKeys=response.xpath('.//span[@class="mr10"]')
#         for dictKey in dictKeys:
#             key=dictKey.xpath('./text()').extract()
#             val=dictKey.xpath('.//span[@class="orange"]/text()').extract()
#             if key and val:
#                 roomPrice[key[0]]=val[0]
                
        
               
               
               
    def _getdetail(self,house):
        try:
            div=house.xpath('.//div[@class="info rel floatl ml15"]')
            detailurl=''.join(div.xpath('.//dd[starts-with(@id,"detail_")]/a[1]/@href').extract())
            return detailurl
        except:
            s=sys.exc_info()
            errorinfo= "Detail error :Error '%s' happened on line %d" % ( s[1], s[2].tb_lineno )
            log.msg(errorinfo, level=log.WARNING)
            return 'null'
        
    def _getGeomURL(self,house):
        div=house.xpath('.//div[@class="info rel floatl ml15"]')
        urlList=div.xpath('.//dd[starts-with(@id,"detail_")]/a[3]/@href').extract()
        try:
            geomUrl=''.join(urlList)
            houseID=geomUrl.strip().split('=')[-1]
            
            return geomUrl.strip(),houseID
        except:
            s=sys.exc_info()
            errorinfo= "GeomID error: '%s' happened on line %d" % ( s[1], s[2].tb_lineno )
            log.msg(errorinfo, level=log.WARNING)
            return 'null','null'
        
    def _getGeom(self,response):
        try:
            em_string=response.body
            p = re.compile( 'px:.*"\d+\.\d+"' )
            px = p.findall( em_string)
            px = px[0].split( "\"" )[1]
            p = re.compile( 'py:.*"\d+\.\d+"' )
            py = p.findall( em_string )
            py = py[0].split( "\"" )[1]
            
            item = response.meta['item']
            """偏移"""
            offerBD=Offset()
            rawX, rawY = float(px),float(py)
            item['Px'], item['Py'] = offerBD.unBdCoor(rawX, rawY)
            yield item
        except:
            s=sys.exc_info()
            errorinfo= "Map URL Error:'%s' happened on line %d" % ( s[1], s[2].tb_lineno )
            log.msg(errorinfo, level=log.WARNING)
            log.msg("Map URL Error is %s"%response.url, level=log.WARNING)
            
            item = response.meta['item']
            item['Px']=0.
            item['Py']=0.
            yield item
            
            
            
    
