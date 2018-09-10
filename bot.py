import discord
from discord.ext import commands
from discord.utils import get
import random
from config import *
from economy import *

bot = commands.Bot(command_prefix=prefix, description=description)

userid = 294247258302578700

@bot.event
async def on_ready():
    	print('Logged in as')
    	print(bot.user.name)
    	print(bot.user.id)
    	print('------')

@bot.event
async def on_message(message):
	if message.content.startswith('>>'):
		global userid
		print("command evoked from " + str(message.author) + ", AKA " + message.author.display_name + ", ID: " + message.author.id + ", BOT : " + str(message.author.bot))
		print('------')
		print("content: " + message.content)
		print('------')
		await bot.process_commands(message)
	elif toogleall:
		print("message sended from " + str(message.author) + ", AKA " + message.author.display_name + ", ID: " + message.author.id + ", BOT : " + str(message.author.bot))
		print('------')
		print("content: " + message.content)
		print('------')

@bot.command(pass_context=True)
async def invite(ctx):
    """invite me!"""
    await bot.say(invite_link)

@bot.command(pass_context=True)
async def say(ctx, *, message):
    """say. autoexplaining."""
    await bot.say(message)

@bot.command(pass_context=True)
async def add(ctx, left : int, right : int):
	"""Adds two numbers together."""
	await bot.say(left + right)

@bot.command(pass_context=True)
async def sub(ctx, left : int, right : int):
	"""subs two numbers together."""
	await bot.say(left - right)

@bot.command(pass_context=True)
async def mul(ctx, left : int, right : int):
	"""mul two numbers together."""
	await bot.say(left * right)

@bot.command(pass_context=True)
async def div(ctx, left : int, right : int):
	"""divs two numbers together."""
	await bot.say(left / right)

@bot.command(pass_context=True)
async def off(ctx):
	"""Shutdown the bot."""
	await bot.say("powering off...")
	bot.logout()
	exit()

@bot.command(pass_context=True)
async def economystart(ctx):
	"""Starts your economy account."""
	if finduser(str(ctx.message.author)):
		await bot.say("you already have an account.")	
	else:
		x = balance([], str(ctx.message.author), None)
		users[x.ID].update()
		await bot.say("you succesfully created an user.")

@bot.command(pass_context=True)
async def addcur(ctx, cur : str, n : int):
	"""Creates a currency."""
	if ctx.message.author.id in owners:
		x = currency(cur, n)
		await bot.say("succesfully created currency " + str(curs[findcurrency(cur)]) + ".")
		for balance in users:
			balance.update()
	else:
		await bot.say("You need to be bot owner!")

@bot.command(pass_context=True)
async def delcur(ctx, cur : str):
	"""Deletes a currency."""
	if ctx.message.author.id in owners:
		x = findcurrency(cur)
		curs.pop(x)
		await bot.say("succesfully deleted currency " + cur + ".")
		for balance in users:
			balance.changecur(x, 0)
	else:
		await bot.say("You need to be bot owner!")

@bot.command(pass_context=True)
async def currencies(ctx):
	"""Shows currencies."""
	x = "```"
	for currency in curs:
		x += "Name: " + str(currency) + ". Value (In gold): " + str(currency.gold) + "\n"
	x += "```"
	await bot.say(x)

@bot.command(pass_context=True)
async def bal(ctx, cur : str):
	"""Shows your money."""
	if finduser(str(ctx.message.author)):
		print(str(users[finduser(str(ctx.message.author)) - 1].cur[findcurrency(cur)]))
		await bot.say(str(ctx.message.author) + ", you have " + str(users[finduser(str(ctx.message.author)) - 1].cur[findcurrency(cur)]) + " " + str(curs[findcurrency(cur)]) + ".")
	else:
		await bot.say("you dont have an account.")

