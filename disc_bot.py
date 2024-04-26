from discord.ext import commands
from dotenv import load_dotenv
from responses import get_response
import discord
import asyncio
import yt_dlp
import os

def run_bot():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	intents = discord.Intents.default()
	intents.message_content = True
	client = commands.Bot(command_prefix="!", intents=intents)

	voice_clients = {}
	queues = {}
	yt_dl_options = {"format": "bestaudio/best"}
	ytdl = yt_dlp.YoutubeDL(yt_dl_options)

	ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

	@client.event
	async def on_ready():
		print(f'{client.user} is now running!')

	async def play_next(ctx):
		if queues[ctx.guild.id] != []:
			link = queues[ctx.guild.id].pop(0)
			await play(ctx, link)

	@client.command(name="play")
	async def play(ctx, link):
		try:
			if ctx.author.voice is None:
				return await ctx.send("Tu tem que tá em um canal de voz né doente...")

			voice_client = await ctx.author.voice.channel.connect()
			voice_clients[ctx.guild.id] = voice_client
		except Exception as e:
			print(e)
		try:
			loop = asyncio.get_event_loop()
			data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

			song = data['url']
			player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

			voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
		except Exception as e:
			print(e)


	@client.command(name="clear")
	async def clear_queue(ctx):
		if ctx.guild.id in queues:
			queues[ctx.guild.id].clear()
			await ctx.send("A merda da fila tá vazia agora, satisfeito?!")
		else:
			await ctx.send("Não tem fila pra limpar filhote de estrume!")

	@client.command(name="pause")
	async def pause(ctx):
		try:
			voice_clients[ctx.guild.id].pause()
		except Exception as e:
			print(e)

	@client.command(name="resume")
	async def resume(ctx):
		try:
			voice_clients[ctx.guild.id].resume()
		except Exception as e:
			print(e)

	@client.command(name="skip")
	async def skip(ctx):
		try:
			voice_clients[ctx.guild.id].stop()
			await play_next(ctx)
			await ctx.send("Skippei essa merda!")
		except Exception as e:
			print(e)

	@client.command(name="stop")
	async def stop(ctx):
		try:
			voice_clients[ctx.guild.id].stop()
			await voice_clients[ctx.guild.id].disconnect()
			del voice_clients[ctx.guild.id]
		except Exception as e:
			print(e)

	@client.command(name="queue")
	async def queue(ctx, url):
		if ctx.guild.id not in queues:
			queues[ctx.guild.id] = []
		queues[ctx.guild.id].append(url)
		await ctx.send("Adicionei essa lixeira na fila!")

	async def send_msg(messsage, user_message: str) -> None:
		if not user_message:
			print('(Message was empty, no intents)')
			return

		if is_private := user_message[0] == '?':
			user_message = user_message[1:]
		try:
			response: str = get_response(user_message)
			await messsage.author.send(response) if is_private else await messsage.channel.send(response)
		except Exception as e:
			print(e)

	@client.event
	async def on_message(message) -> None:
		if message.author == client.user:
			return

		username: str = str(message.author)
		user_message: str = message.content
		channel: str = str(message.channel)

		print(f'[{channel}] {username}: "{user_message}"')
		await send_msg(message, user_message)

	client.run(token=TOKEN)
