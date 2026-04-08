# 🚀 Quick Start Guide

## Step 1: Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Discord bot token

## Step 2: Set Up Python Environment

### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Get Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "HemantGamer SMP Bot"
4. Go to "Bot" → "Add Bot"
5. Under the bot name, click "Copy" under TOKEN
6. Copy the token

## Step 4: Enable Intents

In Discord Developer Portal:
1. Go to your bot application
2. Click "Bot"
3. Scroll down to "Privileged Gateway Intents"
4. Enable:
   - MESSAGE CONTENT INTENT
   - GUILD MEMBERS INTENT
5. Click "Save Changes"

## Step 5: Configure Bot Token

Edit `config.py`:
```python
BOT_TOKEN = "paste_your_token_here"
OWNER_ID = 1372939423297179790  # HemantGamer's ID
```

## Step 6: Install FFmpeg

### Windows:
```powershell
# Using scoop (if installed)
scoop install ffmpeg

# Or use chocolatey
choco install ffmpeg
```

### Linux:
```bash
sudo apt-get install ffmpeg
```

### Mac:
```bash
brew install ffmpeg
```

## Step 7: Run the Bot

```bash
python main.py
```

You should see:
```
🎮 Starting HemantGamer SMP Bot...
📋 Loading cogs...
✅ Loaded cog: music.py
🚀 Connecting to Discord...
✅ Bot logged in as HemantGamer_Bot#0000
🎮 Powered by HemantGamer SMP
```

## Step 8: Invite Bot to Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot
3. Go to "OAuth2" → "URL Generator"
4. Select scopes: `bot`
5. Select permissions:
   - Send Messages
   - Embed Links
   - Manage Messages
   - Moderate Members (for timeouts)
   - Connect (voice)
   - Speak (voice)
6. Copy URL and open in browser to add bot

## Test Commands

Once the bot is in your server, try:
- `/info` - Show bot info
- `/help` - Show all commands
- `/server_links` - Show community links

## Troubleshooting

**Bot doesn't respond:**
- Check if bot is online in Discord
- Verify token in config.py
- Check bot permissions in server

**Links not timing out:**
- Verify MEMBER INTENTS are enabled
- Check bot's role hierarchy (above users)
- Ensure bot has "Manage Members" permission

**Music not working:**
- Check FFmpeg is installed
- Run `ffmpeg -version` to verify
- Ensure bot can connect to voice channels

**Settings not saving:**
- Check write permissions in folder
- Verify `bot_settings.json` exists

## Next Steps

- See [COMMANDS.md](COMMANDS.md) for command details
- Check [README.md](README.md) for feature overview
- Customize settings in `config.py`

🎮 **Powered by HemantGamer**
