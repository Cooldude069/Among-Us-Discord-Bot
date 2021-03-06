import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import time
import json
import os
import shutil
import asyncio
from discord.utils import get
import datetime
from discord import Spotify


def get_prefix(client , message):
	c_server = message.guild
	nickname = c_server.me.display_name
	if nickname.find('-') != -1:
		n1 , n2 = nickname.split('-')
		prefix_is = n1
		return prefix_is

	if nickname.find("-") == -1:
		prefix_is = "a!"
		return prefix_is

client = commands.Bot(command_prefix= get_prefix)
client.remove_command('help')
status = cycle(["49,675 users" , "a!help"])

@client.event
async def on_ready():
	change_status.start()
	print("Bot is ready.")

@client.command()
async def p_e(ctx):
	for guild in client.guilds:
		for i in range(len(guild.emojis)):
			if guild.emojis[i].animated:
				await ctx.send(guild.emojis[i])
		
	print("Process finished")

@tasks.loop(minutes=60)
async def change_status():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening , name = next(status)))

@client.command(aliases = ["Emoji" , "EMOJI"])
async def emoji(ctx):
	await start_log("emoji")
	users = await get_log_data()
	await update_log("emoji")
	emojis = ["<:yes:759276088412471316>" , "<:why:759276133157044264>" , "<:whoIsImposter:759278022686670880>" , "<:whoareu:759275487222169600>" , "<:what:759276168679129108>",  "<:ruImposter:759275533023444992>" , "<:IsawUkilled:759275796816461834>" , "<:IdontKnow:759275922028757012>" , "<:idontkill:759275576480890880>" , "<:iamImposter:759275748778967070>" , "<:Hello:759276199406600244>" , "<:deadbody:759275974708690974>" , "<:dead:759276019303055360>" , "<:crewmate:759276054320775188>" , "<:letVoteOut:759275840948404266>"]
	emj = random.choice(emojis)
	await ctx.send(emj)

@client.command(aliases = ["RPS" , "Rps"])
async def rps(ctx):
	await start_log("1p")
	users = await get_log_data()
	await update_log("1p")
	await ctx.send("Play your move(rock/paper/scissors)")
	results = ["rock" , "paper" , "scissors"]
	def check(message):
		return message.author == ctx.author and message.channel == ctx.message.channel

	try:
		msg = await client.wait_for('message' , timeout = 30.0 , check = check)
	except asyncio.TimeoutError:
		await ctx.send("You took too long to play")
	else:
		answer = random.choice(results)
		if msg.content.lower() == "rock":
			if answer == "paper":
				await ctx.send("I chose paper and won!!, Better luck next time!")
			elif answer == "rock":
				await ctx.send("We both chose rock, Oof a TIE!!")
			elif answer == "scissors":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		elif msg.content.lower() == "paper":
			if answer == "scissors":
				await ctx.send("I chose Scissors and won!!, Better luck next time!")
			elif answer == "paper":
				await ctx.send("We both chose paper, Oof a TIE!!")
			elif answer == "rock":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		elif msg.content.lower() == "scissors":
			if answer == "rock":
				await ctx.send("I chose rock and won!!, Better luck next time!")
			elif answer == "scissors":
				await ctx.send("We both chose scissors, Oof a TIE!!")
			elif answer == "paper":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		else:
			await ctx.send("Please choose a valid option. Game Ended")

