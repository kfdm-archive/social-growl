import logging
logger = logging.getLogger(__name__)
import sys,urllib2,time
import dateutil.parser
try:
	import json
except ImportError:
	try:
		import simplejson as json
	except:
		sys.exit('ERROR LOADING JSON')

API_REALM		= 'Socialcast Email address/Password'
API_URL			= 'https://%s.socialcast.com/'
API_MESSAGES	= API_URL+'api/messages.json'

class Socialcast(object):	
	def __init__(self,domain,email,password):
		self.domain		= domain
		self.email		= email
		self.password	= password
		logger.debug('Domain:   %s', API_URL % self.domain)
		logger.debug('Email:    %s', self.email)
		logger.debug('Password: %s', self.password)
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(API_REALM,API_URL%self.domain,self.email,self.password)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
	
	def messages(self):
		try: data = urllib2.urlopen(API_MESSAGES%self.domain).read()
		except IOError, e:
			logger.exception('Error reading messages %s',e.headers)
			sys.exit(1)
		messages = []
		for msg in json.loads(data)['messages']:
			messages.append(Message(msg))
		return messages

class Message(object):
	def __init__(self,data):
		self._raw	= data
		self.user	= User(data['user'])
		self.created_at = dateutil.parser.parse(data.get('created_at'))
		self.permalink_url = data['permalink_url']
	def __getattr__(self,name):
		return self._raw.get(name,None)
	
class User(object):
	def __init__(self,data):
		self._raw = data
	def __getattr__(self,name):
		return self._raw.get(name,None)
