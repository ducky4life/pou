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

@client.hybrid_command(description="connect to a database")
async def connect_database(ctx, database:str):
    global db_connection
    global db_cursor
    db_connection = sqlite3.connect(f"{db_folder}/{database}.db")
    db_cursor = db_connection.cursor()
    await ctx.send(f"connecting to {database}")

@client.hybrid_command(description="executes a SQL command")
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

@client.hybrid_command(description="commit all changes in the current transactions")
async def commit_changes(ctx):
    db_connection.commit()
    await ctx.send("changes committed")

@client.hybrid_command(description="list all databases")
async def list_databases(ctx):
    databases_list = os.listdir(db_folder)
    for database in databases_list:
        if not database.endswith(".db"):
            databases_list.remove(database)

    msg = "\n".join(databases_list)
    await ctx.send(msg)

@client.hybrid_command(description="deletes a database")
async def delete_database(ctx, database:str):
    try:
        os.remove(f"{db_folder}/{database}.db")
        await ctx.send(f"ok removed {database}.db")
    except Exception as e:
        await ctx.send(e)

@client.hybrid_command(description="renames a database")
async def rename_database(ctx, original_name:str, new_name:str):
    if original_name and new_name:
        try:
            os.rename(f"{db_folder}/{original_name}.db", f"{db_folder}/{new_name}.db")
            await ctx.send(f"ok renamed {original_name}.db to {new_name}.db, pls use /connect_database again if connected to the old database")
        except Exception as e:
            await ctx.send(e)

    else:
        await ctx.send("um pls provide both names")


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