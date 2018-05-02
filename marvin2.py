#!/usr/bin/env python
import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                # return text
                return output['text'], output['channel']
    return "", ""


def parse_message(message, channel):
    for word in message.split():
        if word.startswith('ESNET-TASK') or word.startswith('TASK0'):
            url_string="https://esnet.service-now.com/nav_to.do?uri=task.do?sysparm_query=number=%s" % word
            response="Got a link for you %s" % url_string 
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)            
        if word.startswith('ESNET-CHG') or word.startswith('CHG'):
            url_string="https://esnet.service-now.com/nav_to.do?uri=change_request.do?sysparm_query=number=%s" % word
            response="Got a link for you %s" % url_string 
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)            
        if word.startswith('ESNET-RITM') or word.startswith('RITM'):
            url_string="https://esnet.service-now.com/nav_to.do?uri=sc_req_item.do?sysparm_query=number=%s" % word
            response="Got a link for you %s" % url_string 
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)            
        if word.startswith('ESNET-REQ') or word.startswith('REQ'):
            url_string="https://esnet.service-now.com/nav_to.do?uri=sc_request.do?sysparm_query=number=%s" % word
            response="Got a link for you %s" % url_string 
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)            

def parse_dm(message, channel):
    response = "Oh God, I'm so depressed. Life. Don't talk to me about life."
    if "brak" in message:
        response = "ALL HAIL BRAK!"
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)            
            

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Brain the size of a planet connected")
        while True:
            message, channel = parse_slack_output(slack_client.rtm_read())
            if message is not "":
                parse_message(message, channel)
                if message.startswith(AT_BOT):
                    parse_dm(message.split(AT_BOT)[1].strip().lower(), channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

