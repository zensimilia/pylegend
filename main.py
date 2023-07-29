import logging
import os

import discord

DEBUG = os.environ.get('DEBUG', False)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')
AUDIO_URL = os.environ.get('AUDIO_URL')
VOICE_CHANNEL = os.environ.get('VOICE_CHANNEL')
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=1"',
    'bitrate': 192,
}

discord.utils.setup_logging(
    level=logging.DEBUG if bool(DEBUG) else logging.INFO
)
log = logging.getLogger('bot')


class BotClient(discord.Client):
    admin_user: discord.User | None = None
    voice_channel: discord.VoiceChannel | None = None
    voice_client: discord.VoiceClient | None = None

    async def on_ready(self) -> None:
        message = f'Logged in as {self.user.name} <{self.user.id}>'
        log.warning(message)

        activity = discord.Game('DJ')
        await self.change_presence(
            activity=activity, status=discord.Status.online
        )

        self.admin_user = await self.fetch_user(ADMIN_ID)
        await self.dm_to_admin(message, silent=True)

        self.voice_channel = await self.fetch_channel(VOICE_CHANNEL)

    async def on_error(self, event_method: str, *args, **_kwargs) -> None:
        log.error('%s: %s', event_method, args)
        await self.dm_to_admin(f'{event_method}: {args}')

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        if member.id == self.user.id:
            return

        if not after.channel or after.channel.id != self.voice_channel.id:
            log.info('Member %s <%d> left', member.name, member.id)

        client_in_voice_channel = self.voice_clients or False
        if after.channel and after.channel.id == self.voice_channel.id:
            log.info('Member %s <%d> joined', member.name, member.id)
            await self.join_voice_channel(self.voice_channel)
            self.voice_client.play(
                discord.FFmpegOpusAudio(AUDIO_URL, **FFMPEG_OPTIONS)
            )
            return
        if (
            client_in_voice_channel
            and len(client_in_voice_channel[0].channel.members) == 1
        ):
            await self.leave_voice_channel()

    async def dm_to_admin(self, message: str, **kwargs) -> discord.Message:
        return await self.admin_user.send(message, **kwargs)

    async def join_voice_channel(
        self, voice_channel: discord.VoiceChannel
    ) -> discord.VoiceClient:
        if self.voice_client and self.voice_client.is_connected():
            return
        self.voice_client = await voice_channel.connect()
        log.warning(
            'Joined to the voice channel %s <%d>',
            self.voice_client.channel.name,
            self.voice_client.channel.id,
        )
        return self.voice_client

    async def leave_voice_channel(self) -> None:
        if self.voice_client.is_playing():
            self.voice_client.stop()
        await self.voice_client.disconnect(force=True)
        self.voice_client = None
        log.warning('Left voice channel')


def main():
    if not (BOT_TOKEN and ADMIN_ID and VOICE_CHANNEL and AUDIO_URL):
        log.critical(
            'Configuration environment variables not specified! Check README.md'
        )
        return
    intents = discord.Intents.default()

    client = BotClient(intents=intents)
    client.run(BOT_TOKEN, log_handler=None)


if __name__ == '__main__':
    main()
