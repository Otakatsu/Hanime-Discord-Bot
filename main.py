import json
import os
import requests
import subprocess

import discord
from discord.ext import commands, tasks

intents = discord.Intents.all()

prefix = os.environ.get("prefix", None) 
token = os.environ.get("token", None)


bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{prefix}help\n Made By Moezilla"))


@bot.command()
async def help(ctx):
    embed = discord.Embed(description=f"Hanime Discord Bot\n{prefix}search Kara no Shoujo 1\n{prefix}info kara-no-shoujo-1\n{prefix}watch kara-no-shoujo-1", color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command()
async def search(ctx, *args):
    name = ' '.join(args)
    if name == "":
        embed = discord.Embed(description=f"{prefix}search <space> hanime name", color=discord.Color.green())
        embed.set_image(url="https://media.discordapp.net/attachments/1027884090453667860/1028688677544673371/cdeae50a8a23041b01935.mp4")
        await ctx.send(embed=embed)
    if not name == "":
        url = f"https://apikatsu.otakatsu.studio/api/hanime/search?query={name}&page=0"
        result = requests.get(url) 
        result = result.json()
        K = result["response"]
        keyb = []
        embed = discord.Embed(description=f"Found Hanime - {name}", color=discord.Color.green())
        for x in K:
            id = x["slug"]
            name = x["name"]
            keyb.append(embed.add_field(name=f"{name}", value=f"{id}",inline=True))
        if keyb == []:
            embed = discord.Embed(description=f"No results found, Please check the Spelling and try again", color=discord.Color.green())
            await ctx.send(embed=embed)
        if not keyb == []:     
            await ctx.send(embed=embed)

@bot.command()
async def info(ctx, *args):
    name = ' '.join(args)
    url = f"https://apikatsu.otakatsu.studio/api/hanime/details?id={name}" 
    result = requests.get(url) 
    result = result.json()   
    description = result["description"]
    name = result["name"]
    img = result["poster"]
    view = result["views"]     
    released_date = result["released_date"]
    embed = discord.Embed(title=name, description=description, color=discord.Color.green())
    embed.add_field(name=f"View", value=view, inline=True)
    embed.add_field(name=f"Released Date", value=released_date, inline=True)   
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command()
async def watch(ctx, *args):
    name = ' '.join(args)
    url = f"https://apikatsu.otakatsu.studio/api/hanime/link?id={name}" 
    result = requests.get(url) 
    result = result.json()
    k = f"https://apikatsu.otakatsu.studio/api/hanime/details?id={name}" 
    results = requests.get(k) 
    results = results.json()   
    name = results["name"]
    url = result["data"][0]["url"]
    if not url == "":
        url1 = result["data"][0]["url"]
        url2 = result["data"][1]["url"]
        url3 = result["data"][2]["url"]
        embed = discord.Embed(description=f"{name} Watch Link", color=discord.Color.green())
        embed.add_field(name=f"360p", value=url3, inline=True)
        embed.add_field(name=f"480p", value=url2, inline=True)   
        embed.add_field(name=f"720p", value=url1, inline=True)   
        await ctx.send(embed=embed)
    if url == "":
        url1 = result["data"][1]["url"]
        url2 = result["data"][2]["url"]
        url3 = result["data"][3]["url"]
        embed = discord.Embed(description=f"{name} Watch Link", color=discord.Color.green())
        embed.add_field(name=f"360p", value=url3, inline=True)
        embed.add_field(name=f"480p", value=url2, inline=True)   
        embed.add_field(name=f"720p", value=url1, inline=True)   
        await ctx.send(embed=embed)
               
     
bot.run(token)
    
