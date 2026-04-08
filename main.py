"""
HemantGamer SMP Discord Bot - Main Entry Point
"""

import asyncio
from bot import bot
from config import BOT_TOKEN
import os

async def load_cogs():
    """Load all cogs"""
    cogs_dir = "cogs"
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

async def main():
    """Start the bot"""
    print("🎮 Starting HemantGamer SMP Bot...")
    print("📋 Loading cogs...")
    await load_cogs()
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n❌ ERROR: Bot token not configured!")
        print("📝 Please add your bot token to config.py")
        print("📖 Instructions: https://discord.com/developers/applications")
        return
    
    print("🚀 Connecting to Discord...")
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot shutting down...")
