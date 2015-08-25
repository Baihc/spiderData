# -*- coding: utf-8 -*-
'''
Created on 2015年7月14日

@author: baihc
'''
import json
import psycopg2
import re
import datetime
import os
from twisted.enterprise import adbapi 
from twisted.internet import reactor

class json2db():
    def __init__(self):
        self.connect=psycopg2.connect(database='postgis', user='postgres', password='5211', host='localhost', port=5432)
        self.cursor=self.connect.cursor()
    
    def updateP_C(self,id,province,city):
        sql=u"""UPDATE "宝贝寻家" SET "liveProvince"='%s' ,"liveCity"='%s' WHERE "id"=%s;"""%(province,city,id)
        self.cursor.execute(sql)
        self.connect.commit()

    def updateMissingReason(self,id,missingReason):
        sql=u"""UPDATE "宝贝寻家" SET "missingReason"='%s' WHERE "id"=%s;"""%(missingReason,id)
        self.cursor.execute(sql)
        self.connect.commit()
        
    def insertRow(self,tableName,f,v):
        """f:为fieldName，v：为对应的value"""
        insertSQL='INSERT INTO "%(tableName)s" (%(fieldNames)s) VALUES (%(values)s)'%{"tableName":tableName,"fieldNames":f,"values":v}
#         print insertSQL
        self.cursor.execute(insertSQL)
        self.connect.commit()
        
    def creatTable(self):
        pass    
        
class SQLfilter():
    #正则
    def _filter(self,value,p):
        r=p.findall(value)
        if r:
            return r[0]
        
    #过滤文本型，保留数值型
    def filterFloat(self,value):
        p=re.compile('\d+\.*\d*')
        r=self._filter(value, p)
        if r:
            return float(r)
        else:
            return self._SQLstrFilter(r)
    #过滤SQL语句中的特殊字符
    def _SQLstrFilter(self,v):
        if type(v)==type(u''):
            reList=[("None","Null"),("\\","\\\\"),("'","''")]
            for i,j in reList:
                v.replace(i,j)
        elif v==None:
            v='Null'
        return v
    
    #将Dict拆成insert语句中的fields和values
    def SQLDictSplit(self,fieldDict):
        fieldName='"%s"'%('","'.join(fieldDict.keys()))
        fieldValue=""
        for v in fieldDict.values():
            fieldValue+='%s,'%v
        return fieldName, fieldValue[:-1]
    
def SQLstandard(fieldDict,floatField=('Price','Onsale','Lease'),dateField=('FinsishData','collectDate')):
#     floatField=('LandArea','PropertyRight','BldArea','GreeningRate','PropertyFee','HouseNum','ID','Postcode','PoltRate',"CurrentNum")
#     floatField=('housePrice','houseOnsale','houseLease')
    filterfield=SQLfilter()
    for fieldName in fieldDict:
        fieldvalue=fieldDict[fieldName]
        if fieldName in floatField:
            fieldDict[fieldName]=filterfield.filterFloat(fieldvalue)
        elif fieldName in dateField:
            fieldDict[fieldName]="DATE '%s'"%fieldvalue
        elif type(fieldvalue)==type(u'') or fieldvalue==None:
            fieldDict[fieldName]="'%s'"%filterfield._SQLstrFilter(fieldvalue)
    fieldDict['geom']= "ST_GeomFromText('POINT(%s %s)',4326)"%(fieldDict['Px'],fieldDict['Py'])
    fieldDict.pop('Px')
    fieldDict.pop('Py')
    return fieldDict

class dpPool():
    def __init__(self):
        self.dbpool=adbapi.ConnectionPool(dbapiName='psycopg2',host='localhost',
                database = 'postgis',
                user = 'postgres',
                password = '5211',
                port=5432,
                cp_reconnect = True,
                )
            
    def findById(self):
        query = u"""INSERT INTO "housePrice" (
                    "Onsale",
                    "city",
                    "Name",
                    "houseURL",
                    "collectDate",
                    "Price",
                    "area",
                    "subArea",
                    "geom",
                    "Address",
                    "Type",
                    "Id",
                    "Lease"
                )
                VALUES
                    (
                        '50',
                        '郑州1111',
                        '学府名邸1111',
                        'http://xuefumingdi0371.fang.com/xiangqing/',
                        DATE '2015-07-29',
                        '5454',
                        '中牟',
                        '中牟',
                        ST_GeomFromText (
                            'POINT(113.972598105 34.7100541298)',
                            4326
                        ),
                        '[中牟]商都大道与广惠街交叉口南400米,中牟..',
                        '住宅',
                        '2510715293',
                        '2'
                    )"""
        return self.dbpool.runOperation(query)

    def insertRow(self,tableName,f,v):
        """f:为fieldName，v：为对应的value"""
        insertSQL='INSERT INTO "%(tableName)s" (%(fieldNames)s) VALUES (%(values)s)'%{"tableName":tableName,"fieldNames":f,"values":v}
#         print insertSQL
        return self.dbpool.runOperation(insertSQL)




if __name__ == "__main__":


    dbapi=dpPool()
    dbapi.findById()
    
#     sqlfliter=SQLfilter()
#     print dir(d)
#     js2db=json2db()
#     resultFolder=ur'E:\workcode\spiderFang\result'
#     for jsonFile in os.listdir(resultFolder):
#         if jsonFile[-4:]=='json':
#             print jsonFile
#             houseURLs=[]
#             jsonFilePath=os.path.join(resultFolder,jsonFile)
#             f=open(jsonFilePath,'r')
#             for line in f.readlines():
#                 lineDict=json.loads( line[:-1])
#                 newDict=SQLstandard(lineDict)
#                 f,v=sqlfliter.SQLDictSplit(newDict)
#                 js2db.insertRow("housePrice" , f, v)
 


