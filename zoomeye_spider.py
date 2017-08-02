#coding=utf-8

import requests
import re
import json

def login():
	url_login = 'https://api.zoomeye.org/user/login'
	data = {
			"username":"test",
			"password":"test"
			}
	data = json.dumps(data)
	r = requests.post(url=url_login,data=data)
	#print r.content
	return json.loads(r.content)['access_token']

def main():
	url = 'https://api.zoomeye.org/host/search?query=tomcat'
	headers = {'Authorization':'JWT '+login()}
	r = requests.get(url=url,headers=headers)
	#print r.content
	datas = json.loads(r.content)['matches']
	for data in datas:
		print data['ip']
		#print type(data)

if __name__ == '__main__':
	main()
