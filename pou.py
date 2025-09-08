import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import keep_alive
import sqlite3

intents = discord.Intents.all()
intents.members = True

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="ITS SHAUN THE SHEEP!"))
    await client.tree.sync()

@client.hybrid_command()
async def connect_database(ctx, database:str):
    global db_connection
    global db_cursor
    db_connection = sqlite3.connect(f"{db_folder}/{database}.db")
    db_cursor = db_connection.cursor()
    await ctx.send(f"connecting to {database}")

@client.hybrid_command()
async def exec_command(ctx, command:str):
    response = db_cursor.execute(command)
    await ctx.send(f"executing {command}")
    await ctx.send(str(response.fetchall()))

@client.hybrid_command()
async def list_databases(ctx):
    databases_list = os.listdir(db_folder)
    for database in databases_list:
        if not database.endswith(".db"):
            databases_list.remove(database)

    msg = "\n".join(databases_list)
    await ctx.send(msg)


keep_alive.keep_alive()
client.run(token)