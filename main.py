#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'lipengyuan'

import re
import sys
import time
import chardet
import urllib
import urllib2
import cookielib
import cookielib
from HTMLParser import HTMLParser

names_url = "http://www.qimingzi.net/showNames.aspx"
base_url = "http://www.qimingzi.net/"

first_name = '李'
sex = '女'

params = urllib.urlencode({'surname': first_name, 'sex': sex})

headers = {"Cookie":"bdshare_firstime=1405234549757; ASP.NET_SessionId=aqa5ev55yjtoebexdssesjqo; searchType=poem; "
					"userSurname=%e6%9d%8e; userSex=2; AJSTAT_ok_pages=3; AJSTAT_ok_times=2"}

#TestData = urllib.urlopen(url).read()
#print chardet.detect(TestData)

class myHtmlParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.flag = None
		self.key  = None

	def handle_decl(self, decl):
		None
	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			self.flag = 'a'
			self.key = attrs[0][1] # get name detail url

	def handle_endtag(self,tag):
		None

	def handle_data(self, data):
		if len(data.strip()) > 0 and self.flag == 'a':
			getScore(data)

	def handle_comment(self,comment):
		None

def getHtml(url, params={}, headers={}):
	try:
		if params and headers:
			request = urllib2.Request(url, params, headers)
		else:
			request = urllib2.Request(url)

		response = urllib2.urlopen(request)
		return response.read().decode('gb2312', 'ignore')
	except urllib2.URLError:
		print 'Oops! Timeout Error! Sorry!'

def getCookie(url):
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	request = urllib2.Request(url)
	opener.open(request)
	ret = ''
	if cj:
		for ck in cj:
			print ck.name, ck.value
			ret = (ck.name + "=" + ck.value) + ";" + ret
		return ret
	else:
		return ''

def getScore(name):
	surname = urllib.quote(name[0:1].encode('gb2312'))
	lastname = urllib.quote(name[1:].encode('gb2312'))
	s = urllib.quote(sex.decode('utf8').encode('gb2312'))
	detail_url = "http://www.qimingzi.net/simpleReport.aspx?surname="+ surname + "&name=" + lastname + "&sex=" + s

	html = getHtml(detail_url)

	first_tag = '<div class="fenshu">'
	score = html[html.index(first_tag) + len(first_tag): html.index('</div><a name="zhuanye">')]
	print score
	if score and int(score) >= 90:
		result = ', '.join([name, score, detail_url])
		writeDown(result)

def writeDown(result):
	print result
	type = sys.getfilesystemencoding()

	f = open('name.txt', 'a')
	f.write(result.encode(type))
	f.write('\n')
	f.flush()
	f.close()

def Start():
	try:
		html = getHtml(names_url, params, headers)

		target_start = html.index('<div class="scon" >')
		target_end = html.index('<div style="padding-left:150px;">')
		target_content = html[target_start: target_end]
		print target_content

		m = myHtmlParser()
		m.feed(target_content)
		m.close()
	except:
		print 'Have a rest, then continue...'
		time.sleep(5)

	print('once more...')
	Start()

if __name__ == '__main__':
	Start()