@client.command(aliases = ["Challenge" , "CHALLENGE"])
async def challenge(ctx , opponent:discord.Member):
	await start_log("2p")
	users = await get_log_data()
	await update_log("2p")

	if opponent == ctx.author:
		await ctx.send("You cannot play against yourself")
		return

	await ctx.send(f"{opponent.mention}, Do you accept the challenge?(yes/no)")
	def check(message):
		return message.channel == ctx.message.channel and message.author == opponent

	try:
		msg = await client.wait_for('message' , timeout = 30.0 , check = check)
	except asyncio.TimeoutError:
		await ctx.send("You took too long to accept")
	else:
		if msg.content.lower() == "no":
			await ctx.send("Game ended")
			return
		await ctx.send("Get ready contestants, Check your dm")
		c1 = await ctx.author.create_dm()
		c2 = await opponent.create_dm()
		await ctx.author.dm_channel.send("Game starting in 5s")
		await opponent.dm_channel.send("Game starting in 5s")
		await asyncio.sleep(3)
		embed = discord.Embed(title = "Among Us Hand cricket!" , color = discord.Color.red())
		embed.set_image(url = "https://media.tenor.com/images/2ab9e2f21aece2154bc36bf6c9b2e09e/tenor.gif")
		embed.add_field(name = "Play your move(rock/paper/scissors)" , value = "** **")
		embedo = discord.Embed(title = "Among Us Hand cricket!" , color = discord.Color.blue())
		embedo.set_image(url = "https://media.tenor.com/images/d075fedb342564f3aefb67ff7895b953/tenor.gif")
		embedo.add_field(name = "Play your move(rock/paper/scissors)" , value = "** **")
		await ctx.author.dm_channel.send(embed = embed)
		await opponent.dm_channel.send(embed = embedo)
		def checka(message):
			return isinstance(message.channel, discord.channel.DMChannel) and message.author == ctx.author
		def checko(message):
			return isinstance(message.channel, discord.channel.DMChannel) and message.author == opponent
		try:
			msg = await client.wait_for('message' , timeout = 30.0 , check = checka)
			mtg = await client.wait_for('message' , timeout = 30.0 , check = checko)
			answer = mtg.content.lower()
		except asyncio.TimeoutError:
			await ctx.send("You took too long to respond")
		else:
			await c1.send(f"Your opponent chose {answer}")
			await c2.send(f"Your opponent chose {msg.content}")
			if msg.content.lower() == "rock":
				if answer == "paper":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "rock":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "scissors":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			elif msg.content.lower() == "paper":
				if answer == "scissors":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "paper":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "rock":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			elif msg.content.lower() == "scissors":
				if answer == "rock":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "scissors":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "paper":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			else:
				await c1.send("Please choose a valid option. Game Ended")




