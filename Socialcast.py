import sys
import urllib2
try: import simplejson as json
except ImportError: sys.exit('ERROR LOADING JSON')

API_REALM		= 'Socialcast Email address/Password'
API_URL			= 'https://%s.socialcast.com/'
API_MESSAGES	= API_URL+'api/messages.json'

class Socialcast(object):	
	def __init__(self,domain,email,password):
		self.domain		= domain
		self.email		= email
		self.password	= password
		
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(API_REALM,API_URL%self.domain,self.email,self.password)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
	
	def messages(self):
		try: data = urllib2.urlopen(API_MESSAGES%self.domain).read()
		except IOError, e:
			print e.headers
			sys.exit(1)
		messages = []
		for msg in json.loads(data)['messages']:
			messages.append(Message(msg))
		return messages

class Message(object):
	def __init__(self,data):
		self._raw	= data
		self.user	= User(data['user'])
	def __getattr__(self,name):
		return self._raw.get(name,None)
	
class User(object):
	def __init__(self,data):
		self._raw = data
	def __getattr__(self,name):
		return self._raw.get(name,None)