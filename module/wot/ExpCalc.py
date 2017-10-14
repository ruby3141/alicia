# leftExp for future extension

class ExpCalc:
	def exp(start, end, leftExp = 0):
		# Covering Exception
		if start == end:
			return 0
		elif start > end:
			start, end = end, start

		acc = 0
		if leftExp != 0:
			acc = leftExp
			start += 1
		for exp in range(start,end):
			acc += getNext(exp)
		
		return acc

	def getNext(start):
		skill = start // 100 + 1
		per = (start % 100) / 100
		return round((2 ** skill) * 25 * (100 ** per))

	def testPrint(a, b, c=0):
		print(a, 'to', b, 'with expression [LeftExp]', c, '=', exp(a, b, c))
