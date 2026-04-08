"""
Main Discord Bot - HemantGamer SMP
Features: Anti-Link, Image Control, Bad Word Filter, Music Player
"""

import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta
from config import BOT_TOKEN, OWNER_ID, TIMEOUT_DURATION, SERVER_LINKS, DESCRIPTION

# Setup Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents, description=DESCRIPTION)

# Storage for settings
SETTINGS_FILE = "bot_settings.json"

def load_settings():
    """Load bot settings from file"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        "allowed_links": [],
        "allowed_images": [],
        "bad_words": ["badword"],
        "disabled_users": {},
        "muted_users": {}
    }

def save_settings(settings):
    """Save bot settings to file"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def is_owner(ctx):
    """Check if user is bot owner"""
    return ctx.author.id == OWNER_ID

# Load settings at startup
bot.settings = load_settings()

@bot.event
async def on_ready():
    """Bot ready event"""
    print(f"✅ Bot logged in as {bot.user}")
    print(f"🎮 Powered by HemantGamer SMP")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="🎮 HemantGamer SMP | /help"
        )
    )

@bot.event
async def on_message(message):
    """Handle all messages for filtering"""
    # Ignore bot messages
    if message.author.bot:
        return

    guild_id = str(message.guild.id) if message.guild else "dm"
    user_id = str(message.author.id)

    # Check if user is muted
    if guild_id in bot.settings["muted_users"]:
        if user_id in bot.settings["muted_users"][guild_id]:
            mute_time = bot.settings["muted_users"][guild_id][user_id]
            if datetime.now().timestamp() < mute_time:
                await message.delete()
                return
            else:
                del bot.settings["muted_users"][guild_id][user_id]
                save_settings(bot.settings)

    # Skip owner
    if message.author.id == OWNER_ID:
        await bot.process_commands(message)
        return

    # Anti-Link Check
    if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
        if user_id not in bot.settings["allowed_links"]:
            try:
                await message.author.timeout(
                    timedelta(seconds=TIMEOUT_DURATION),
                    reason="Sent unauthorized link"
                )
                await message.delete()
                embed = discord.Embed(
                    title="❌ Links Not Allowed",
                    description=f"{message.author.mention} timed out for 1 minute\nUse authorized channels to share links.",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed, delete_after=10)
            except Exception as e:
                print(f"Error timing out user: {e}")
            return

    # Image Check
    if message.attachments:
        has_images = any(
            att.content_type and att.content_type.startswith('image/')
            for att in message.attachments
        )
        if has_images and user_id not in bot.settings["allowed_images"]:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🖼️ Images Not Allowed",
                    description=f"{message.author.mention} only owners can send images.",
                    color=discord.Color.orange()
                )
                await message.channel.send(embed=embed, delete_after=10)
            except Exception as e:
                print(f"Error handling image: {e}")
            return

    # Bad Words Check
    message_lower = message.content.lower()
    for bad_word in bot.settings["bad_words"]:
        if bad_word.lower() in message_lower:
            try:
                await message.author.timeout(
                    timedelta(seconds=TIMEOUT_DURATION),
                    reason=f"Used bad word: {bad_word}"
                )
                await message.delete()
                embed = discord.Embed(
                    title="⚠️ Bad Word Detected",
                    description=f"{message.author.mention} timed out for 1 minute",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed, delete_after=10)
            except Exception as e:
                print(f"Error handling bad word: {e}")
            return

    await bot.process_commands(message)

# ==================== COMMANDS ====================

