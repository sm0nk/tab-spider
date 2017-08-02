#coding=utf-8
import requests
import threading
import Queue
from bs4 import BeautifulSoup as BS
import re,time,json

'''
step1 access all pages  find_all vulnerabilities
step2 exchange operate
	ex_success   ex_ed   KB_NOT  Noway_Ex
step3 download poc

'''

headers = {
'Host': 'www.seebug.org',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'X-CSRFToken': '6ZqJzdh2on58BNogVIqw6xmxrsF8lCw4',
'Referer': 'https://www.seebug.org/vuldb/vulnerabilities?page=2',
'Cookie': 'Hm_lvt_6b15558d6e6f640af728f65c4a5bf687=1484033705,1484897193,1484966432,1484966443; csrftoken=6ZqJzdh2on58BNogVIqw6xmxrsF8lCw4; __jsluid=c8cb8546722ae5917f85b49b64081ed4; Hm_lpvt_6b15558d6e6f640af728f65c4a5bf687=1484966696; sessionid=73e4b4a01bd16hg7vdstjrtkeah5fz33; messages="05f7b0cd72cdc37ef2f4f8f0a07c588a63571fbb$[[\"__json_message\"\0540\05425\054\"Login succeeded. Welcome\054 sm0nk.\"]]"',
'Connection': 'close',
'Upgrade-Insecure-Requests': '1',
}

class SeebugPOC(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self._queue = queue
	def run(self):
		while not self._queue.empty():
			url = self._queue.get_nowait()
			self.spider(url)

	def spider(self,url):
		r = requests.get(url=url,headers=headers)
		#print r.status_code
		soup = BS(r.content,'lxml')
		names = soup.find_all(name='a',attrs={'class','vul-title'})
		for name in names:
			#print name
			#print name['title'].encode('utf-8')
			ssvid = name['href'].split('-')[-1]
			exchange_url = 'https://www.seebug.org/vuldb/ssvid-'+str(ssvid)
			print exchange_url
			dic = {}
			dic['type'] = 'poc'
			dic['anonymous'] = 'true'
			datas = json.dumps(dic)
			#print postdata
			#postdata = {"type":"poc","anonymous":true}
			exchange_r = requests.post(url=exchange_url,data=datas,headers=headers)
			print exchange_r.status_code,len(exchange_r.content)#,exchange_r.content
			if len(exchange_r.content) in [52,69]:
				down_url = 'https://www.seebug.org/vuldb/downloadPoc/'+ssvid
				down_r =requests.get(url=down_url,headers=headers)
				f = open('poc/'+ssvid+'.py','w')
				f.write(down_r.content)
				f.close
			time.sleep(2)


def main():
	queue = Queue.Queue()
	for i in range(1,6):
		queue.put('https://www.seebug.org/vuldb/vulnerabilities?page='+str(i))
	threads = []
	thread_count = 2
	for i in range(thread_count):
		threads.append(SeebugPOC(queue))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':
	main()

