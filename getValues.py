import gspread
import json
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
		stateText += boi + '\nInfected : {}'.format(stateGlobalData[boi]["infected"]) + '\nDead : {}\n'.format(stateGlobalData[boi]["dead"])
	return stateText

def districtData():
	districtText = ''
	for districtBoi in globalData:
		districtText += districtBoi + '\nInfected : {}'.format(globalData[districtBoi]["infected"]) + '\nDead : {}\n'.format(globalData[districtBoi]["dead"])
	districtText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return districtText