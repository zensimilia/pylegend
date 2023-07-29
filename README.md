# pylegend

Another Discord bot that plays streaming music, but only when member is joins a specific voice channel.

## How to use it

1. Create `.env` file in root directory of project.
2. Fill required environment variables:
   | var | description |
   |----- |------------- |
   | BOT_TOKEN | Bot token |
   | ADMIN_ID | Id of administrator member |
   | VOICE_CHANNEL | Id of desired voice channel |
   | AUDIO_URL | Audio stream address |
3. Run Docker container: `docker-compose up -d --build`

### Development

1. Make python virtual environment `python -m venv venv` and activate it `souce venv/bin/activate` (on Windows `venv\Scripts\activate.bat`)
2. Install dependencies: `pip install -r requirements`
3. Run the Bot: `python main.py`

On Linux environments requires getting the following dependencies: ffmpeg, libffi, opus.
