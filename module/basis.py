def set(router):
	async def keepalive(msg):
		return ["PONG :%s"%(msg.mbody,)]
	router.add("", keepalive, cmd = "PING")

def reload():
	pass #does nothing