@client.command(aliases = ["Coin_flip" , "COIN_FLIP" , "Flip_coin" , "flip_coin" , "FLIP_COIN" , "FLIP" , "Flip" , "coin_flip"])
async def flip(ctx):
	await start_log("coin_flip")
	users = await get_log_data()
	await update_log("coin_flip")
	embed = discord.Embed(title = f"{ctx.author.display_name} Has flipped a coin" , color = discord.Color.orange())
	embed.set_thumbnail(url = ctx.author.avatar_url)
	embed.set_image(url = "https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
	links = ["https://media.tenor.com/images/d9cc74bec0a2a582d1887045c62595c9/tenor.gif" , "https://media.tenor.com/images/1de5555846dc3e3cd279983cbd2e986d/tenor.gif"]
	msg = await ctx.send(embed = embed)
	nembed = discord.Embed(title = f"And the result is ....." , color = discord.Color.orange())
	nembed.set_image(url = random.choice(links)) 
	await asyncio.sleep(8)
	await msg.edit(embed = nembed)

@client.command(aliases = ["Add_emoji" , "ADD_EMOJI" , "Add" , "add" , "ADD"])
async def add_emoji(ctx , name = None, number = 0):
	await start_log("add_emoji")
	users = await get_log_data()
	await update_log("add_emoji")
	emojis = ["<:yes:759276088412471316>" , "<:why:759276133157044264>" , "<:whoIsImposter:759278022686670880>" , "<:whoareu:759275487222169600>" , "<:what:759276168679129108>",  "<:ruImposter:759275533023444992>" , "<:IsawUkilled:759275796816461834>" , "<:IdontKnow:759275922028757012>" , "<:idontkill:759275576480890880>" , "<:iamImposter:759275748778967070>" , "<:Hello:759276199406600244>" , "<:deadbody:759275974708690974>" , "<:dead:759276019303055360>" , "<:crewmate:759276054320775188>" , "<:letVoteOut:759275840948404266>" , "<:me_ghost:763035423769100288>" , "<:shy_witch:763035032033165322>" , "<:doc_imposter:763035079706017832>" , "<:imposter:763035386585808916>" , "<:leave_me:763035256139022346>" , "<:announce:763035338842832897>" , "<:magician:763035212245368852>" , "<:not_me:763035139948281856>"]
	if name == None:
		embed = discord.Embed(title = "Emojis" , color = discord.Color.red())
		for i in range(len(emojis)):
			embed.add_field(name = "** **" , value = f"{i+1} : {emojis[i]}")

		embed.set_footer(text = "You need manage emojis permissions to use this" , icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS4HiptS4Q-kl6KMfBkVeJXTMqoVL4gO0rbaQ&usqp=CAU")

		await ctx.send(embed = embed)
		await ctx.send(f"Use add_emoji <name> <number> to add the emoji to your server Or add_emoji full-pack to add all emojis")
	
	elif name == "full-pack":
		if ctx.author.guild_permissions.manage_emojis:
			emojid = ["759276088412471316" , "759276133157044264" , "759278022686670880" , "759275487222169600" , "759276168679129108",  "759275533023444992" , "759275796816461834" , "759275922028757012" , "759275576480890880" , "759275748778967070" , "759276199406600244" , "759275974708690974" , "759276019303055360" , "759276054320775188" , "759275840948404266" , "763035423769100288" , "763035032033165322" , "763035079706017832" , "763035386585808916" , "763035256139022346" , "763035338842832897" , "763035212245368852" , "763035139948281856"]

			for emoji_id in emojid:
				emj = client.get_emoji(int(emoji_id))
				url = emj.url
				img = await url.read()
				emoji_name = emj.name
				await ctx.author.guild.create_custom_emoji(name = emoji_name , image = img)
			
			await ctx.send("Emojis successfully created")
		else:
			await ctx.send("You don't have the necessary permissions")
	else:
		if ctx.author.guild_permissions.manage_emojis:
			needed = number - 1
			emojid = ["759276088412471316" , "759276133157044264" , "759278022686670880" , "759275487222169600" , "759276168679129108",  "759275533023444992" , "759275796816461834" , "759275922028757012" , "759275576480890880" , "759275748778967070" , "759276199406600244" , "759275974708690974" , "759276019303055360" , "759276054320775188" , "759275840948404266" , "763035423769100288" , "763035032033165322" , "763035079706017832" , "763035386585808916" , "763035256139022346" , "763035338842832897" , "763035212245368852" , "763035139948281856"]
			emid = int(emojid[needed])
			emoji = client.get_emoji(emid)
			url = emoji.url
			img = await url.read()
			await ctx.author.guild.create_custom_emoji(name = name , image = img)
			await ctx.send("Emoji created")
		else:
			await ctx.send("You dont have the necessary permissions")



@client.command(aliases = ["Invite" , "INVITE"])
async def invite(ctx):
	await start_log("invite")
	users = await get_log_data()
	await update_log("invite")
	embed = discord.Embed(title = "Invite Among Us bot using the below link" , color = discord.Color.green())
	embed.add_field(name = "Go to the official server" , value = "https://discord.gg/tgyW2Jz")
	embed.add_field(name = "Invite the best Among Us Bot" , value = "https://bit.ly/3ceYuEW")
	embed.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
	await ctx.send(embed = embed)

@client.command(aliases = ["Report" , "REPORT"])
async def report(ctx, * ,problem = None):
	server = discord.utils.get(client.guilds , id = 757239002826014731)
	cnl = server.get_channel(763763201069940756)
	embed = discord.Embed(title = f"{ctx.author.display_name}'s Complaint/report" , color = discord.Color.orange())
	embed.add_field(name = "** **" , value = problem)
	await cnl.send(embed = embed)
	

@client.command(aliases = ["Vc" , "VC"])
async def vc(ctx , code = None , server = None):
	await start_log("vc")
	users = await get_log_data()
	await update_log("vc")
	if code == None:
		await ctx.send("Please enter the code of your Among Us game")
		msg = await client.wait_for('message' ,  check=lambda message: message.author == ctx.author)
		print(msg.content)
	if ctx.guild.id == 757239002826014731:
		cat = discord.utils.get(ctx.guild.categories , id = 757247392981450813)
	else:
		cat = ctx.message.channel.category

	await ctx.author.guild.create_voice_channel(name = f"🚀{code} -> {server}" , category = cat , user_limit = 11)
	vch = discord.utils.get(ctx.author.guild.voice_channels , name = f"🚀{code} -> {server}")
	vch.permissions_for(ctx.author)
	await ctx.author.create_dm()
	await ctx.author.dm_channel.send("Your voice channel has been created successfully, It will be deleted after 30 minutes. Here is your link.")
	link = await vch.create_invite(max_uses = 11)
	await ctx.author.dm_channel.send(f"{link}")
	await asyncio.sleep(1800)
	await vch.delete()

async def get_log_data():
	with open("logs.json" , "r") as f:
		users = json.load(f)

	return users

async def start_log(command_name):
	users = await get_log_data()

	if command_name in users:
		return False
	else:
		users[command_name] = {}
		users[command_name]["count"] = 0

	with open("logs.json" , "w") as f:
		json.dump(users,f)
	return True

async def update_log(command_name):
	users = await get_log_data()

	users[command_name]["count"] += 1

	with open("logs.json" , "w") as f:
		json.dump(users,f)

	bal = users[command_name]["count"]

	return bal


@client.command(aliases = ["Stats" , "STATS"])
async def stats(ctx):
	embed = discord.Embed(title = "Among us Bot stats!" , color = discord.Color.green())
	embed.add_field(name = "Total servers " , value = f"`{len(client.guilds)}`")
	count = 0
	for guild in client.guilds:
		count += len(guild.members)

	embed.add_field(name = "Total members" , value = f"`{count}`")

	users = await get_log_data()

	embed.add_field(name = "Today's commands stats!" , value = "** **" , inline = False)
	c_count =  0
	for used in users:
		c_count += users[used]["count"]

	embed.add_field(name = "Total commands used" , value = f"`{c_count}`" , inline = False)

	for used in users:
		embed.add_field(name = f"{used}" , value = f'''`{users[used]["count"]}`''')

	embed.set_thumbnail(url = "https://5droid.ru/uploads/posts/2020-02/1581588210_among-us.png")

	await ctx.send(embed = embed)

@client.command(aliases = ["Mute" , "MUTE"])
async def mute(ctx):
	await start_log("mute")
	users = await get_log_data()
	await update_log("mute")
	if ctx.author.voice.channel == None:
		await ctx.send("You have to be connected to a voice channel first")
		return

	await ctx.author.edit(mute = True)

	for member in ctx.author.voice.channel.members:
		if member.top_role < ctx.author.top_role:
			await member.edit(mute = True)

@client.command(aliases = ["Unmute" , "UNMUTE"])
async def unmute(ctx):
	await start_log("unmute")
	users = await get_log_data()
	await update_log("unmute")
	if ctx.author.voice.channel == None:
		await ctx.send("You have to be connected to a voice channel first")
		return

	await ctx.author.edit(mute = False)
		
	for member in ctx.author.voice.channel.members:
		if member.top_role < ctx.author.top_role:
			await member.edit(mute = False)



@client.command(aliases = ["Guide" , "GUIDE"])
async def guide(ctx):
	await start_log("guide")
	users = await get_log_data()
	await update_log("guide")
	embed = discord.Embed(title = "Among Us Guide Page" , color = discord.Color.orange())
	embed.set_image(url = "https://media.tenor.com/images/c3b4688a7189725f664c9c6af0b33003/tenor.gif")
	msg = await ctx.send(embed = embed)
	await asyncio.sleep(30)
	guide = discord.Embed(title = "Among Us Guide Page" , color = discord.Color.orange())
	guide.add_field(name = ":map:Full Guide" , value = "https://bit.ly/2ZHsF2A")
	guide.add_field(name = "<:among_us:755993889508163655>Crewmate" , value = "https://bit.ly/3khxtU6")
	guide.add_field(name = ":detective:Imposter" , value = "https://bit.ly/2ZHsF2A")
	guide.add_field(name = "To learn about maps use the below command" , value = "a!maps" , inline = False)
	guide.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
	await msg.edit(embed = guide)

@client.command(aliases = ['Maps' , 'MAPS'])
async def maps(ctx):
	await start_log("maps")
	users = await get_log_data()
	await update_log("maps")
	among = discord.Embed(title = "Choose one of the below maps by typing the command `a!{map name}`.\n Eg. a!skeld \nyou can choose between skeld, mirahq and polus" , color = discord.Color.orange())
	among.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
	await ctx.send(embed = among)
	
@client.command(aliases = ['Skeld' , 'SKELD'])
async def skeld(ctx):
	await start_log("skeld")
	users = await get_log_data()
	await update_log("skeld")
	skeld = discord.Embed(title = 'Skeld' , color = discord.Color.orange())
	skeld.set_image(url = 'https://preview.redd.it/tv8ef4iqszh41.png?auto=webp&s=46faf550020fd59c8d8bab29705b0fcb80521850')
	await ctx.send(embed = skeld)
	
@client.command(aliases = ['Polus' , 'POLUS'])
async def polus(ctx):
	await start_log("polus")
	users = await get_log_data()
	await update_log("polus")
	polus = discord.Embed(title = 'Polus' , color = discord.Color.orange())
	polus.set_image(url = 'https://vignette.wikia.nocookie.net/among-us-wiki/images/4/4c/Polus.png/revision/latest?cb=20200907133344')
	await ctx.send(embed = polus)
	
@client.command(aliases = ['Mirahq' , 'MIRAHQ'])
async def mirahq(ctx):
	await start_log("mirahq")
	users = await get_log_data()
	await update_log("mirahq")
	mira = discord.Embed(title = 'Mira HQ' , color = discord.Color.orange())
	mira.set_image(url = 'https://vignette.wikia.nocookie.net/among-us-wiki/images/0/0a/Mirahq.png/revision/latest?cb=20200907132939')
	await ctx.send(embed = mira)

@client.command(aliases = ["Kill" , "KILL" , "hit" , "Hit" , "HIT"])
async def kill(ctx , user:discord.Member = None):
	await start_log("kill")
	users = await get_log_data()
	await update_log("kill")
	if user == ctx.author:
		link = "https://media.tenor.com/images/084529f26cc165e65ea6009206174f29/tenor.gif"
		lit = f"{ctx.author.display_name} Killed himself"
	else:
		links = ["https://media.tenor.com/images/2ad01fc73cc91abd54069f2e8deb50cc/tenor.gif","https://media.tenor.com/images/49f4a71df065a3bf90d9ebfd0cbd2d58/tenor.gif" , "https://media.tenor.com/images/091a8ed3a3896e8f3b4bffa02c298491/tenor.gif" , "https://media.tenor.com/images/f2295524300b47930f650f82080e0bb5/tenor.gif" ,"https://media.tenor.com/images/a461243877f3e2494a4c69999b232a97/tenor.gif" ,"https://media.tenor.com/images/7bb1baedb25f70d66d811088e464c4a3/tenor.gif" ,"https://media.tenor.com/images/d46c724d422714d738a84a51f1caf00b/tenor.gif" , "https://media.tenor.com/images/a166604b0b8f34779dbbd2dd690efb58/tenor.gif"]
		link = random.choice(links)
		lit = f"{ctx.author.display_name} Killed {user.display_name}"
	embed = discord.Embed(title = lit , color = discord.Color.red())
	embed.set_image(url = link)
	await ctx.send(embed = embed)

@client.command(aliases = ["Ping" , "PING"])
async def ping(ctx):
	await start_log("ping")
	users = await get_log_data()
	await update_log("ping")
	await ctx.send(f'Ping: {round(client.latency * 1000)} ms')


@client.event
async def on_guild_join(guild):
	cnl = client.get_channel(759265178616332308)
	await cnl.send(f"Among Us bot was added to {guild.name}")

@client.command(aliases=['HELP', 'Help'])
async def help(ctx):
	await start_log("help")
	users = await get_log_data()
	await update_log("help")
	await ctx.message.author.create_dm()
	helpm  = discord.Embed(title = f"Among Us Help!" , color = discord.Color.darker_grey())
	helpm.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
	prfx = get_prefix(client = client , message = ctx.message)
	helpm.add_field(name = f"Hey! My prefix is {prfx}" , value = "So Lets go through my commands" , inline = False)
	helpm.add_field(name = "To set a custom prefix change the bot's nickname to {prefix}-{any name u want}" , value = "Eg. if the prefix is ?, change nickname to ?-Among Us")
	helpm.add_field(name = ":one: guide -> will guide you" , value = "This will give you all the required information about the game" , inline = False)
	helpm.add_field(name = ":two: maps -> will show you all maps" , value = "This will give you the blueprints of all the maps" , inline = False)
	helpm.add_field(name = ":three: ping -> Shows the bot's latency" , value = "Pong!" , inline = False)
	helpm.add_field(name = ":four: vc {code} {server} -> Makes a special voice channel" , value = "U can invite the people you want(limit = 11)" , inline = False)
	helpm.add_field(name = ":five: invite -> Generates an invite link for the bot" , value = "You can get the link to the official server")
	helpm.add_field(name = ":six: kill/hit {user} -> Just a fun command" , value = "try it, it's epic" , inline = False)
	helpm.add_field(name = ":seven: emoji -> Generates a random Among Us emoji" , value = "I love those Emoji's" , inline = False)
	helpm.add_field(name = ":eight: add_emoji/add -> adds the among us emoji to your server" , value = "use a!add to know how to go forward" , inline = False)
	helpm.add_field(name = ":nine: mute -> Mutes the people in the voice channel" , value = "Only the people who have a role lower than you will be muted" , inline = False)
	helpm.add_field(name = ":keycap_ten: unmute -> Unmutes the people in the voice channel" , value = "Keep the discussions going" , inline = False)
	helpm.add_field(name = ":one::one: report {complain} -> Report's the complain to the bot's devs" , value = "Don't use this feature unnecessarily" , inline = False)
	helpm.add_field(name = ":fire:New Features!!:fire:" , value = "** **" , inline = False)
	helpm.add_field(name = ":one::two: rps -> Starts a rock, paper , scissors game with the bot" , value = "It is really fun" , inline = False)
	helpm.add_field(name = ":one::three: challenge {user} -> Play a 1v1 rock, paper scissors with your friend" , value = "It takes place in Dm, Don't worry" , inline = False)
	helpm.add_field(name = ":one::four: flip -> Flips a coin for you" , value = "Solve your disputes with just a flip of the coin" , inline = False)
	await ctx.message.author.dm_channel.send(embed = helpm)
	await ctx.send("You've got mail!!")

client.run("TOKEN")