@bot.command(pass_context=True)
async def pay(ctx, cur : str, n : int):
	"""Pays n coins to target. Needs to be bot owner."""
	if ctx.message.author.id in owners:
		if finduser(str(ctx.message.mentions[0])):
			print(len(curs))
			users[finduser(str(ctx.message.mentions[0])) - 1].changecur(findcurrency(cur), n)
			await bot.say("succesfully gived " + str(n) + " " + str(curs[findcurrency(cur)]) + " to " + str(ctx.message.mentions[0]) + ".")
		else:
			await bot.say("that user dont have an account.")
	else:
		await bot.say("You need to be admin!")

@bot.command(pass_context=True)
async def take(ctx, cur, n : int):
	"""Takes n coins from target. Needs to be bot owner."""
	if ctx.message.author.id in owners:
		if finduser(str(ctx.message.mentions[0])):
			users[finduser(str(ctx.message.mentions[0])) - 1].changecur(findcurrency(cur), -n)
			await bot.say("succesfully taked " + str(n) + " " + str(curs[findcurrency(cur)]) + " from " + str(ctx.message.mentions[0]) + ".")
		else:
			await bot.say("that user dont have an account.")
	else:
		await bot.say("You need to be admin!")

@bot.command(pass_context=True)
async def dice(ctx, n : int):
	"""Rolls a dice."""
	if finduser(str(ctx.message.author)):
		if users[finduser(str(ctx.message.author)) - 1].checkcur(1, n):
			users[finduser(str(ctx.message.author)) -1].changecur(1, -n)
			die1 = random.randint(1,6)
			die2 = random.randint(1,6)    
			r = die1 + die2  
			if r == 7:
				users[finduser(str(ctx.message.author)) - 1].changecur(1, n * 10)
				await bot.say("congratulations! you have 7. your bet: ```" + str(n) + "``` your profit: ```" + str(n * 10) + "```")
			elif r >= 6 and r <= 8:
				users[finduser(str(ctx.message.author)) - 1].changecur(1, n * 4)
				await bot.say("congratulations! you have " + str(r) + ". your bet: ```" + str(n) + "``` your profit: ```" + str(n * 4) + "```")
			elif r >= 5 and r <= 9:
				users[finduser(str(ctx.message.author)) - 1].changecur(1, n * 2)
				await bot.say("congratulations! you have " + str(r) + ". your bet: ```" + str(n) + "``` your profit: ```" + str(n * 2) + "```")
			else:
				await bot.say("sorry, you have " + str(r) + ". your bet: ```" + str(n) + "``` your profit: ```" + str(0) + "```")
		else:
			await bot.say("you dont have sufficient coins.")
	else:
		await bot.say("you dont have an account.")

@bot.command(pass_context=True)
async def multiplier(ctx, n : int):
	"""Gives you a multiplier."""
	if finduser(str(ctx.message.author)):
		if users[finduser(str(ctx.message.author)) - 1].checkcur(1, n):
			users[finduser(str(ctx.message.author)) - 1].changecur(1, -n)
			r = random.randint(-10,10)
			users[finduser(str(ctx.message.author)) - 1].changecur(1, n * r)
			await bot.say("you have " + str(r) + "x. your bet: ```" + str(n) + "``` your profit: ```" + str(n * r) + "```")
		else:
			await bot.say("you dont have sufficient coins.")
	else:
		await bot.say("you dont have an account.")

@bot.command(pass_context=True)
async def save(ctx):
	"""Saves the currency list."""
	if ctx.message.author.id in owners:
		saveall()
		await bot.say("succesfully saved state.")
	else:
		await bot.say("You need to be bot owner!")

@bot.command(pass_context=True)
async def load(ctx):
	"""Loads the currency list."""
	if ctx.message.author.id in owners:
		users[:] = []
		curs[:] = []
		loadall()
		await bot.say("succesfully loaded state.")
	else:
		await bot.say("You need to be bot owner!")

