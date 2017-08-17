import re

class Router(object):
	def __init__():
		self.clist = []

	def add(self, condition, route, who = None, cmd = None, where = None, argcond = None):
		argcondition = []
		if who is not None:
			argcondition.append(("who", who))
		if cmd is not None:
			argcondition.append(("cmd", cmd))
		if where is not None:
			argcondition.append(("where", where))
		if argcond is not None:
			argcondition.append(cond) for cond in argcond
		self.clist.append((argcondition, condition, route))

	def privmsg(self, condition, route, who = None, where = None, argcond = None):
		self.add(condition, route, who=who, cmd="PRIVMSG", where=where, argcond=argcond)

	async def __call__(self, msg):
		for cmd in clist:
			fallthrough = False
			for cond in cmd[0]:
				try:
					if type(cond[0]) is str:
						target = getattr(msg, cond[0])
					else:
						target = msg.args[cond[0]]
					if re.fullmatch(cond[1], target, flags = re.I) is None:
						fallthrough = True
						break
				except:
					fallthrough = True
					break
			if fallthrough:
				continue
			if match(cond[1], msg.sub, flags = re.I) is not None:
				sub = msg.sub[:]
				msg.sub = re.sub(cond[1], "", msg.sub, flags = re.I)
				await cond[2](msg)
				msg.sub = sub[:]
