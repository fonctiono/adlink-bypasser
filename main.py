# SCRIPTED BY pulse.zip
# SCRIPTED BY pulse.zip
# SCRIPTED BY pulse.zip

# Services
import discord
import os
from discord import app_commands
import requests
import json
from urllib.parse import urlparse
import time

# Setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Storage
LOGS_FILE = "logs.txt"

# Classes
def bypass(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    start_time = time.time()
    try:
        response = requests.head(url, headers=headers, allow_redirects=True)
        final_url = response.url

        adlink = urlparse(url).netloc
        end_time = time.time()
        elapsed_time = end_time - start_time

        return {
            'success': True,
            'url': final_url,
            'adlink': adlink,
            'time': elapsed_time
        }
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        return {'success': False, 'error': f"Request error: {str(e)}"}

# Commands
@tree.command(name="bypass", description="Bypass a shortened URL")
@app_commands.describe(url="The URL to bypass")
async def bypass_command(interaction: discord.Interaction, url: str):
    if not url.startswith("https://"):
        url = "https://" + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    if domain not in ['bit.ly', 'shorturl.at']:
        response = {
            "success": False,
            "error": "Only bit.ly and shorturl.at URLs are supported."
        }
    else:
        result = bypass(url)
        if result['success']:
            with open(LOGS_FILE, 'r') as stats:
                lines_count = len(stats.readlines()) # counts total lines of logs.txt (bypassed urls logs)
            response = {
                "success": True,
                "url": result['url'],
                "adlink": result['adlink'],
                "time": f"{result['time']:.2f} seconds",
                "stats": f"{lines_count} bypasses so far"
            }
            with open(LOGS_FILE, 'a') as logs:
                logs.write(f"Bypassed {url} > {result['url']}\n")
        else:
            response = {
                "success": False,
                "error": result['error']
            }

    response_message = f"```json\n{json.dumps(response, indent=4)}\n```"
    await interaction.response.send_message(response_message)

@tree.command(name="export", description="Export the logs.txt file and send it to your DM (Admin only)")
async def export_command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("**Error:** You do not have permission to use this command.", ephemeral=True)
        return

    try:
        await interaction.user.send(file=discord.File(LOGS_FILE))
        await interaction.response.send_message("Logs have been sent to your DM.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"**Error:** Unable to send the logs file. {str(e)}", ephemeral=True)

# Startup
@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}!')
    print(f"Bot ID: {bot.user.id}")

# if you run on replit:
# bot.run(os.environ['asdafsafsafsfsfafaafsfafdafdsfdzfazsdzefqdgzdgfdszgfeadzegdafdgz']) # asdaf... is the secret name (rename if you want)

# if you run on bot hosters
bot.run('DISCORD_TOKEN') # replace with your bot token
