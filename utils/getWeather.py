#!/usr/bin/env python


import sys
import urllib2
import re
from pprint import pprint

def getWeather(city):
	try:
		values=""
		page = urllib2.urlopen("http://www.google.com/ig/api?weather="+city)
	except:
		print "Error"
		sys.exit(1)
	page = page.read()
	restofdays=[]

	if 'problem_cause data' in page:
        	message = "Error location not found: "+city
        	return message
	
	p_city = page[page.index('city data="')+11:]
	p_city = p_city[:p_city.index('"')]
	
	p_date = page[page.index('forecast_date data="')+20:]
	p_date = p_date[:p_date.index('"')]
	
	p_temp = page[page.index('temp_c data="')+13:]
	p_temp = p_temp[:p_temp.index('"')]
	
	p_humidity= page[page.index('humidity data="')+15:]
	p_humidity = p_humidity[:p_humidity.index('"')]
	
	p_wind= page[page.index('wind_condition data="')+21:]
	p_wind = p_wind[:p_wind.index('"')]
	
	forecast = page[page.index('forecast_conditions'):]
	day=forecast[forecast.index('day_of_week data="')+18:]
	day=day[:day.index('"')]
	low = forecast[forecast.index('low data="')+10:]
	low=low[:low.index('"')]
	high= forecast[forecast.index('high data="')+11:]
	high=high[:high.index('"')]
	condition = forecast[forecast.index('condition data="')+16:]
	condition=condition[:condition.index('"')]
	tmp= [day, low, high, condition]
	restofdays.append(tmp)
	
	forecast2 = forecast[forecast.index('</forecast_conditions>')+1:]
	day=forecast2[forecast2.index('day_of_week data="')+18:]
	day=day[:day.index('"')]
	low = forecast2[forecast2.index('low data="')+10:]
	low=low[:low.index('"')]
	high= forecast2[forecast2.index('high data="')+11:]
	high=high[:high.index('"')]
	condition = forecast2[forecast2.index('condition data="')+16:]
	condition=condition[:condition.index('"')]
	tmp= [day, low, high, condition]
	restofdays.append(tmp)
	
	forecast3 = forecast2[forecast2.index('</forecast_conditions>')+1:]
	day=forecast3[forecast3.index('day_of_week data="')+18:]
	day=day[:day.index('"')]
	low = forecast3[forecast3.index('low data="')+10:]
	low=low[:low.index('"')]
	high= forecast3[forecast3.index('high data="')+11:]
	high=high[:high.index('"')]
	condition = forecast3[forecast3.index('condition data="')+16:]
	condition=condition[:condition.index('"')]
	tmp= [day, low, high, condition]
	restofdays.append(tmp)
	
	forecast4 = forecast3[forecast3.index('</forecast_conditions>')+1:]
	day=forecast4[forecast4.index('day_of_week data="')+18:]
	day=day[:day.index('"')]
	low = forecast4[forecast4.index('low data="')+10:]
	low=low[:low.index('"')]
	high= forecast4[forecast4.index('high data="')+11:]
	high=high[:high.index('"')]
	condition = forecast4[forecast4.index('condition data="')+16:]
	condition=condition[:condition.index('"')]
	tmp= [day, low, high, condition]
	restofdays.append(tmp)

	for sub in restofdays:
		sub[1] = (int(sub[1]) - 32) * 5/9
		sub[2] = (int(sub[2]) - 32) * 5/9
		
	message = p_city +"\n"+ p_date+"\n"+p_temp+" C"+"\n"+p_humidity+"\n"+p_wind+"\n"+"\n"
	message += "Day\tLow\tHigh\tCondition\t\n"
	for sub in restofdays:
		for e in sub:
			message += str(e)+"\t"
		message += "\n"
	return message
	
		
if __name__=="__main__":
	message =getWeather(sys.argv[1])
	print message

