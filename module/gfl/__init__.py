import re
import math
import sqlite3

commands = []
comstring = "./(gfl|소녀전선|소전)"

db = sqlite3.connect("data.db")

def gfl_expc(pmsg):
	if re.fullmatch(r"(?i):\./(gfl|소녀전선|소전) (exp|경험치|경) [0-9]+ [0-9]+", \
		pmsg[-1]) is not None:
		_, __, s, f = pmsg[-1].split()
		if int(s) <= 100 and 0 < int(f) <= 100:
			start = int(s)
			fin = int(f)
			result = 0
			if start > fin:
				start, fin = fin, start
			if start < fin:
				c = db.cursor()
				c.execute("SELECT sum(experience) FROM (SELECT * FROM gfl_expc WHERE lv" + \
				" BETWEEN ? AND ?)", (start, fin - 1))
				result = c.fetchone()[0];
				c.close()
			return [":필요 경험치는 %d이고, 작전보고서는 %d개가 필요해요." % \
			(result, math.ceil(result / 3000))]
	c = pmsg[-1].split()
	return [":'%s %s [시작레벨] [목표레벨]'처럼 입력해 주세요!"%(c[0][1:],c[1])]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(gfl|소녀전선|소전) (exp|경험치|경)( .*)?")], gfl_expc))

def gfl_produce(pmsg):
	if re.fullmatch(r"(?i):\./(gfl|소녀전선|소전) (produce|prod|제조) [0-9]{0,2}:[0-5][0-9]", \
		pmsg[-1]) is not None:
		_, __, t = pmsg[-1].split()
		m, s = t.split(":")
		minute, second = int(m), int(s)
		time = minute * 60 + second
		c = db.cursor()
		c.execute("SELECT * from gfl_produce where time = ?", (time,))
		dbrs = c.fetchall()
		if dbrs is not None and len(dbrs) != 0:
			result = []
			for dbr in dbrs:
				result.append(":★%d %s: %s"%(dbr[1],dbr[2],dbr[3]))
		else:
			result = [":해당하는 결과가 없어요!"]
		return result
	c = pmsg[-1].split()
	return [":'%s %s 시:분'처럼 입력해 주세요!"%(c[0][1:],c[1])]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(gfl|소녀전선|소전) (produce|prod|제조)( .*)?")], gfl_produce))

def gfl_help(pmsg):
	return [":소녀전선 관련 정보를 제공하는 명령이에요.", \
	":./(gfl|소녀전선|소전) (exp|경험치|경)|(produce|prod|제조)"]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(gfl|소녀전선|소전) ?")], gfl_help))