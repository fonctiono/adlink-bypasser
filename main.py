# SCRIPTED BY visey.lol fr
import discord, os
from discord import app_commands
import requests
import json
from urllib.parse import urlparse
import time

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

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
        
@tree.command(name="bypass", description="Bypass a shortened URL")
@app_commands.describe(url="The URL to bypass")
async def bypass_command(interaction: discord.Interaction, url: str):
    if not url.startswith("https://"):
        url = "https://" + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    if domain not in ['bit.ly', 'shorturl.at']:
        response_message = "**Error:** Only bit.ly and shorturl.at URLs are supported."
    else:
        result = bypass(url)
        if result['success']:
            response_message = f"```json\nFinal URL: {result['url']}\n" \
                               f"Adlink Domain: {result['adlink']}\n" \
                               f"Time: {result['time']:.2f} seconds```"
        else:
            response_message = f"**Error:** {result['error']}"

    await interaction.response.send_message(response_message)

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}!')

# if you run on replit:
bot.run(
    os.environ
    [
    'asdafsafsafsfsfafaafsfafdafdsfdzfazsdzefqdgzdgfdszgfeadzegdafdgz'
    ]
)
# if you run on bot hosters
# bot.run('YOUR_TOKEN')
