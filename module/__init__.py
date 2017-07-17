import importlib

__all__ = ["basis"]

packages = []
commands = []
comstrings = []
comstring = ""

for pname in __all__:
	packages.append(importlib.import_module("." + pname, "module"))

for package in packages:
	commands += package.commands
	comstrings.append(package.comstring)

comstring = " | ".join(comstrings)
commands.append(([(1, r"(?i)PRIVMSG"), (-1, r"(?i):./(help|도움)")], \
	lambda pmsg: [":명령어 목록 : " + comstring]))

def mreload():
	for package in packages:
		importlib.reload(package)
