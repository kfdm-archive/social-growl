import sys
from ConfigParser import ConfigParser

class Config:
	def __init__(self,file):
		self._file = file
		self._config = ConfigParser()
		try: self._config.readfp(open(file))
		except IOError:
			print >> sys.stderr, 'No config file found.  Writing defaults'
			self._config.set('DEFAULT','email','###')
			self._config.set('DEFAULT','password','###')
			self._config.set('DEFAULT','domain','###')
			self._config.set('DEFAULT','growlapp','Socialcast')
			self._config.set('DEFAULT','polldelay','600')
			self._config.write(open(file,'w'))
			sys.exit(1)
	def __getattr__(self,name):
		return self._config.get('DEFAULT',name)
	