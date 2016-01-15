#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

def download(url):
	if url is None:
		return None
	try:
		headers = {'User-Agent': 'Mozilla/5.0'}
		#headers = {}
		req = urllib2.Request(url, headers = headers)
		response = urllib2.urlopen(req, timeout = 5)
	except urllib2.HTTPError, e:
		print e.code
	except urllib2.URLError, e:
		print e.reason 
	else:
		if response.getcode() == 200:
			return response.read()
	return None

def parse_main(cont):
	soup = BeautifulSoup(cont, 'lxml')
	new_url = soup.find('article').find('a').get('href')
	return new_url

def parse_account(cont):
	soup = BeautifulSoup(cont, 'lxml')
	tag_span = soup.find_all("span", attrs={"style": "color: #339966;"})
	for content in tag_span:
		#title = content.get_text().encode('UTF-8')
		title = content.get_text()
		print(title)

def getVIP(webSite):
	url = "http://www.vipfenxiang.com/"+webSite+"/"
	#print url
	cont = download(url)
	new_url = parse_main(cont)
	#print new_url
	cont = download(new_url)
	parse_account(cont)


if __name__ == '__main__':
	print("==========优酷==========")
	getVIP("youku")
	print("==========爱奇艺==========")
	print("Note:请使用客户端登录，提示绑定点击跳过")
	getVIP("iqiyi")
