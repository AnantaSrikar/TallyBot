from slack import RTMClient
import time
import json
import getValues

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

	if(message.startswith('!')):
		if(message.startswith('!start')):
			web_client.chat_postMessage(channel = channel_id, text="Hi <@{}>! I'm still awake!".format(user))

		elif(message.startswith('!districtData')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the district-wise tally :\n{}".format(getValues.districtData()))

		elif(message.startswith('!stateData')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the state-wise tally :\n{}".format(getValues.stateData()))

		elif(message.startswith('!apiData')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the API data :\n{}".format(getValues.apiDistrictData()))

		elif(message.startswith('!findState')):
			stateName = message[11:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.findState(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")

		elif(message.startswith('!findDist')):
			districtName = message[10:]
			if(len(districtName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.findDistrict(districtName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the District")
		
		elif(message.startswith('!stateDists')):
			stateName = message[12:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.stateDists(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")

		elif(message.startswith('!distNAstate')):
			stateName = message[13:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.distNAstate(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")
			
		elif(message.startswith('!help')):
			fileManager = open('res/bot_intro.txt', 'r')
			bot_intro = fileManager.read()
			fileManager.close()
			web_client.chat_postMessage(channel = channel_id, text=bot_intro)

		else:
			web_client.chat_postMessage(channel = channel_id, text="IDK that command, try !help")
	
	elif('boomer' in message.lower()):
		web_client.chat_postMessage(channel = channel_id, text="Wait till I get coded for this :angry:")
			
rtm_client = RTMClient(token=getTokens()["slack_bot_token"])
rtm_client.start()

# TODO : today's total count