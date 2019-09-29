#!/bin/sh
echo "1" &&
systemctl stop musictheatrebot &&
echo "2" &&
cd /usr/local/tgbots/musictheatrebot &&
ls &&
git pull &&
echo "3" &&
systemctl start musictheatrebot