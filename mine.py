from random import *
import os
import discord

a, flg, prs, w, h, mm, x, y, lost = [], [], [], 12, 8, 15, 0, 0, False

#is integer?
def is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

#clamp the values
def clamp(v, mi, ma):
	return max(mi, min(v, ma))

#checks how many bonbs are around a position
def checkNum(x, y):
	o = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			xx = x + j
			yy = y + i
			if(xx >= 0 and xx < h and yy >= 0 and yy < w and a[xx][yy] == ":bomb:"):
				o += 1
	return o


#initialize the board
def init(ww, hh):
	global a, flg, prs, w, h, mm, x, y, lost

	a, flg, prs, w, h, mm, x, y, lost = [], [], [], 12, 8, 15, 0, 0, False

	w = ww
	h = hh

	#generate board
	for i in range(h):
		b = []
		c = []
		d = []
		for i in range(w):
			b.append("[ ]")
			c.append(0)
			d.append(0)
		a.append(b)
		flg.append(c)
		prs.append(d)

	#add mines
	for i in range(mm):
		if(i >= (h * w)): continue
		yp = randint(1, h) - 1
		xp = randint(1, w) - 1
		
		cn = 0
		while 1:
			if(a[yp][xp] == ":bomb:"):
				yp = randint(1, h) - 1
				xp = randint(1, w) - 1
			else:
				break
			#prevent infinite loop
			if(cn > 1000): break
			cn += 1


		a[yp][xp] = ":bomb:"

	#add numberz
	n = [":blue_square:", ":one:", ":two:", ":three:" , ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
	for i in range(h):
		for j in range(w):
			if(a[i][j] == ":bomb:"): continue
			a[i][j] = n[checkNum(i, j)]

	#remove zeros
	for i in range(h):
		for j in range(w):
			if(a[i][j] == "[0]"):
				a[i][j] = "[ ]"

def clampPos():
	global x, y
	x = clamp(x, 0, w - 1)
	y = clamp(y, 0, h - 1)

#print the board
def printG():
	global x, y

	clampPos()

	oo = ""
	for i in range(h):
		o = ""
		for j in range(w):
			if(i == y and j == x):
				o += ":snake:"
				continue
			if(flg[i][j] == 1):
				o += ":triangular_flag_on_post:"
				continue
			if(prs[i][j] == 0):
				o += ":blue_square:"
				continue
			o += a[i][j]
		oo += o + "\n"
	return oo

def printGO():
	clampPos()

	oo = ""
	for i in range(h):
		o = ""
		for j in range(w):
			if(a[i][j] == ":bomb:"):
				o += ":boom:"
				continue
			o += a[i][j]
		oo += o + "\n"
	return oo


def addPos(xx, yy):
	global x, y
	x += xx
	y += yy

def addFlag():
	global flg, prs, x, y
	if(prs[y][x] == 0 and flg[y][x] == 0): flg[y][x] = 1
	elif(flg[y][x] == 1): flg[y][x] = 0


async def revealPos(msg):
	global lost, a, flg, x, y

	embed = discord.Embed(title = "You lost :(", type = "rich", description = printGO(), colour = discord.Colour.from_rgb(56, 245, 154))

	if(a[y][x] == ":bomb:"): await msg.edit(embed = embed); lost = True
	if(flg[y][x] == 0): prs[y][x] = 1

def error(e):
	return discord.Embed(title = "Error", type = "rich", description = e, colour = discord.Colour.from_rgb(245, 103, 56))

emojis = ["⬅️", "➡️", "⬆️", "⬇️", "🚩", "👇"]

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self, message):

		if message.author == client.user:
			return

		if message.content.startswith("!mine"):
			global mesg

			try:
				sz = message.content.split()

				if(len(sz) > 2 and is_int(sz[1]) and is_int(sz[2])):
					w = int(sz[1])
					h = int(sz[2])

					init(w, h)
				else:
					await message.channel.send(embed = error("Incorrect usage of command!"))

			except Exception as e:
				await message.channel.send(embed = error(str(e)))

			try:
				embed = discord.Embed(title = "MineSweeper", type = "rich", description = printG(), colour = discord.Colour.from_rgb(56, 245, 154))

				mesg = await message.channel.send(embed = embed)

				for em in emojis:
					await mesg.add_reaction(em)
			except Exception as e:
				await message.channel.send(embed = error(str(e)))

	async def on_reaction_add(self, reaction, user):
		global mesg

		async for usr in reaction.users():
			if usr == client.user: continue

			if reaction.message == mesg:
				if reaction.emoji == '➡️':
					addPos(1, 0)
				if reaction.emoji == '⬅️':
					addPos(-1, 0)
				if reaction.emoji == '⬆️':
					addPos(0, -1)
				if reaction.emoji == '⬇️':
					addPos(0, 1)
				if reaction.emoji == '🚩':
					addFlag()
				if reaction.emoji == '👇':
					await revealPos(mesg)

			if not lost:
				embed = discord.Embed(title = "MineSweeper", type = "rich", description = printG(), colour = discord.Colour.from_rgb(56, 245, 154))

				await mesg.edit(embed = embed)


client = MyClient()
client.run('<token goes here>')
