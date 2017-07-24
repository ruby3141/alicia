#!/usr/bin/python3
import socket
import re
import importlib
import configparser
import module

c = configparser.ConfigParser()
c.read("config.ini")

def main():
	s = connect()
	sendmsg(s, "NICK " + c['Bot']['nickname'])
	sendmsg(s, "USER %s 0 * :%s" % (c['Bot']['username'], c['Bot']['realname']))
	recvr = snlrecvr(s, int(c['Connection']['bufsize']))
	msgsl = re.compile(r"(?:^:)(.*?)(?:\s:)(.*)")
	while True:
		msg = next(recvr)

		sl = msgsl.fullmatch(msg)
		if sl is not None:
			pmsg = sl.group(1).split() + [":" + sl.group(2)]
		else:
			pmsg = msg.split()
			if pmsg[0][0] == ":":
				pmsg[0] = pmsg[0][1:]

		fired = False
		for command in module.commands:
			if all(re.fullmatch(condition[1], pmsg[condition[0]]) for condition in command[0]):
				fired = True
				resps = command[1](pmsg)
				break

		if fired:
			fired = False
			for resp in resps:
				if resp[0] == ":":
					if pmsg[2] == c['Bot']['nickname']:
						target, _, __ = re.split(r"!|@", pmsg[0])
					else:
						target = pmsg[2]
					sendmsg(s, "PRIVMSG %s %s"%(target, resp))
				else:
					sendmsg(s, resp)
		elif pmsg[0] == "PING":
			sendmsg(s, "PONG " + pmsg[1])
		elif pmsg[1] == "001":
			for chan in re.split(r", *", c['Server']['channel']):
				sendmsg(s, "JOIN " + chan)
		elif pmsg[1] == "PRIVMSG" and pmsg[-1] == ":./reload":
			module.mreload()
			importlib.reload(module)
			if pmsg[2] == nickname:
				target, _, __ = re.split(r"!|@", pmsg[0])
			else:
				target = pmsg[2]
			sendmsg(s, "PRIVMSG %s :로드 완료!"%(target))

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
	s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)
	s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
	s.settimeout(int(c['Connection']['timeout']))
	s.connect((c['Server']['host'], int(c['Server']['port'])))
	return s

def sendmsg(s, msg):
	s.sendall((msg + '\r\n').encode(c['Server']['encoding']))
	print("<< " + msg)

def snlrecvr(s, bufsize): #receive from socket s and yield it line by line.
	carry = ""
	while True:
		data = s.recv(bufsize).decode(c['Server']['encoding'])
		lines = data.split('\r\n')
		lines[0] = carry + lines[0]
		for i, line in enumerate(lines[:-1]):
			print(">> " + line)
			yield line
		carry = lines[-1]

main()
