#!/bin/sh
/usr/bin/lt --port 5000 --subdomain miptdlsbot &>/var/log/localtunnel &
cd /home/belousov/bot_current
/usr/bin/python3 bot.py &>/var/log/telegrambot &

