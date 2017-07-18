import re
import math
import sqlite3

commands = []
comstring = "./(gfl|소녀전선|소전)"

db = sqlite3.connect("data.db")

def gfl_expc(pmsg):
	_, __, s, f = pmsg[-1].split()
	if start.isdigit() and fin.isdigit() and 0 < start <= 100 and 0 < fin <= 100:
		start = int(s)
		fin = int(f)
		result = 0
		if start < fin:
			fin, start = start, fin
			c = db.cursor()
			c.execute("SELECT sum(experience) FROM (SELECT * FROM gfl_expc WHERE lv" + \
			" BETWEEN ? AND ?)", (start, fin - 1))
			result = c.fetchone()[0];
			return [":필요 경험치는 %d이며, 작전보고서는 %d개가 필요합니다!" % \
			(result, math.ceil(result / 3000))]
	return [":'%s %s [시작레벨] [목표레벨]'처럼 입력해 주세요!"]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(gfl|소녀전선|소전) (exp|경험치|경) [0-1]* [0-1]*")], gfl_expc))
