#!/usr/bin/env python
import os
import time
from slackclient import SlackClient

# connects to slack, prints the raw stream messages

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
sc = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if sc.rtm_connect() :
    while True:
        print sc.rtm_read()
        time.sleep(1)
else:
    print "Connection Failed"
