import random
import math

class Token:
	def __init__(self, val):
		self.val = val

	def compare(self, cval):
		if self.val == cval:
			return True
		else:
			return False

	def reset(self):
		self.val = ""

class Block:
	def __init__(self, index):
		self.index = index


def parse(code):
	def setNewInt(lst, vals):
		for i in vals:
			lst.append(Token(i))
		return lst

	def setNewStr(lst, vals):
		for i in vals:
			lst.append(Token(str(i)))
		return lst

	cd = list(code)
	pos = 0

	Tokens = []
	Tks = []

	cd.append('EOF')
	Names = ""

	Stack = []
	Cstack = []

	Fbuff = []
	Blocks = {}
	Fpos = 0

	Vars = {}

	# Numbers detecting
	Tokens = setNewStr(Tokens, list(range(0, 10))) # Index: (0 to 9)

	# Math operations detecting
	Tokens = setNewStr(Tokens, ['+', '-', '*', '/', '%', '<', '>']) # Index: (10 to 16)

	# Literal detecting
	Tokens = setNewStr(Tokens, ['"', '\'']) # Index: (17 to 18)

	# Loops and functions detecting
	Tokens = setNewStr(Tokens, ['[', ']', '{', '}']) # Index: (19 to 22)

	# I/O
	Tokens = setNewStr(Tokens, ['.', ',', '~']) # Index: (23 to 25)
	
	# Stack manipulating
	Tokens = setNewStr(Tokens, ['$', '#', '^', '@']) # Index: (26 to 29)
	Tokens = setNewStr(Tokens, ['!', '?', ';', '`']) # Index: (30 to 33)
	Tokens = setNewStr(Tokens, ['n', 'b', 'i', 's', 'a'])

	for i in range(len(Tokens)):
		Tks.append(Tokens[i].val)
	Ext = [
	['π', 'φ', 'ρ', 'Σ', 'ω', ';', '=', ':'],
	['¬', 'σ', '°', '&'],
	['C', '(', ')', '|']]

	Lts = ['d', 'j', 'k', 't']

	while cd[pos] != 'EOF':
		if cd[pos] in Tks[0:10]:
			while cd[pos] in Tks[0:10]:
				Names += cd[pos]
				pos += 1
			pos -= 1
			Stack.append(int(Names))
			Names = ""
		elif cd[pos] == '«':
			while cd[pos] != '»':
				pos += 1

		elif cd[pos] == Tks[10]:
			Stack[-2] = Stack[-2] + Stack[-1]
			Stack.pop()

		elif cd[pos] == Tks[11]:
			Stack[-2] = Stack[-2] - Stack[-1]
			Stack.pop()

		elif cd[pos] == Tks[12]:
			Stack[-2] = Stack[-2] * Stack[-1]
			Stack.pop()

		elif cd[pos] == Tks[13]:
			Stack[-2] = Stack[-2] / Stack[-1]
			Stack.pop()

		elif cd[pos] == Tks[14]:
			Stack[-2] = Stack[-2] % Stack[-1]
			Stack.pop()

		elif cd[pos] == Tks[15]:
			Stack.append(int(Stack[-2] < Stack[-1]))

		elif cd[pos] == Tks[16]:
			Stack.append(int(Stack[-2] > Stack[-1]))

		elif cd[pos] == Tks[17]:
			pos += 1
			while cd[pos] != Tks[17]:
				Names += cd[pos]
				pos += 1
			Stack.append(Names)
			Names = ""

		elif cd[pos] == Tks[18]:
			pos += 1
			Stack.append(ord(cd[pos]))

		elif cd[pos] == Tks[19]:
			if Stack[-1] == 0:
				Stack.pop()
				while cd[pos] != ']':
					pos += 1

		elif cd[pos] == Tks[20]:
			if Stack[-1] != 0:
				Stack.pop()
				while cd[pos] != '[':
					pos -= 1

		elif cd[pos] == Tks[21]:
			Fbuff.append(pos)
			while cd[pos] != '}':
				pos += 1

		elif cd[pos] == Tks[23]:
			print(Stack[-1], end = "")
			Stack.pop()

		elif cd[pos] == Tks[24]:
			print(chr(Stack[-1]), end = "")
			Stack.pop()

		elif cd[pos] == Tks[25]:
			Stack.append(int(input()))

		elif cd[pos] == Tks[26]:
			Stack.append(Stack[-1])
		elif cd[pos] == Tks[27]:
			Stack.pop()
		elif cd[pos] == Tks[28]:
			Stack[-2], Stack[-1] = Stack[-1], Stack[-2]
		elif cd[pos] == Tks[29]:
			Stack.reverse()

		elif cd[pos] == Tks[30]:
			Fpos = pos
			pos = Fbuff[Stack[-1]]
			Stack.pop()

		elif cd[pos] == Tks[22]:
			pos = Fpos

		elif cd[pos] == Tks[33]:
			while cd[pos] != '\n':
				pos += 1

		elif cd[pos] == Tks[34]:
			Stack[-1] = int(not Stack[-1])
		elif cd[pos] == Tks[35]:
			Stack[-1] = bool(Stack[-1])
		elif cd[pos] == Tks[36]:
			Stack[-1] = int(Stack[-1])
		elif cd[pos] == Tks[37]:
			Stack[-1] = str(Stack[-1])

		elif cd[pos] == Tks[31]:
			if Stack[-2] != 0:
				Fpos = pos
				pos = Fbuff[Stack[-1]]
				Stack.pop()

		elif cd[pos] == Tks[38]:
			lArr = Stack[-1]
			oArr = []
			Stack.pop()
			for i in range(lArr):
				oArr.append(Stack[-1])
				Stack.pop()
			oArr.reverse()
			Stack.append(oArr)


		elif cd[pos] == Ext[0][0]:
			Stack.append(math.pi)
		elif cd[pos] == Ext[0][1]:
			Stack.append((1 + math.sqrt(5))/2)
		elif cd[pos] == Ext[0][2]:
			Stack[-2] = round(Stack[-2], Stack[-1])
			Stack.pop()
		elif cd[pos] == Ext[0][3]:
			Stack[-1] = sum(Stack[-1])
		elif cd[pos] == Ext[0][4]:
			break
		elif cd[pos] == Ext[0][5]:
			Stack.reverse()
			for i in enumerate(Stack):
				print(Stack[i[0]], end = " ")
			quit()
		elif cd[pos] == Ext[0][6]:
			if type(Stack[-2]) == int:
				exec(f"Vars['{Stack[-1]}'] = {Stack[-2]}")
			elif type(Stack[-2]) == str:
				exec(f"Vars['{Stack[-1]}'] = '{Stack[-2]}'")
			Stack.pop()
			Stack.pop()
		elif cd[pos] == Ext[0][7]:
			exec(f"Stack.append(Vars['{Stack[-1]}'])")
			Stack.pop(-2)

		elif cd[pos] == Ext[1][0]:
			if Stack[-2] == 0:
				Fpos = pos
				pos = Fbuff[Stack[-1]]
				Stack.pop()

		elif cd[pos] == Ext[1][1]:
			Stack[-1] = math.trunc(Stack[-1])

		elif cd[pos] == Ext[1][2]:
			Stack.append(input())

		elif cd[pos] == Ext[1][3]:
			Stack.append(int(Stack[-2] == Stack[-1]))

		elif cd[pos] == Ext[2][0]:
			Stack = []

		elif cd[pos] == Ext[2][1]:
			Cstack.append(Stack[-1])
			Stack.pop()

		elif cd[pos] == Ext[2][2]:
			Stack.append(Cstack[-1])
			Cstack.pop()

		elif cd[pos] == Ext[2][3]:
			Stack.append(ord(input()))

		elif cd[pos] == 'S':
			print(Stack, Cstack)

		elif cd[pos] == Lts[0]:
			Name = Stack[-1]
			block = Block(Fbuff[-1])
			Stack.pop()
			Blocks[Name] = block

		elif cd[pos] == Lts[1]:
			if Stack[-2] != 0:
				Fpos = pos
				pos = Blocks[Stack[-1]].index
				Stack.pop()

		elif cd[pos] == Lts[2]:
			Fpos = pos
			pos = Blocks[Stack[-1]].index
			Stack.pop()

		elif cd[pos] == Lts[3]:
			if Stack[-2] == 0:
				Fpos = pos
				pos = Blocks[Stack[-1]].index
				Stack.pop()
				


		pos += 1

	


parse("""
100"counter"=
{"Как дела у всех кста? ".}"print"d

1["print"j "counter":1-"counter"= "counter":]

""")