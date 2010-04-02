#!/usr/bin/env python
CFG_FILE		= 'social.cfg'
API_REALM		= 'Socialcast Email address/Password'
API_URL			= 'https://%s.socialcast.com/'
API_MESSAGES	= API_URL+'api/messages.json'

import sys
import urllib2
from ConfigParser import ConfigParser
try: import simplejson as json
except ImportError: sys.exit('ERROR LOADING JSON')

config = ConfigParser()
try: config.readfp(open(CFG_FILE))
except IOError:
	print >> sys.stderr, 'No config file found.  Writing defaults'
	config.set('DEFAULT','email','###')
	config.set('DEFAULT','password','###')
	config.set('DEFAULT','domain','###')
	config.write(open(CFG_FILE,'w'))
	sys.exit(1)


email		= config.get('DEFAULT', 'email')
password	= config.get('DEFAULT', 'password')
domain		= config.get('DEFAULT', 'domain')

print API_URL%domain
print API_MESSAGES%domain

auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(API_REALM,API_URL%domain,email,password)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

try: data = urllib2.urlopen(API_MESSAGES%domain).read()
except IOError, e:
	print e.headers
	sys.exit(1)


print json.loads(data)

for msg in json.loads(data)['messages'] :
	print msg['id'],msg['title']
	print msg['body']
	print