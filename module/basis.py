import re

commands = []
comstring = "./ping ./핑 ./pong ./퐁"

def ping(pmsg):
	nick, username, addr = re.split(r"!|@", pmsg[0])
	return [":%s, 퐁!"%(nick,)]

commands.append(([(1, r"(?i)PRIVMSG"), (-1, r"(?i):\./(ping|핑)")], ping))

def pong(pmsg):
	nick, username, addr = re.split(r"!|@", pmsg[0])
	return [":%s, 핑?"%(nick,)]

commands.append(([(1, r"(?i)PRIVMSG"), (-1, r"(?i):\./(pong|퐁)")], pong))

def puck(pmsg):
	return [":(퍽)(퍼버벅)"]

commands.append(([(1, r"(?i)PRIVMSG"), (-1, r"(?i):\./(퍽|vjr|puck)")], puck))
