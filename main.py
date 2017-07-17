#!/usr/bin/python3
import socket
import re
import importlib
import module

server = "irc.ozinger.org"
port = 6667
encoding = "utf-8"
delm = "\r\n"

nickname = "아리시아"
username = "alicia_bot"
realname = "./help 나 ./도움 | 언니 대신 일하러 나왔어요"
chanlist = ["#xgc"]

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(128)
	s.connect((server, port))
	sendmsg(s, "NICK " + nickname)
	sendmsg(s, "USER %s 0 * :%s" % (username, realname))
	recvr = snlrecvr(s, 4096)
	msgsl = re.compile(r"(?:^:)(.*?)(?:\s:)(.*)")
	while True:
		msg = next(recvr)

		sl = msgsl.match(msg)
		if sl is not None:
			pmsg = sl.group(1).split() + [":" + sl.group(2)]
		else:
			pmsg = msg.split()
			if pmsg[0][0] == ":":
				pmsg[0] = pmsg[0][1:]

		fired = False
		for command in module.commands:
			if all(re.match(condition[1], pmsg[condition[0]]) for condition in command[0]):
				fired = True
				resps = command[1](pmsg)
				break

		if fired:
			fired = False
			for resp in resps:
				if resp[0] == ":":
					if pmsg[2] == nickname:
						target, _, __ = re.split(r"!|@", pmsg[0])
					else:
						target = pmsg[2]
					sendmsg(s, "PRIVMSG %s %s"%(target, resp))
				else:
					sendmsg(s, resp)
		elif pmsg[0] == "PING":
			sendmsg(s, "PONG " + pmsg[1])
		elif pmsg[1] == "001":
			for chan in chanlist:
				sendmsg(s, "JOIN " + chan)
		elif pmsg[1] == "PRIVMSG" and pmsg[-1] == ":./reload":
			module.mreload()
			importlib.reload(module)
			if pmsg[2] == nickname:
				target, _, __ = re.split(r"!|@", pmsg[0])
			else:
				target = pmsg[2]
			sendmsg(s, "PRIVMSG %s :로드 완료!"%(target))

def sendmsg(s, msg):
	s.sendall((msg + delm).encode(encoding))
	print("<< " + msg)

def snlrecvr(s, bufsize): #receive from socket s and yield it line by line.
	carry = ""
	while True:
		data = s.recv(bufsize).decode(encoding)
		lines = data.split(delm)
		lines[0] = carry + lines[0]
		for i, line in enumerate(lines):
			if i == len(lines) - 1:
				carry = line
			else:
				print(">> " + line)
				yield line

main()
