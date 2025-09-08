import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import keep_alive
import sqlite3

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
token = os.getenv("POU_TOKEN")
db_folder = "databases"
db_connection = sqlite3.connect(f"{db_folder}/default.db")
db_cursor = db_connection.cursor()

client = commands.Bot(
    command_prefix=[f"!lilshet "],
    intents=intents)

@client.event
async def on_ready():
    print('Roboduck is ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="firs tim meh"))
    await client.tree.sync()

@client.hybrid_command()
async def connect_database(ctx, database:str):
    global db_connection
    global db_cursor
    db_connection = sqlite3.connect(f"{db_folder}/{database}.db")
    db_cursor = db_connection.cursor()
    await ctx.send(f"connecting to {database}")

@client.hybrid_command()
@app_commands.choices(commit=[
    app_commands.Choice(name="true", value="true"),
    app_commands.Choice(name="false", value="false")
])
async def exec_command(ctx, *, command:str, commit:str="false"):
    response = db_cursor.execute(command)

    if commit == "true":
        db_connection.commit()

    msg = str(response.fetchall())

    await ctx.send(f"executing: `{command}`")
    await ctx.send(f"```{msg}```")

@client.hybrid_command()
async def commit_changes(ctx):
    db_connection.commit()
    await ctx.send("changes committed")

@client.hybrid_command()
async def list_databases(ctx):
    databases_list = os.listdir(db_folder)
    for database in databases_list:
        if not database.endswith(".db"):
            databases_list.remove(database)

    msg = "\n".join(databases_list)
    await ctx.send(msg)


bot_id_list = [1186326404267266059, 839794863591260182, 944245571714170930, 1396935480284680334, 1414634216292876308]

@client.event
async def on_message(message: discord.Message):
    await client.process_commands(message)
    if message.content.startswith('!lilshet'):
        return
    elif message.author.id not in bot_id_list:
        if "shun" in message.content.lower():
            await message.channel.send("shun abooz mi")
        if "😔" in message.content.lower() or "sadege" in message.content.lower():
            await message.channel.send("firs tim meh")
        if "pou:" in message.content.lower():
            await message.channel.send("i wonder y")


keep_alive.keep_alive()
client.run(token)