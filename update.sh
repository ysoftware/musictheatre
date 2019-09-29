#!/bin/sh
systemctl stop musictheatrebot &&
cd /usr/local/tgbots/musictheatrebot &&
git pull &&
systemctl start musictheatrebot