# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import json2db  
from twisted.enterprise import adbapi
import datetime
import os


class EsfangPipeline(object):
    
    def __init__(self):
        self.js2db=json2db.dpPool()
        self.sqlfliter=json2db.SQLfilter()
        
#         self.file = codecs.open('fang_data.json', mode='wb', encoding='utf-8')
    
    def creatFolder(self,spidername):
        today=datetime.date.today()
        folderTime=''.join([str(i) for i in today.timetuple()[:2]])
        folderPath=ur'E:\workcode\spiderFang\result\%s'%(spidername+folderTime)
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
        return folderPath
    
    def process_item(self, item, spider):
        lineDict=dict(item)
        spidername=spider.name
        
        folder=self.creatFolder(spidername)
        
        #存json
        if 'city' in item:
            jsonfilename=item['city']
        else:
            jsonfilename=spidername
        fileJson = codecs.open(os.path.join(folder,jsonfilename+'.json'), mode='a', encoding='utf-8')
        line=json.dumps(lineDict, ensure_ascii=False)+'\n'
        fileJson.write(line)
        fileJson.close()
        #入库
        if spidername=='spiderFang':
            newDict=json2db.SQLstandard(lineDict)
            f,v=self.sqlfliter.SQLDictSplit(newDict)
      
            d=self.js2db.insertRow("housePrice" , f, v)
#         
        return True

class bbhjPipeline(object):
    
#     def __init__(self):
#         self.file = codecs.open('fang_data.json', mode='wb', encoding='utf-8')
    def process_item(self, item, spider):
        
        jsonfilename='soufun_bj_detail'
        
        fileJson = codecs.open('%s.json'%jsonfilename, mode='a', encoding='utf-8')
        line=json.dumps(dict(item), ensure_ascii=False)+'\n'
        fileJson.write(line)
        fileJson.close()
        return item