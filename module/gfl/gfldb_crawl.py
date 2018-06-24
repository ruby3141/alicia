#!/usr/bin/python3
import requests, bs4, sqlite3

db = sqlite3.connect("../../data.db")
r = requests.get("http://gfl.zzzzz.kr/timetable.php")
bs = bs4.BeautifulSoup(r.text, 'html.parser')

pt = bs.select("#timetable tr")
et = bs.select("#equiptimetable tr")

ptable = [[v.get_text() for v in p.find_all("td")] for p in pt[1:]]
etable = [[v.get_text() for v in e.find_all("td")] for e in et[1:]]

for p in ptable:
	p[0] = int(p[0][0:2])*60 + int(p[0][3:5])
	p[1], p[2] = int(p[2][0]), p[1]

for e in etable:
	e[0] = int(e[0][0:2])*60 + int(e[0][3:5])
	if(len(e[2]) > 0):
		e[1], e[2] = int(e[2][0]), e[1]
	else:
		e[1], e[2] = 0, e[1]

pdic = {}
edic = {}

for p in ptable:
	if (p[0], p[1], p[2]) not in pdic:
		pdic[(p[0], p[1], p[2])] = p[3]
	else:
		pdic[(p[0], p[1], p[2])] += (" · " + p[3])

for e in etable:
	if (e[0], e[1], e[2]) not in edic:
		edic[(e[0], e[1], e[2])] = e[3]
	else:
		edic[(e[0], e[1], e[2])] += (" · " + e[3])

c = db.cursor()

c.execute("DELETE FROM gfl_produce")
c.execute("DELETE FROM gfl_pequip")
c.executemany("INSERT INTO gfl_produce VALUES (?, ?, ?, ?)",
	[(p[0], p[1], p[2], p[3]) for p in [list(pk) + [pv] for pk, pv in pdic.items()]])
c.executemany("INSERT INTO gfl_pequip VALUES (?, ?, ?, ?)",
	[(e[0], e[1], e[2], e[3]) for e in [list(ek) + [ev] for ek, ev in edic.items()]])

c.close()

db.commit()
db.close()
