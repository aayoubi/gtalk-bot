
import sys
import urllib2
import time
import textwrap
import re

def getURL(url):
	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
	except urllib2.URLError, e:
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code
		sys.exit(1)
	else:
		return response

def stripLine(line):
	insideBracket = False
	desc = ''
	for c in line:
		if c == '<':
			insideBracket = True
		if c == '>':
			insideBracket = False
			continue
		if insideBracket :
			continue
		desc += c
	return desc


def getVideoInfo(video):		
	url = video
	if url.startswith("http://"):
		url = url
	else:
		url = "http://"+url
	page = getURL(url)
	line = page.readline()
	title =''

	while line:
		if 'meta name="title"' in line:
			title = line[line.index('content=\"')+9:]
			title = title[:title.index('\"')]
		if 'id="eow-description"' in line:
			desc = stripLine(line)
		if 'id="eow-date"' in line:
			date = line[line.index('eow-date'):]
			date = date[date.index('>')+1:date.index('<')]
		if 'watch-view-count' in line:
			tmp = ''
			tmp += line
			line = page.readline()
			while ('span' not in line):
				tmp += line
				line = page.readline()
			count= repr(tmp)
			count =count[count.index('<strong>')+8:count.index('</strong>')]
		if 'class="likes"' in line:
			likes = line[line.index('class="likes">')+14:line.index('</span>')]
			dislikes= line[line.index('class="dislikes">')+17:]
			dislikes=dislikes[:dislikes.index('</span>')]
		line = page.readline()

	"""	
	if title:
		print "Title:"	
		print title
		print
	if date:
		print "Added on:"
		print date
		print
	if desc:
		print "Description:"
		print desc
	if count:
		print "Total Views count:"
		print count
	if likes:
		print "Total likes:"
		print likes
	if dislikes:
		print "Total dislikes:"
		print dislikes

	"""
	return (title, date, desc, count, likes, dislikes)

if __name__=='__main__':
	title, date, desc, count, likes, dislikes = getVideoInfo(sys.argv[1])
	print title
	print date
	print desc
	print count
	print likes
	print dislikes
