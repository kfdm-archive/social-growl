import sys
import os
from ConfigParser import ConfigParser,NoOptionError,NoSectionError

class Config:
	_defaults = {
		'gntp':{
			'host':'localhost',
			'port':23053,
			'password':'',
		},
		'social':{
			'email':'###',
			'password':'',
			'domain':'###',
			'appname':'Socialcast',
			'polldelay':600,
			'debug':False,
		},
	}
	_booleans = ['social.debug']
	_ints = ['gntp.port','social.polldelay']
	def __init__(self,file):
		self._file = os.path.expanduser(file)
		self._config = ConfigParser()
		try: self._config.readfp(open(self._file))
		except IOError:
			print >> sys.stderr, 'No config file found.  Writing defaults to',file
			for section,options in self._defaults.iteritems():
				self._config.add_section(section)
				for option,default in options.iteritems():
					self._config.set(section,option,default)
			self._config.write(open(self._file,'w'))
			# If the EDITOR var is set, we'll open their editor 
			# to edit the configuration file
			if os.environ['EDITOR']:
				os.system('%s %s'%(os.environ['EDITOR'],self._file))
			sys.exit(1)
	def __getitem__(self,key):
		section,option = key.split('.',1)
		try:
			if key in self._booleans:
				return self._config.getboolean(section, option)
			if key in self._ints:
				return self._config.getint(section, option)
			return self._config.get(section,option)
		except NoSectionError:
			self._config.add_section(section)
			self._config.set(section,option,self._defaults[section][option])
			self._config.write(open(self._file,'w'))
		except NoOptionError:
			self._config.set(section,option,self._defaults[section][option])
			self._config.write(open(self._file,'w'))
