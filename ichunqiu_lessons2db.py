#coding=utf-8
import re,sys
import requests
import json
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://www.ichunqiu.com/courses/ajaxCourses'
#postdata = 'courseTag=&courseDiffcuty=&IsExp=&producerId=&orderField=&orderDirection=&pageIndex=1&tagType=2'

headers = {
		'Host': 'www.ichunqiu.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
		'Accept': '*/*',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'http://www.ichunqiu.com/courses/263',
		'Content-Length': '98',
		'Cookie': 'Hm_lvt_1a32f7c660491887db0960e9c314b022=1482718025,1482999217,1483669624,1484445947; Hm_lvt_9104989ce242a8e03049eaceca950328=1480755934,1482644451,1482999233; pgv_pvi=7311038464; __jsluid=28ffae20a28e3fd3947a36033c4286ac; gr_user_id=6ccdab7a-ffde-4fb5-9542-59b687d101f5; browse=a%3A6%3A%7Bi%3A55765%3Bs%3A19%3A%222016-12-27+09%3A43%3A10%22%3Bi%3A54473%3Bs%3A19%3A%222016-12-04+17%3A09%3A22%22%3Bi%3A53239%3Bs%3A19%3A%222016-12-04+17%3A09%3A58%22%3Bi%3A50755%3Bs%3A19%3A%222016-12-04+17%3A10%3A16%22%3Bi%3A50777%3Bs%3A19%3A%222016-12-04+17%3A10%3A37%22%3Bi%3A55799%3Bs%3A19%3A%222016-12-04+17%3A16%3A41%22%3B%7D; uid=McTxMpxhNpyipcihdumnQq5iNuTlkOQO0O0OO0O0O; chkphone=acWxNpxhQpDiAchhNuSnEqyiQuDIO0O0O; ci_session=85fd874b3df53fb85890e40042c3ad078cdd5b28; Hm_lpvt_1a32f7c660491887db0960e9c314b022=1484446078',
		'Connection': 'close'
		}

conn = MySQLdb.connect(host='127.0.0.1',port = 3306,user = 'root',passwd = 'root',db = 'ichunqiu',use_unicode = True,charset="utf8")
cus  = conn.cursor()

def courses(postdata):
	r = requests.get(url=url,data=postdata,headers=headers)
	data = json.loads(r.text)
	counter =  len(data['course']['result'])
	for i in range(0,counter):
		CourseName = data['course']['result'][i]['courseName'].encode('utf-8')
		#CourseName = data['course']['result'][i]['courseName']
		Author = data['course']['result'][i]['producerName'].encode('utf-8')
		#Author = data['course']['result'][i]['producerName']
		BuyNum = data['course']['result'][i]['buyNum']
		print CourseName,Author,BuyNum
		sql = "insert into ICQ_Courses (CourseName,Author,Hits) values('%s','%s','%s')"%(CourseName,Author,BuyNum)
		cus.execute(sql)
		print sql ,'write success'

for i in range(1,12):
    postdata =  'courseTag=&courseDiffcuty=&IsExp=&producerId=&orderField=&orderDirection=&pageIndex='+str(i)+'&tagType=2'
    #print postdata
    courses(postdata)
    time.sleep(0.1)

cus = conn.commit()
#cus.close()
conn.close()
