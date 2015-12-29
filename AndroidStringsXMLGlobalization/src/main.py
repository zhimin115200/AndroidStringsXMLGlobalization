#coding=utf-8

'''
Created on 2015-12-28

@author: zhimin115200
'''
import os
import re
import json
import urllib
import urllib2
import traceback
import xml.dom.minidom

dir='E://abc'
split='147258'

def get_all_xml_files_from_dir(path):
    list = os.listdir(dir)
    files=[]
    for line in list:
        filepath = os.path.join(dir,line)
        files.append(filepath)
    return files

class dataMap:
    def __init__(self):  
        self.names = []    
        self.values = []
        self.a=0


def get_all_strings_form_xml(path):
    
    dom = xml.dom.minidom.parse(path)  
    root = dom.documentElement
    itemlist = root.getElementsByTagName('string')
    
    data=dataMap()
    for i in range(0, len(itemlist)):
        item=itemlist[i]
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        
        if item.firstChild:
#             match = zhPattern.search(item.firstChild.nodeValue)
            
#             if match:
            data.names.append(item.getAttribute("name"))
            data.values.append(item.firstChild.nodeValue)
    return data

def translate(word):

    proxy = urllib2.ProxyHandler({'http': r'http://username:password@proxyserver:port'})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    url = 'http://apis.baidu.com/apistore/tranlateservice/translate?query=%s&from=zh&to=en'%word
    req = urllib2.Request(url)
    req.add_header("apikey", "c7a52b0a188711dbfdc3ef0c4c23ae1c")
    
    resp = urllib2.urlopen(req)
    content = resp.read()
    result=""
    if(content):
        content = json.loads(content)
        if content['errNum']==0:
            result = content["retData"]["trans_result"][0]["dst"]
            print result
    return result

def set_all_strings_to_xml(path , data , result):
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('string')
    for i in range(0, len(itemlist)):
        item=itemlist[i]
        for j in range(0,len(data.names)):
            if item.getAttribute("name")==data.names[j]:
                item.firstChild.nodeValue=result[j]
    f =  open(path,'w')
    dom.writexml(f,encoding = 'utf-8')

if __name__ == '__main__':
   
    print '开始'
    files = get_all_xml_files_from_dir(dir)
    for file in files:
        
        try:
            
            data = get_all_strings_form_xml(file) 
            
            word=''
            for i in range(0,len(data.names)):
                word=word+split+data.values[i] 
            result = translate(word)
            result=result.split(split)
            del result[0]

            set_all_strings_to_xml(file ,data, result)
            
        except:
            print traceback.print_exc() 
          
        print "进度 ："+str(files.index(file)+1) +"/"+ str(len(files))
    print '结束'

        
    
    