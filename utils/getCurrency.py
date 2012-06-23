#!/usr/bin/env python

import urllib2
import re
import sys
from pprint import pprint

def getCurrency(first_price, second_price):
	try:
		values=""
		page = urllib2.urlopen("http://www.iccfx.com/curtable.php?tocompare="+first_price + "&tosearch="+second_price)
		pattern = re.compile('[&nbsp;]+(\d+.\d+)[&nbsp;]+.*[&nbsp;]+(\d+.\d+)[&nbsp;]+')
		for line in page:
			if pattern.search(line):
				values = pattern.search(line).groups()
				if values == ('0000', '0000'):
					message ="Unknown symbol: " +second_price+"\n"
					message +="Please go to http://en.wikipedia.org/wiki/List_of_circulating_currencies for more info"
					return message
		if not values:
			message = "Unknown symbol: " +first_price+"\n"
			message +="Please go to http://en.wikipedia.org/wiki/List_of_circulating_currencies for more info"
			return message
		else:
			message = { 	second_price+" to "+first_price: values[0], 
					first_price+" to "+second_price: values[1] }
		return message
	except Exception, e:
		print "Error:\n%s" % e
		
if __name__ =="__main__":
	prices = getCurrency(sys.argv[1],sys.argv[2])
	pprint(prices)
