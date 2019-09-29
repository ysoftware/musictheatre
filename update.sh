#!/bin/sh
ls &&
cd /usr/local/tgbots/musictheatrebot &&
systemctl stop musictheatrebot &&
git pull &&
systemctl start musictheatrebot