@bot.command(pass_context=True)
async def top(ctx, cur : str):
	"""shows the top."""
	lb = []
	lb = sortlb(cur)
	top = "leaderboard: \n"
	if len(lb) >= 10:
		i = 0
		while i != 10:
			top += "#" + str(i + 1) + ": " + str(lb[i].tag) + " - " + str(lb[i].cur[findcurrency(cur)]) + " " + str(curs[findcurrency(cur)]) + " \n"
			i += 1
	else:
		i = 0
		while i != len(lb):
			top += "#" + str(i + 1) + ": " + str(lb[i].tag) + " - " + str(lb[i].cur[findcurrency(cur)]) + " " + str(curs[findcurrency(cur)]) + " \n"
			i += 1
	await bot.say(top)

@bot.command(pass_context=True)
async def addowner(ctx):
	"""add an owner."""
	if ctx.message.author.id == host:
		owners.append(ctx.message.mentions[0].id)
		await bot.say("Enjoy your owner!")
	else:
		await bot.say("fuck you men, you arent the bot owner!")

@bot.command(pass_context=True)
async def delowner(ctx):
	"""removes an owner."""
	if ctx.message.author.id == host:
                try:
                        c = owners.index(ctx.message.mentions[0].id)
                        owners.pop(c)
                        await bot.say("Success")
                except IndexError:
                        await bot.say(str(ctx.message.mentions[0]) + " isnt an owner.")
	else:
		await bot.say("fuck you men, you arent the bot owner!")

@bot.command(pass_context=True)
async def setrole(ctx, role : str):
	"""sets a role to a user"""
	if ctx.message.author.server_permissions.manage_roles:
		x = get(ctx.message.server.roles, name = role)
		await bot.add_roles(ctx.message.mentions[0], x)
		await bot.say("succesfully gave role " + role + " to user " + str(ctx.message.mentions[0]))
	else:
		await bot.say("Error: you need Manage Roles permission!")

@bot.command(pass_context=True)
async def removerole(ctx, role : str):
	"""removes a role from a user"""
	if ctx.message.author.server_permissions.manage_roles:
		x = get(ctx.message.server.roles, name = role)
		await bot.remove_roles(ctx.message.mentions[0], x)
		await bot.say("succesfully deleted role " + role + " from user " + str(ctx.message.mentions[0]))
	else:
		await bot.say("Error: you need Manage Roles permission!")

@bot.command(pass_context=True)
async def clear(ctx, n : int):
	"""Clears n messages"""
	if ctx.message.author.server_permissions.manage_messages:
		n += 1
		await bot.purge_from(ctx.message.channel, limit=n)
	else:
		await bot.say("Error: you need Manage Messages permission!")

@bot.command(pass_context=True)
async def kick(ctx):
	"""kicks a user"""
	if ctx.message.author.server_permissions.kick_members:
		await bot.kick(ctx.message.mentions[0])
		await bot.say("succesfully kicked user " + str(ctx.message.mentions[0]))
	else:
		await bot.say("Error: you need Kick Members permission!")

@bot.command(pass_context=True)
async def banned(ctx):
	"""returns banned users list"""
	ban_list = await bot.get_bans(ctx.message.server)
	msg = "```"
	for discord.user in ban_list:
		msg += str(discord.user) + ", ID " + str(discord.user.id) + '\n'
	msg += "```"
	await bot.say(msg)

@bot.command(pass_context=True)
async def ban(ctx):
	"""bans a user"""
	if ctx.message.author.server_permissions.ban_members:
		await bot.ban(ctx.message.mentions[0], delete_message_days=0)
		await bot.say("succesfully banned user " + str(ctx.message.mentions[0]))
	else:
		await bot.say("Error: you need Ban Members permission!")

@bot.command(pass_context=True)
async def unban(ctx, id):
	"""unbans a user"""
	if ctx.message.author.server_permissions.ban_members:
		user = await bot.get_user_info(id)
		await bot.unban(ctx.message.server, user)
		await bot.say("succesfully unbanned user " + str(user))
	else:
		await bot.say("Error: you need Ban Members permission!")

bot.run(TOKEN)
