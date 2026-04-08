"""
Music Player Cog for HemantGamer SMP Bot
YouTube Music Support
"""

import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from datetime import timedelta
from config import OWNER_ID

# Setup youtube-dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
    'quiet': False,
    'no_warnings': False,
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('webpage_url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            data = data['entries'][0]
        audio_url = data['url']
        return cls(discord.FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"), data=data)

class Music(commands.Cog):
    """Music player commands"""

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}

    def is_owner(self, ctx):
        """Check if user is bot owner"""
        return ctx.author.id == OWNER_ID

    async def cog_load(self):
        print("✅ Music Cog Loaded")

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Play music from YouTube"""
        guild_id = ctx.guild.id

        # Check if user is in voice channel
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Not in Voice",
                description="Join a voice channel to play music",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        voice_channel = ctx.author.voice.channel

        # Connect to voice if not connected
        if not ctx.voice_client:
            try:
                await voice_channel.connect()
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Connection Error",
                    description=f"Could not join voice channel: {str(e)}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        else:
            # Move bot if in different channel
            if ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)

        # Loading message
        loading = await ctx.send("🔍 Searching for song...")

        try:
            # Search and get audio
            loop = self.bot.loop
            source = await YTDLSource.from_url(query, loop=loop)

            # Play audio
            ctx.voice_client.play(
                source,
                after=lambda e: print(f'Player error: {e}') if e else None
            )

            # Now playing embed
            embed = discord.Embed(
                title="▶️ Now Playing",
                description=f"[{source.title}]({source.url})",
                color=discord.Color.purple()
            )
            embed.set_footer(text="🎵 Music Player")
            await loading.delete()
            await ctx.send(embed=embed)

            self.now_playing[guild_id] = source.title

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Could not play song: {str(e)}",
                color=discord.Color.red()
            )
            await loading.delete()
            await ctx.send(embed=embed)

    @commands.command()
    async def join_music_bot(self, ctx, *, channel: discord.VoiceChannel = None):
        """Owner: Connect bot to voice channel"""
        if not self.is_owner(ctx):
            await ctx.send("❌ Owner only command!")
            return

        if channel is None:
            if not ctx.author.voice:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Join a voice channel or specify one",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            channel = ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.disconnect()

        try:
            await channel.connect()
            embed = discord.Embed(
                title="✅ Connected",
                description=f"Bot joined {channel.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Could not connect: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def move_music_bot(self, ctx, *, channel: discord.VoiceChannel = None):
        """Owner: Move bot to different voice channel"""
        if not self.is_owner(ctx):
            await ctx.send("❌ Owner only command!")
            return

        if channel is None:
            if not ctx.author.voice:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Join a voice channel or specify one",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            channel = ctx.author.voice.channel

        if ctx.voice_client:
            try:
                await ctx.voice_client.move_to(channel)
                embed = discord.Embed(
                    title="✅ Moved",
                    description=f"Bot moved to {channel.mention}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Could not move: {str(e)}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="Bot is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        """Stop music playback"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            embed = discord.Embed(
                title="⏹️ Stopped",
                description="Music playback stopped",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not Playing",
                description="No music is playing",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        """Pause music playback"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(
                title="⏸️ Paused",
                description="Music paused",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not Playing",
                description="No music is playing",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx):
        """Resume music playback"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(
                title="▶️ Resumed",
                description="Music resumed",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not Paused",
                description="No music is paused",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnect bot from voice"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            embed = discord.Embed(
                title="👋 Disconnected",
                description="Bot disconnected from voice",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="Bot is not in a voice channel",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    """Load music cog"""
    await bot.add_cog(Music(bot))