@bot.command()
async def allow_link(ctx, user: discord.User = None):
    """Owner: Whitelist user to send links"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if user is None:
        await ctx.send("❌ Please mention a user: `/allow_link @username`")
        return

    if str(user.id) not in bot.settings["allowed_links"]:
        bot.settings["allowed_links"].append(str(user.id))
        save_settings(bot.settings)
        embed = discord.Embed(
            title="✅ Link Access Granted",
            description=f"{user.mention} can now send links",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ {user.mention} already has link access")

@bot.command()
async def remove_link(ctx, user: discord.User = None):
    """Owner: Remove link whitelist from user"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if user is None:
        await ctx.send("❌ Please mention a user: `/remove_link @username`")
        return

    if str(user.id) in bot.settings["allowed_links"]:
        bot.settings["allowed_links"].remove(str(user.id))
        save_settings(bot.settings)
        embed = discord.Embed(
            title="❌ Link Access Removed",
            description=f"{user.mention} can no longer send links",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ {user.mention} doesn't have link access")

@bot.command()
async def allow_image(ctx, user: discord.User = None):
    """Owner: Whitelist user to send images"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if user is None:
        await ctx.send("❌ Please mention a user: `/allow_image @username`")
        return

    if str(user.id) not in bot.settings["allowed_images"]:
        bot.settings["allowed_images"].append(str(user.id))
        save_settings(bot.settings)
        embed = discord.Embed(
            title="🖼️ Image Access Granted",
            description=f"{user.mention} can now send images",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ {user.mention} already has image access")

@bot.command()
async def remove_image(ctx, user: discord.User = None):
    """Owner: Remove image whitelist from user"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if user is None:
        await ctx.send("❌ Please mention a user: `/remove_image @username`")
        return

    if str(user.id) in bot.settings["allowed_images"]:
        bot.settings["allowed_images"].remove(str(user.id))
        save_settings(bot.settings)
        embed = discord.Embed(
            title="❌ Image Access Removed",
            description=f"{user.mention} can no longer send images",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ {user.mention} doesn't have image access")

@bot.command()
async def add_bad_word(ctx, *, word: str = None):
    """Owner: Add word to bad word filter"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if word is None:
        await ctx.send("❌ Please provide a word: `/add_bad_word badword`")
        return

    word = word.lower().strip()
    if word not in bot.settings["bad_words"]:
        bot.settings["bad_words"].append(word)
        save_settings(bot.settings)
        embed = discord.Embed(
            title="⚠️ Bad Word Added",
            description=f"'{word}' added to filter (1 minute timeout)",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ '{word}' already in filter")

@bot.command()
async def remove_bad_word(ctx, *, word: str = None):
    """Owner: Remove word from bad word filter"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    if word is None:
        await ctx.send("❌ Please provide a word: `/remove_bad_word badword`")
        return

    word = word.lower().strip()
    if word in bot.settings["bad_words"]:
        bot.settings["bad_words"].remove(word)
        save_settings(bot.settings)
        embed = discord.Embed(
            title="✅ Bad Word Removed",
            description=f"'{word}' removed from filter",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ '{word}' not in filter")

@bot.command()
async def list_bad_words(ctx):
    """Owner: List all bad words"""
    if not is_owner(ctx):
        await ctx.send("❌ Owner only command!")
        return

    words = "\n".join([f"• {w}" for w in bot.settings["bad_words"]])
    embed = discord.Embed(
        title="⚠️ Bad Word Filter",
        description=words if words else "No bad words added",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

@bot.command()
async def server_links(ctx):
    """Show server links"""
    embed = discord.Embed(
        title="🎮 HemantGamer SMP Links",
        description="Join our community!",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="HemantGamer SMP",
        value=f"[Join Here]({SERVER_LINKS['hemantgamer']})",
        inline=False
    )
    embed.add_field(
        name="Community Discord",
        value=f"[Join Here]({SERVER_LINKS['community']})",
        inline=False
    )
    embed.set_footer(text="🎮 Powered by HemantGamer")
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    """Show bot info"""
    embed = discord.Embed(
        title="🎮 HemantGamer SMP Bot",
        description="Complete moderation and music bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="🚫 Anti-Link", value="1 minute timeout for links", inline=False)
    embed.add_field(name="🖼️ Image Control", value="Only owner can send images", inline=False)
    embed.add_field(name="⚠️ Bad Word Filter", value="1 minute timeout + message delete", inline=False)
    embed.add_field(name="🎵 Music Player", value="/play, /join_music_bot, /move_music_bot", inline=False)
    embed.set_footer(text="🎮 Powered by HemantGamer")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    """Show all commands"""
    embed = discord.Embed(
        title="📋 Bot Commands",
        description="HemantGamer SMP Bot Help",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="🔐 Owner Commands",
        value="`/allow_link @user` - Allow user to send links\n"
              "`/remove_link @user` - Remove link access\n"
              "`/allow_image @user` - Allow user to send images\n"
              "`/remove_image @user` - Remove image access\n"
              "`/add_bad_word word` - Add word to filter\n"
              "`/remove_bad_word word` - Remove word from filter\n"
              "`/list_bad_words` - List all bad words",
        inline=False
    )
    embed.add_field(
        name="🎵 Music Commands",
        value="`/play song` - Play music from YouTube\n"
              "`/join_music_bot channel` - Bot joins voice channel (owner)\n"
              "`/move_music_bot channel` - Move bot to channel (owner)\n"
              "`/stop` - Stop music",
        inline=False
    )
    embed.add_field(
        name="ℹ️ Info Commands",
        value="`/server_links` - Show server links\n"
              "`/info` - Show bot info\n"
              "`/help` - Show this message",
        inline=False
    )
    embed.set_footer(text="🎮 Powered by HemantGamer")
    await ctx.send(embed=embed)

def run():
    """Start the bot"""
    bot.run(BOT_TOKEN)
