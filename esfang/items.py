# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import DictItem, Field

def create_item_class(class_name, field_list):
    fields = {field_name: Field() for field_name in field_list}
    
    return type(class_name, (DictItem,), {'fields': fields})

class EsfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city=scrapy.Field()
    area=scrapy.Field()#大商圈
    subArea=scrapy.Field()#商圈
    collectDate=scrapy.Field()
    Id=scrapy.Field()
    houseURL=scrapy.Field()
    Name=scrapy.Field()
    Address=scrapy.Field()
    Type=scrapy.Field()
    Px=scrapy.Field()#小区位置
    Py=scrapy.Field()#小区位置
    Detail=scrapy.Field()#小区详情的URL地址
    Onsale=scrapy.Field()#小区出售房源
    Lease=scrapy.Field()#小区出租房源
    Price=scrapy.Field()#小区均价
    leaseOneRoom=scrapy.Field()
    leaseTwoRoom=scrapy.Field()
    leaseThreeRoom=scrapy.Field()
    leaseSigleRoom=scrapy.Field()
    Geom=scrapy.Field()
    
class EsfangItemAreaURL(scrapy.Item):
    areaURL=scrapy.Field()
    subAreaURL=scrapy.Field()

class bbhjItem(scrapy.Item):
    name=scrapy.Field()
    id=scrapy.Field()
    sex=scrapy.Field()
    brithDate=scrapy.Field()
    missimgDate=scrapy.Field()
    liveAddress=scrapy.Field()
    liveProvince=scrapy.Field()
    liveCity=scrapy.Field()
    liveDistrict=scrapy.Field()
    missingLocal=scrapy.Field()
    missingProvince=scrapy.Field()
    missingCity=scrapy.Field()
    missingDistrict=scrapy.Field()
    missInfo=scrapy.Field()
    
class EsfangDetailItem(scrapy.Item):
    Px=scrapy.Field()#小区位置
    Py=scrapy.Field()#小区位置
    Name=scrapy.Field()#小区名
    DetailURL=scrapy.Field()#小区详情的URL地址
    ID=scrapy.Field()#ID
    LandArea=scrapy.Field()#占地面积
    BldArea=scrapy.Field()#建筑面积
    Localtion=scrapy.Field()#环线位置
    PropertyType=scrapy.Field()#物业类别
    HouseNum=scrapy.Field()#总户数
    CurrentNum=scrapy.Field()#当期户数
    PoltRate=scrapy.Field()#容积率
    PropertyFee=scrapy.Field()#物业费
    ProjctFeature=scrapy.Field()#项目特色
    Postcode=scrapy.Field()#邮政编码
    PropertyRight=scrapy.Field()#产权
    FinsishData=scrapy.Field()#竣工日期
    BuildStructure=scrapy.Field()#建筑结构
    GreeningRate=scrapy.Field()#绿化率
    city=scrapy.Field()
    
    
    