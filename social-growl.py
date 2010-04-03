#!/usr/bin/env python
CFG_FILE = 'social.cfg'

from Config import Config
from Socialcast import Socialcast

config	= Config(CFG_FILE)
sc		= Socialcast(config.domain,config.email,config.password)
msgs	= sc.messages()
for msg in  msgs:
	print "#%s - %s [%s]"%(msg.id,msg.title,msg.user.username)
	if msg.body:
		print msg.body[0:80]
	if msg.external_url:
		print msg.external_url
	print

print '%d messages'%len(msgs)