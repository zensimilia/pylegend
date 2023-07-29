FROM python:3.10-alpine
RUN adduser -D bot
RUN apk add -U -q --no-cache libffi-dev libsodium-dev opus-dev ffmpeg
WORKDIR /home/bot/pylegend
ADD requirements.txt .
RUN pip install -U pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir
ADD --chown=bot:bot --chmod=660 . .
USER bot
CMD [ "python", "main.py" ]
