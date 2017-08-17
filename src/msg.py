import logging

logger = logging.getLogger("alicia")

class Msg(object):
	def __init__(msg):
		logger.debug(">> %s"%(msg,))
		colon = False
		if msg[0] == ":":
			colon = True
			msg = msg[1:]
		arg = msg.split(" :", 1)
		self.args = arg[0].split()
		if colon:
			self.who = self.args[0]
			self.cmd = self.args[1]
			self.where = self.args[2]
			self.mbody = arg[1]
		else:
			self.cmd = self.args[0]
			self.mbody = arg[1]
		self.sub = mbody[:]

