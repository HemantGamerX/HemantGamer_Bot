# 🎮 HemantGamer SMP Discord Bot

A complete Discord bot for the HemantGamer SMP community with advanced moderation features and music player.

## ✨ Features

### 🚫 Anti-Link System
- Automatic 1-minute timeout for users sending links
- `/allow_link @username` - Whitelist users to send links
- Owner always allowed (ID: 1372939423297179790)

### 🖼️ Image Restrictions
- Only owner can send images by default
- `/allow_image @username` - Whitelist users to send images
- Auto-delete non-owner images

### ⚠️ Bad Word Filter
- `/add_bad_word badword` - Add words to filter (owner only)
- Automatic 1-minute timeout for violations
- Messages automatically deleted

### 🎵 Music Player
- `/play "song name"` - Play from YouTube
- `/join_music_bot channel` - Connect to voice (owner only)
- `/move_music_bot channel` - Move between channels (owner only)
- `/stop` - Stop playback
- `/pause` - Pause music
- `/resume` - Resume music

### 📢 Community Links
- `/server_links` - Show HemantGamer SMP and Community Discord links
- Always display "Powered by HemantGamer"

## 🔗 Community Links
- **HemantGamer SMP**: https://discord.gg/kmnE8CNw2G
- **Community Discord**: https://discord.gg/4dyQB3yZJq

## 📋 Requirements

- Python 3.8+
- Discord.py 2.3+
- yt-dlp for YouTube support
- FFmpeg (for audio)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   cd HemantGamer_coding
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Bot Token**
   - Get token from [Discord Developer Portal](https://discord.com/developers/applications)
   - Add to `config.py`:
     ```python
     BOT_TOKEN = "your_token_here"
     ```

3. **Run Bot**
   ```bash
   python main.py
   ```

## 📖 Full Documentation

See [QUICKSTART.md](QUICKSTART.md) and [COMMANDS.md](COMMANDS.md) for detailed setup and command information.

## 🎯 Owner Commands

All owner commands are restricted to user ID: `1372939423297179790`

- `/allow_link @user` - Whitelist for links
- `/remove_link @user` - Revoke link access
- `/allow_image @user` - Whitelist for images
- `/remove_image @user` - Revoke image access
- `/add_bad_word word` - Add to bad word filter
- `/remove_bad_word word` - Remove from filter
- `/list_bad_words` - Show all bad words

## 📁 Project Structure

```
HemantGamer_coding/
├── main.py                 # Bot entry point
├── bot.py                 # Core bot logic
├── config.py              # Configuration
├── cogs/
│   ├── __init__.py
│   └── music.py          # Music player
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore
└── README.md             # This file
```

## 🔧 Configuration

Edit `config.py` to customize:
- `BOT_TOKEN` - Discord bot token
- `OWNER_ID` - Owner's Discord ID
- `TIMEOUT_DURATION` - Timeout length in seconds
- `SERVER_LINKS` - Community server links

## 💾 Data Storage

- `bot_settings.json` - Stores whitelist and bad words

## 🛠️ Technical Details

- **Framework**: discord.py
- **Audio**: FFmpeg + yt-dlp
- **Storage**: JSON file persistence
- **Timeouts**: Discord timeouts (mutes)

## ❓ Support

For issues or features, check the setup requirements and ensure:
- Bot token is valid
- Bot has required intents enabled
- Bot has permission to timeout members
- FFmpeg is installed (for music)

## 📜 License

Created for HemantGamer SMP Community

🎮 **Powered by HemantGamer**
