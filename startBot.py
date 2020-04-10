from slack import RTMClient
import time
import json

def getTokens():
	allTokens = json.load(open('res/TOKENS.json', 'r'))
	return allTokens

@RTMClient.run_on(event="hello")
def bot_init(**payload):
	print('The bot has started to run\n')
	
@RTMClient.run_on(event="message")
def say_hello(**payload):
	data = payload['data']
	web_client = payload['web_client']

	message = ''
	channel_id = ''
	user = ''
	try:
		message = data['text']
		channel_id = data['channel']
		user = data['user']
	except:
		pass
	if(message.startswith('Hi') and user != ''):
		web_client.chat_postMessage(channel = channel_id, text=f"Hi <@{user}>!")
	elif(message.startswith('!')):
		web_client.chat_postMessage(channel = channel_id, text=f"You have entered a command! Awesome!")

rtm_client = RTMClient(token=getTokens()["slack_bot_token"])
rtm_client.start()