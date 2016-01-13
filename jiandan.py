from bs4 import BeautifulSoup
import urllib2
import os

"""
spider for images on jiandan.net
"""

def encrypted_id(id):
	byte1 = bytearray('3go8&$8*3*3h0k(2)2')
	byte2 = bytearray(id)
	byte1_len = len(byte1)
	for i in xrange(len(byte2)):
		byte2[i] = byte2[i]^byte1[i%byte1_len]
 	m = md5.new()
 	m.update(byte2)
	result = m.digest().encode('base64')[:-1]
	result = result.replace('/', '_')
	result = result.replace('+', '-')
	return result

class HtmlDownloader(object):
	
	def download(self, url):
		if url is None:
			return None
		try:
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
		except urllib2.URLError, e:
			print e.reason 
		else:
			if response.getcode() == 200:
				return response.read()
		return None


class HtmlParser(object):

	def find_img(self, page_url, soup):  # TODO: use map()
		img_url_list = []
		img_tag_list = soup.find(id="wrapper").find("ol", class_="commentlist").find_all('img')
		#print len(img_tag_list)
		for tag in img_tag_list:
			if tag.get('org_src') != None:
				img_url_list.append(tag.get('org_src'))
			else:
				img_url_list.append(tag.get('src'))
		#print len(img_url_list)
		return img_url_list

	def show_current_page(self, soup):
		tag = soup.find(class_="current-comment-page")
		print "current page: %s" % tag.get_text()

	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return None
		#print page_url, len(html_cont)
		#soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		soup = BeautifulSoup(html_cont, 'lxml')
		#return new_urls, new_data
		self.show_current_page(soup)
		img_url_list = self.find_img(page_url, soup)
		#print img_list
		return img_url_list


class SpiderMain(object):
	def __init__(self):
		self.downloader = HtmlDownloader()
		self.parser = HtmlParser()
		#self.outputer = HtmlOutputer()

	def download_img(self, img_url_list):  # TODO: use map()
		path = './image'
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except:
			print "Failed to create directory in %s" % path
			exit()
		for url in img_url_list:
			content = self.downloader.download(url)
			name = path + '/' + url.split('/')[-1]
			if content != None:
				fp = open(name, 'wb')
				fp.write(content)
				fp.close()
				print 'saved: %s' % name

	def craw(self, root_url):
		html_cont = self.downloader.download(root_url)
		#print len(html_cont)
		img_url_list = self.parser.parse(root_url, html_cont)
		#print img_url_list
		self.download_img(img_url_list)


if __name__ == "__main__":
	root_url = "http://jandan.net/ooxx"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)