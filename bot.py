import discord
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name='TEST SERVER')	
    channel = discord.utils.get(guild.text_channels, name='general')
    await channel.send('O bot está online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "!help":
    	await message.channel.send('Olá! Digite !source para acessar meu source code, e !author para saber sobre meu criador.')

    if message.content.lower() == '!source':
        await message.channel.send('Olá! Você pode encontrar meu source code em https://github.com/murilomenezes1/DiscordBot')
    if message.content.lower() == "!author":
    	await message.channel.send("Fui desenvolvido por Murilo Menezes para a disciplina de NLP!")

client.run(str(TOKEN))




