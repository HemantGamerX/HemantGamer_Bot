# 📋 Command Reference

## 🔐 Owner-Only Commands

All these commands can only be used by the bot owner (ID: 1372939423297179790)

### Link Management
- `/allow_link @username` - Allow user to send links (bypasses 1m timeout)
- `/remove_link @username` - Remove link access

**Example:**
```
/allow_link @HemantGamer
```

### Image Management
- `/allow_image @username` - Allow user to send images
- `/remove_image @username` - Remove image access

**Example:**
```
/allow_image @Trusted_User
```

### Bad Word Filter
- `/add_bad_word badword` - Add word to filter (1m timeout + message delete)
- `/remove_bad_word badword` - Remove word from filter
- `/list_bad_words` - Show all current bad words

**Examples:**
```
/add_bad_word spam
/add_bad_word badword
/list_bad_words
```

## 🎵 Music Commands

### Play Music
- `/play "song name"` - Search and play from YouTube
- `/play "artist name - song name"` - More specific search

**Examples:**
```
/play "Never Gonna Give You Up"
/play "Rick Astley - Never Gonna Give You Up"
/play "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Voice Control (Owner Only)

- `/join_music_bot channel_name` - Bot joins voice channel
- `/move_music_bot channel_name` - Move bot to another channel
- `/stop` - Stop music playback
- `/pause` - Pause current music
- `/resume` - Resume paused music
- `/disconnect` - Bot leaves voice

**Examples:**
```
/join_music_bot Music
/move_music_bot Gaming
/stop
```

## ℹ️ Information Commands

### General Info
- `/help` - Show all commands
- `/info` - Show bot features
- `/server_links` - Show HemantGamer links

## 🚫 Auto-Moderation (Automatic)

### Anti-Link
- **Trigger**: Sending Discord invite links
- **Action**: 1 minute timeout + message delete
- **Exception**: Users in whitelist or owner

### Image Restriction
- **Trigger**: Sending images (non-owners)
- **Action**: Message auto-deleted + warning
- **Exception**: Users in whitelist or owner

### Bad Word Filter
- **Trigger**: Using filtered words
- **Action**: 1 minute timeout + message delete
- **Exception**: Owner (always allowed)

## 📝 Command Syntax

### Understanding placeholders:
- `@username` or `@user` - Mention a user
- `"text"` - Put text in quotes if multiple words
- `channel_name` - Voice channel name

### Examples:
```
❌ /allow_link HemantGamer          (Wrong - need mention)
✅ /allow_link @HemantGamer         (Correct)

❌ /play Never Gonna Give You Up    (May not work)
✅ /play "Never Gonna Give You Up"  (Better)

❌ /join_music_bot                  (Need channel)
✅ /join_music_bot Music            (Correct)
```

## 🎯 Common Use Cases

### Setup Links
```
/allow_link @Moderation_Team
/allow_link @Helpers
```

### Add Multiple Bad Words
```
/add_bad_word spam
/add_bad_word inappropriate
/add_bad_word badword
/list_bad_words
```

### Music Session
```
/join_music_bot Music
/play "gaming music - epic"
/pause
/resume
/move_music_bot Main_Hall
```

### Trust Users for Images
```
/allow_image @Content_Creator
/allow_image @Streamer
```

## ⚙️ Settings

All settings are automatically saved in `bot_settings.json`:
- Whitelisted link users
- Whitelisted image users
- Bad word list
- Muted users (temporary)

Settings persist across bot restarts!

## 🔄 Best Practices

1. **Links**: Only whitelist trusted users or moderators
2. **Images**: Restrict to content creators only
3. **Bad Words**: Add commonly misused terms, not necessarily curse words
4. **Music**: Keep volume reasonable to not disrupt server
5. **Timeouts**: 1 minute is default, allows users to cool down

## ❓ Need Help?

- See `/help` in your Discord server
- Check [README.md](README.md) for overview
- See [QUICKSTART.md](QUICKSTART.md) for setup

🎮 **Powered by HemantGamer**
