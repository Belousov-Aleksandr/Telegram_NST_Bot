#!/bin/sh
kill -9 $(pidof node)
kill -9 $(pidof python3)
/bin/sleep 5
cd /home/belousov/bot_current
/usr/bin/lt --port 5000 --subdomain miptdlsbot &> /var/log/localtunnel &
/usr/bin/python3 bot.py &> /var/log/telegrambot &