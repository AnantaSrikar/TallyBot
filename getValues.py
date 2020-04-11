import gspread
import json
import requests
from oauth2client.service_account import ServiceAccountCredentials

def getTokens():
	allTokens = json.load(open('res/TOKENS.json', 'r'))
	return allTokens

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(getTokens()["sheet_url"]).worksheet('Sheet1')

# DON'T EDIT ANYTHING ABOVE THIS!!
globalData = {} # dictionary that will have all the district wise dictionary
stateGlobalData = {} # dictionary that will have all the state wise dictionary
totalSumDead = 0
totalSumInfected = 0
rowCount = False
rowNum = 1
for row in sheet.get():   #sheet.get the whole document as a dictionary of dictionaries	
	if not rowCount:
		rowCount = not rowCount
		continue
	try:
		districtBoi = row[3]
		stateBoi = row[2]
	except Exception as e:
		print('Exception at {}, error : {}'.format(rowNum, e))

	if districtBoi in globalData:
		try:
			globalData[districtBoi]["infected"] += int(row[4])
		except:
			pass

		try:
			globalData[districtBoi]["dead"] += int(row[5])
		except:
			pass
	else:
		globalData[districtBoi] = {}
		try:
			globalData[districtBoi]["infected"] = int(row[4])
		except:
			globalData[districtBoi]["infected"] = 0

		try:
			globalData[districtBoi]["dead"] = int(row[5])
		except:
			globalData[districtBoi]["dead"] = 0

	if stateBoi in stateGlobalData:
		try:
			stateGlobalData[stateBoi]["infected"] += int(row[4])
		except:
			pass

		try:
			stateGlobalData[stateBoi]["dead"] += int(row[5])
		except:
			pass
	else:
		stateGlobalData[stateBoi] = {}
		try:
			stateGlobalData[stateBoi]["infected"] = int(row[4])
			
		except:
			stateGlobalData[stateBoi]["infected"] = 0

		try:
			stateGlobalData[stateBoi]["dead"] = int(row[5])
		except:
			stateGlobalData[stateBoi]["dead"] = 0
	
	rowNum += 1

for boi in stateGlobalData:
	totalSumInfected += stateGlobalData[boi]["infected"]
	totalSumDead += stateGlobalData[boi]["dead"]

def stateData():
	stateText = ''
	for boi in stateGlobalData:
		stateText += boi + '\nInfected : {}'.format(stateGlobalData[boi]["infected"]) + '\nDead : {}\n\n'.format(stateGlobalData[boi]["dead"])
	stateText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return stateText

def districtData():
	districtText = ''
	for districtBoi in globalData:
		districtText += districtBoi + '\nInfected : {}'.format(globalData[districtBoi]["infected"]) + '\nDead : {}\n\n'.format(globalData[districtBoi]["dead"])
	districtText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return districtText


def apiDistrictData():
	districtAPIdata = requests.get(getTokens()["district_api_url"]).json()
	apiDataText = ''
	for districtBoi in districtAPIdata:
		apiDataText += districtBoi + '\nInfected : {}'.format(districtAPIdata[districtBoi]['infected']) + '\nDead : {}\n\n'.format(districtAPIdata[districtBoi]['dead'])
	apiDataText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return apiDataText

def findState(stateName):
	stateText = ''
	if(stateName in stateGlobalData):
		stateText = 'Values for {}:\n'.format(stateName) + 'Infected : {}\nDead : {}'.format(stateGlobalData[stateName]["infected"], stateGlobalData[stateName]["dead"])
	else:
		stateText = '{} not found, check spelling and try again'.format(stateName)
	return stateText

def findDistrict(districtName):
	districtText = ''
	if(districtName in globalData):
		districtText = 'Values for {}:\n'.format(districtName) + 'Infected : {}\nDead : {}'.format(globalData[districtName]["infected"], globalData[districtName]["dead"])
	else:
		districtText = '{} not found, check spelling and try again'.format(districtName)
	return districtText

def stateDists(stateName):
	found = False
	stateDistrictsText = 'Districts with numbers in {}:\n'.format(stateName)
	districtAPIdata = requests.get(getTokens()["district_api_url"]).json()
	print(districtAPIdata)
	for districtBoi in districtAPIdata:
		if(stateName == districtAPIdata[districtBoi]["state"]):
			stateDistrictsText += districtBoi +':\nInfected : {}\nDead : {}\n\n'.format(districtAPIdata[districtBoi]["infected"], districtAPIdata[districtBoi]["dead"])
			if(not found):
				found = not found
	if(found):
		return stateDistrictsText
	
	return "Found nothing for {}".format(stateName)