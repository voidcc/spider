# -*- coding: utf-8 -*-
import urllib2
import json
import os
import md5

"""
download musics of certain playlist
"""

class NeteaseMusic():
	def __init__(self, playlist_id):
		self.playlist_id = playlist_id
		self.playlist = []

	def download_url(self, url):
		if url is None:
			return None
		try:
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(req, timeout=1)
		except urllib2.HTTPError, e:
			print e.code
		except urllib2.URLError, e:
			print e.reason 
		else:
			if response.getcode() == 200:
				return response.read()
		return None

	def show_info(self, content):
		if content is not None:
			print '[playlist name]: %s' % content.get('name')
			print '[playlist id  ]: %d' % content.get('id')
			print '[track count  ]: %d' % content.get('trackCount')
			for idx, track in enumerate(content['tracks']):
				print idx+1, track['name']

	def save_track(self, content):
		if content is None:
			return 
		fpath = './' + content['name']
		try:
			if not os.path.exists(fpath):
				os.mkdir(fpath)
		except:
			print "Failed to create directory in %s" % fpath
			exit()
		music_url_list = []
		for track in content['tracks']:
			name = '/'.join([fpath, track['name'] + '.mp3'])
			print name
			music_url = track['mp3Url']
			music_url_list.append((name, music_url))
			print music_url
			#print '[hMusic]: %s' % track.get('hMusic').get('dfsId')
			#print '[mMusic]: %s' % track.get('mMusic').get('dfsId')
			#print '[lMusic]: %s' % track.get('lMusic').get('dfsId')
		return music_url_list
			
	def download_music(self, music_url_list):
		for item in music_url_list:
			print 'downloading to %s' % item[0]
			with open(item[0], 'wb') as mp3:
				response = urllib2.urlopen(item[1], timeout=2)
				mp3.write(response.read())
				response.close()

	def get_playlist(self):
		#url = 'http://music.163.com/#/playlist?id=' + str(self.playlist_id)
		url = 'http://music.163.com/api/playlist/detail?id=' + str(self.playlist_id)
		#print '[url]: %s' % url
		response = self.download_url(url)
		if response is None:
			print 'content is None'
			return None
		content = json.loads(response)['result']
		#self.show_info(content)
		return content
		
	def download_playlist(self):
		content = self.get_playlist()
		self.show_info(content)
		music_url_list = self.save_track(content)
		self.download_music(music_url_list)


if __name__ == "__main__":
	spider = NeteaseMusic(130059070)
	spider.download_playlist()