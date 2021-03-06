import logging
logger = logging.getLogger(__name__)

try:
	from gntp.config import GrowlNotifier as _Notifier
except ImportError:
	from Growl import GrowlNotifier as _Notifier


GROWL_NOTIFICATIONS = ['Message','Notice']

class GrowlNotifier(_Notifier):
	def __init__(self,appname,iconname=None):
		_icon = None
		if iconname:
			_icon = open(iconname).read()
		_Notifier.__init__(
			self,
			applicationName = appname,
			notifications = GROWL_NOTIFICATIONS,
			defaultNotifications = GROWL_NOTIFICATIONS,
			applicationIcon = _icon
		)
	def growl_notice(self,msg):
		msg_title = "[%s] %s"%(msg.user.username,msg.title)
		if msg.body:
			msg_body = msg.body
		else:
			msg_body = msg.external_url
		msg_body = "%s\n%s"%(msg.created_at,msg_body)
		logger.info(msg_title)
		self.notify(noteType='Message', title=msg_title,
			description=msg_body, callback=msg.permalink_url)
	def msg_summary(self,count):
		self.notify(
			noteType = 'Notice',
			title = "%s Messages Total"%count,
			description = '',
		)
