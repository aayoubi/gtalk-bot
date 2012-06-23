#!/usr/bin/env python

from __future__ import division

import sys
import time
import re
import os

from pprint import pprint
from PyGtalkRobot import GtalkRobot

from utils.getVideo import *
from utils.getCurrency import *
from utils.getWeather import *

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

from xml.etree import ElementTree

############################################################################################################################

class SampleBot(GtalkRobot):
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == super_email:
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        #email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
        '''(email|mail|em|m)\s+(.*?@.+?)\s+(.*)(?i)'''
        email_addr = args[1]
        subject =  "sent from bot"
        body = args[2]
	
	jid = user.getStripped()
	if jid == super_email:
		gmail_user=email
		gmail_pwd=password
		self.replyMessage(user, "Sending email...")
		mail(gmail_user, gmail_pwd, email_addr, "A message from:  "+str(user), body)
		print user, "execute command: Send Email to ", email_addr

		self.replyMessage(user, "Email sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
		self.replyMessage(user, "Body: "+ body)
	else:
		self.replyMessage(user, "You are not allowed to send mails")

    def command_003_GetVideoInformation(self, user, message, args):
	#get youtube video information
	'''(youtube|video|vid)\s+((http://www|www)(.youtube.com.*))(?i)'''
	video=args[1]
	self.replyMessage(user, "Getting video info...")
	print user, "executed command: Get Video Info of", video
	self.usercommands.append([user.getStripped(), "get video info", video])

	title, date, desc, count, likes, dislikes = getVideoInfo(video)
	if title:
		self.replyMessage(user, "Title:")
		self.replyMessage(user, title)
	if date:
		self.replyMessage(user, "Added on:")
		self.replyMessage(user, date)
	if desc:
		self.replyMessage(user, "Description:")
		self.replyMessage(user, desc)
	if count:
		self.replyMessage(user, "Total Count:")
		self.replyMessage(user, count)
	if likes:
		self.replyMessage(user, "Total likes:")
		self.replyMessage(user, likes)
	if dislikes:
		self.replyMessage(user, "Total Dislikes:")
		self.replyMessage(user, dislikes)

    def command_004_Calculate(self, user, message, args):
	'''(^\d+(\.[0-9]+)?(e[0-9]+|E[0-9]+)?\s*(\+|\*|/|-)+\s*(\d+(\.[0-9]+)?(e[0-9]+|E[0-9]+)?)$)'''
	print user, "executed command: Calculator"
	self.usercommands.append([user.getStripped(), "calculator"])
	try:
		value = eval(message)
	except:
		self.replyMessage(user, "Error in arithmetic expression")
	else:
		self.replyMessage(user, value)
    
    def command_005_GetHistoryCommands(self, user, message, args):
	'''(^history$)'''
	jid = user.getStripped()
	if jid == super_email:
		for element in self.usercommands:
			self.replyMessage(user, element)
	else:
		self.replyMessage(user, "You are not allowed to execute this command")
    def command_006_GetCurrency(self, user, message, args):
	'''(^currency\s+([A-Z]{3})\s+([A-Z]{3})$)'''
	first_price = args[1]
	second_price=args[2]
	self.usercommands.append([user.getStripped(), "Currency "+first_price + " "+second_price])
	if first_price and second_price:
		prices= getCurrency(first_price, second_price)
		self.replyMessage(user, prices)
	else:
		self.replyMessage(user, "Error getting currency")
    
    def command_007_GetWeather(self, user, message, args):
	'''(^weather\s+(\w+)$)'''
	city=args[1]
	self.usercommands.append([user.getStripped(), "Weather "+city])
	if city:
		message = getWeather(city)
		self.replyMessage(user, message)
	else:
		self.replyMessage(user, "Error missing city name")
	

    def command_010_ShowHelp(self, user, message, args):
	#shows commands help
	'''(help|show help)'''
	print user, "executed command: Show Help"
	self.usercommands.append([user.getStripped(), "show help"])
	self.replyMessage(user, "\nCommands:")
	self.replyMessage(user, "(email) <email> <message>")
	self.replyMessage(user, "\n(available|busy|away) <personal_message>")
	self.replyMessage(user, "\n(youtube|video|vid) <youtube_link>")
	self.replyMessage(user, "\n(arithmetic expression) i.e: 10 * 3250")
	self.replyMessage(user, "\n(currency) <SYMBOL> <SYMBOL i.e: currency USD EUR")
	self.replyMessage(user, "\n(weather) <CITY>")
	self.replyMessage(user, "\nMore features to come...")

   
    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
	print user, "executed command: Unknown Command:", args
	self.usercommands.append([user.getStripped(), "unknown command ", message])
        self.replyMessage(user, "Wle unknown Command at:\n" + time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))

def mail(user, passwd, to, subject, text):
   msg = MIMEMultipart()

   msg['From'] = user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(user, passwd)
   mailServer.sendmail(user, to, msg.as_string())
   mailServer.close()

############################################################################################################################
if __name__ == "__main__":
    doc = ElementTree.parse('resources/auth.xml')
    try:
        email = doc.find('Username').text
        password = doc.find('Password').text
	super_email = doc.find('Superuser').text
    except:
        print "Error in XML file format: auth.xml."
    bot = SampleBot()
    bot.setState('available', "botting...")
    bot.start(email, password)
