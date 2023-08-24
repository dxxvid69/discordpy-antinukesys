import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Your server's threshold for triggering anti-nuke
NUKE_ACTION_THRESHOLD = 3

# Dictionary to keep track of actions by users
user_actions = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await check_nuke(member.guild)

@bot.event
async def on_member_remove(member):
    await check_nuke(member.guild)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id not in user_actions:
        user_actions[user_id] = []

    user_actions[user_id].append(message.id)
    await check_nuke(message.guild)

async def check_nuke(guild):
    if not guild:
        return

    for user_id, actions in user_actions.items():
        if len(actions) >= NUKE_ACTION_THRESHOLD:
            user = guild.get_member(user_id)
            if user:
                await user.ban(reason="Nuke detection: Too many actions")
    
    # Clear user actions after a while
    for user_id in user_actions.copy():
        if guild.get_member(user_id):
            user_actions[user_id] = []
        else:
            del user_actions[user_id]

bot.run("YOUR_BOT_TOKEN")

# This is just a starting point and may need further refinement and customization based on your server's specific requirements. Keep in mind that an effective anti-nuke system could involve a wide range of actions, including detecting mass message deletion, role changes, channel deletions, etc. This example focuses on message actions as an illustration.

# Please replace `"YOUR_BOT_TOKEN"` with your actual bot token. Also, remember that a sophisticated anti-nuke system might involve using a database to store information about user actions and implementing more advanced heuristics to identify suspicious behavior.
