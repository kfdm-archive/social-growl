#!/usr/bin/env python
# Use the location of this file for the CWD
import os
os.chdir(os.path.dirname(__file__))

CFG_FILE = 'social.cfg'
GROWL_NOTIFICATIONS = ['Message','Notice']

from time import sleep
from Growl import GrowlNotifier
from Config import Config
from Socialcast import Socialcast

config	= Config(CFG_FILE)

#Register Growl
growl = GrowlNotifier(
	applicationName = config.growlapp,
	notifications = GROWL_NOTIFICATIONS,
	defaultNotifications = GROWL_NOTIFICATIONS,
	applicationIcon = open('icon.png').read()
)
growl.register()
def growl_notice(msg):
	msg_title = "[%s] %s"%(msg.user.username,msg.title)
	
	if msg.body: msg_body = msg.body
	else: msg_body = msg.external_url
	
	msg_body = str(msg.created_at) + '\n' + msg_body
	
	print msg_title
	growl.notify( noteType = 'Message', title = msg_title, description = msg_body )

sc		= Socialcast(config.domain,config.email,config.password)
msgs	= sc.messages()
growl.notify(
	noteType = 'Notice',
	title = "%s Messages Total"%(len(msgs)),
	description = '',
)
growl_notice(msgs[0])
last_message = msgs[0].created_at

while(True):
	try:
		print 'Sleeping for %s\t%s'%(config.polldelay,last_message)
		sleep(int(config.polldelay))
		newest_message = last_message
		for msg in sc.messages():
			if msg.created_at > last_message:
				growl_notice(msg)
				if msg.created_at > newest_message:
					newest_message = msg.created_at
		last_message = newest_message
				
	except KeyboardInterrupt:
		exit('Exiting')
