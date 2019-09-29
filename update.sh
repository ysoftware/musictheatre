#!/bin/sh
systemctl stop musictheatrebot &&
cd /usr/local/tgbots/musictheatrebot &&
ls &&
git pull &&
systemctl start musictheatrebot