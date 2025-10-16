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
db_folder = "databases"

def get_database_path(name):
    return(f"{db_folder}/{name}.db")

load_dotenv()
token = os.getenv("POU_TOKEN")
db_connection = sqlite3.connect(get_database_path("default"))
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
    db_connection.close()
    db_connection = sqlite3.connect(get_database_path(database))
    db_cursor = db_connection.cursor()
    await ctx.send(f"connecting to {database}")

@client.hybrid_command(description="executes a SQL command")
@app_commands.choices(commit=[
    app_commands.Choice(name="true", value="true"),
    app_commands.Choice(name="false", value="false")
])
@app_commands.describe(commit="whether to commit all unsaved changes in the transaction")
async def exec_command(ctx, *, command:str, commit:str="false"):
    response = db_cursor.execute(command)

    if commit == "true":
        db_connection.commit()

    msg = str(response.fetchall())

    await ctx.send(f"executing: `{command}`")
    await ctx.send(f"```{msg}```")

@client.hybrid_command(description="commit all changes in the current transaction")
async def commit_changes(ctx):
    db_connection.commit()
    await ctx.send("changes committed")

@client.hybrid_command(description="rollbacks all changes in the current transaction")
async def rollback_changes(ctx):
    db_connection.rollback()
    await ctx.send("changes rollbacked")

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
        os.remove(get_database_path(database))
        await ctx.send(f"ok removed {database}.db")
    except Exception as e:
        await ctx.send(e)

@client.hybrid_command(description="renames a database")
async def rename_database(ctx, original_name:str, new_name:str):
    if original_name and new_name:
        try:
            os.rename(get_database_path(original_name), get_database_path(new_name))
            await ctx.send(f"ok renamed {original_name}.db to {new_name}.db, pls use /connect_database again if connected to the old database")
        except Exception as e:
            await ctx.send(e)

    else:
        await ctx.send("um pls provide both names")

@client.hybrid_command(description="backups a database into another. uncommitted changes will be discarded.")
async def backup_database(ctx, source:str, target:str):
    if source and target:
        source_connection = sqlite3.connect(get_database_path(source))
        target_connection = sqlite3.connect(get_database_path(target))

        source_connection.backup(target_connection)

        source_connection.close()
        target_connection.close()

        await ctx.send(f"backupped {source}.db to {target}.db")


# silly stuff

bot_id_list = [1186326404267266059, 839794863591260182, 944245571714170930, 1396935480284680334, 1414634216292876308]
shun_counter = 0

@client.event
async def on_message(message: discord.Message):
    await client.process_commands(message)
    if message.content.startswith('!lilshet'):
        return
    elif message.author.id not in bot_id_list:
        if "shun" in message.content.lower():
            global shun_counter
            shun_counter = shun_counter + 1
            await message.channel.send(f"shun abooz mi {shun_counter} tim")
        if "😔" in message.content.lower() or "sadege" in message.content.lower():
            await message.channel.send("firs tim meh")
        if "pou:" in message.content.lower():
            await message.channel.send("i wonder y")
        if "💩" in message.content.lower():
            await message.channel.send("(the real one TM)")
        if "love pou" in message.content.lower() or "pou so cut" in message.content.lower():
            await message.channel.send("firs tim woh")
        elif "pou" in message.content.lower():
            await message.channel.send("omg me mention! i love pous 💩💩")
        if "i wonder y" in message.content.lower():
            await message.channel.send("i wonder y tu")

@client.hybrid_command(description="shun abooz tims")
async def get_shun_abooz(ctx):
    global shun_counter
    await ctx.send(f"shun abooz mi {shun_counter} tim")

@client.hybrid_command(description="set shun abooz tim")
async def abooz_pou(ctx, tim:str="1"):
    global shun_counter
    original = shun_counter
    shun_counter = int(tim)
    await ctx.send(f"shun abooz mi from {original} tim to {shun_counter} tim")

@client.event
async def on_command_error(ctx, error):
    channel_id = 1131914463277240361
    channel = client.get_channel(channel_id)
    await channel.send(error)
    await channel.send(error.__traceback__)


keep_alive.keep_alive()
client.run(token)
