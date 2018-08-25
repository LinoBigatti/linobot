import json

users = []

curs = []

class balance:
	def __init__(self, bal : list, name, previus : bool):
		self.ID = len(users)
		if previus:
			self.cur = bal
		else:
			self.cur = [0] * len(curs)
		self.tag  = name
		users.insert(self.ID, self)
	
	def __str__(self):
		return str(self.ID) + " " + self.tag + " " + str(self.cur) + '\n'
	
	def changecur(self, id, n):
		self.cur[id] += n
	
	def checkcur(self, id, n):
		if self.cur[id] >= n:
			return 1
		else:
			return 0
	
	def update(self):
		if len(self.cur) < len(curs):
			self.cur = self.cur + [0] * (len(curs) - len(self.cur))

class currency:
	def __init__(self, name, price):
		self.ID = len(curs)
		self.gold = price
		self.tag = name
		curs.insert(self.ID, self)
	
	def __str__(self):
		return self.tag
	
	def convert(self, cur, n):
		return (cur.gold / self.gold) * n
	
def finduser(id):
	for balance in users:
		if balance.tag == id:
			return balance.ID + 1
	return 0

def findcurrency(id):
	for currency in curs:
		if currency.tag == id:
			return currency.ID

def as_bal(dictlist):
    newbal = balance(dictlist['cur'], dictlist['tag'], True)
    return newbal

def as_cur(dictlist):
    newcur = currency(dictlist['tag'], dictlist['gold'])
    return newcur

def saveall():
	open('db.json', 'w').close()
	ballist = []
	for balance in users:
		ballist.append(balance.__dict__)
	with open('db.json', 'w') as f:  
		json.dump(ballist, f)
	
	open('curs.json', 'w').close()
	curlist = []
	for currency in curs:
		curlist.append(currency.__dict__)
	with open('curs.json', 'w') as f:  
		json.dump(curlist, f)

def loadall():
	with open('db.json', 'r') as f:  
		users = json.loads(f.read(), object_hook = as_bal)
	with open('curs.json', 'r') as f:  
		curs = json.loads(f.read(), object_hook = as_cur)
	for balance in users:
		balance.update()

def sortlb(cur):
		lb = []
		x = findcurrency(cur)
		lb = sorted(users, key=lambda y: y.cur[x])
		return lb