#!/bin/sh
cd /usr/local/tgbots/musictheatrebot &&
git pull &&
systemctl restart musictheatrebot &&
chmod +x update.sh