import re
from .ExpCalc import ExpCalc

commands = []
comstring = "./(wot|월탱|탱크)"

def wot_expc(pmsg):
	if re.fullmatch(r"(?i):\./(wot|월탱|탱크) (exp|경험치|경) [0-9]{0,4} [0-9]{0,4}", \
		pmsg[-1]) is not None:
		_, __, s, f = pmsg[-1].split()
		if 0 < int(s) <= 1000 and 0 < int(f) <= 1000:
			result = ExpCalc.exp(int(s), int(f))

			return [":필요한 승무원 경험치는 %d입니다." % \
			(result)]
		else:
			return "승무원 숙련도 입력이 너무 큽니다!"
	c = pmsg[-1].split()
	return [":'%s %s [시작숙련도] [최종숙련도]'처럼 입력해 주세요!"%(c[0][1:],c[1])]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(wot|월탱|탱크) (exp|경험치|경)( .*)?")], wot_expc))

def wot_help(pmsg):
	return [":World of Tanks 관련 정보를 제공하는 명령이에요.", \
	":./(wot|월탱|탱크) (exp|경험치|경)"]

commands.append(([(1,r"PRIVMSG"), \
	(-1, r"(?i):\./(wot|월탱|탱크) ?")], wot_help))
