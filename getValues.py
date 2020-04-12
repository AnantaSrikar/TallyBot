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
totalData = {} # has all the data
totalSumDead = 0
totalSumInfected = 0
rowCount = False
rowNum = 1
def reloadData():
	global rowCount
	global rowNum
	global totalSumDead
	global totalSumInfected
	global totalData
	rowCount = False
	rowNum = 1
	totalSumDead = 0
	totalSumInfected = 0
	totalData = {}
	for row in sheet.get():   #sheet.get the whole document as a list of lists

		if not rowCount:
			rowCount = not rowCount
			continue
		try:
			districtBoi = row[3]
			stateBoi = row[2]
		except Exception as e:
			print('Exception at {}, error : {}'.format(rowNum, e))

		if stateBoi in totalData:
			if districtBoi in totalData[stateBoi]:
				try:
					totalData[stateBoi][districtBoi]["infected"] += int(row[4])
				except:
					pass

				try:
					totalData[stateBoi][districtBoi]["dead"] += int(row[5])
				except:
					pass
			
			else:
				totalData[stateBoi][districtBoi] = {}
				try:
					totalData[stateBoi][districtBoi]["infected"] = int(row[4])
				except:
					totalData[stateBoi][districtBoi]["infected"] = 0

				try:
					totalData[stateBoi][districtBoi]["dead"] = int(row[5])
				except:
					totalData[stateBoi][districtBoi]["dead"] = 0
		
		else:
			totalData[stateBoi] = {}
			totalData[stateBoi][districtBoi] = {}
			try:
				totalData[stateBoi][districtBoi]["infected"] = int(row[4])
			except:
				totalData[stateBoi][districtBoi]["infected"] = 0

			try:
				totalData[stateBoi][districtBoi]["dead"] = int(row[5])
			except:
				totalData[stateBoi][districtBoi]["dead"] = 0		
		rowNum += 1

	for boi in totalData:
		for distBoi in totalData[boi]:
			totalSumInfected += totalData[boi][distBoi]["infected"]
			totalSumDead += totalData[boi][distBoi]["dead"]

def stateData():
	reloadData()
	stateText = ''
	for stateBoi in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for districtBoi in totalData[stateBoi]:
			infectedStateSum += totalData[stateBoi][districtBoi]["infected"]
			deadStateSum += totalData[stateBoi][districtBoi]["dead"]
		stateText += stateBoi +'\nInfected : {}'.format(infectedStateSum) + '\nDead : {}\n\n'.format(deadStateSum)
	return stateText

def districtData():
	reloadData()
	districtText = ''
	for stateBoi in totalData:
		districtText += '{} :\n'.format(stateBoi)
		for distBoi in totalData[stateBoi]:
			districtText += distBoi + ':\nInfected : {}'.format(totalData[stateBoi][distBoi]["infected"]) + '\nDead : {}\n\n'.format(totalData[stateBoi][distBoi]["dead"])
	return districtText


def apiDistrictData():
	reloadData()
	districtAPIdata = requests.get(getTokens()["district_api_url"]).json()
	apiDataText = ''
	for districtBoi in districtAPIdata:
		apiDataText += districtBoi + '\nInfected : {}'.format(districtAPIdata[districtBoi]['infected']) + '\nDead : {}\n\n'.format(districtAPIdata[districtBoi]['dead'])
	apiDataText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return apiDataText

def findState(stateName):
	reloadData()
	stateText = ''
	if stateName in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for districtBoi in totalData[stateName]:
			infectedStateSum += totalData[stateName][districtBoi]["infected"]
			deadStateSum += totalData[stateName][districtBoi]["dead"]
		stateText = 'Values for {}:\n'.format(stateName) + 'Infected : {}\nDead : {}'.format(infectedStateSum, deadStateSum)
		return stateText
	return('{} not found, check spelling and try again'.format(stateName))

def findDistrict(districtName):
	reloadData()
	districtText = ''
	for stateBoi in totalData:
		if districtName in totalData[stateBoi]:
			districtText = 'Values for {}:\n'.format(districtName) + ':\nInfected : {}'.format(totalData[stateBoi][districtName]["infected"]) + '\nDead : {}'.format(totalData[stateBoi][districtName]["dead"])
			return districtText
	return('{} not found, check spelling and try again'.format(districtName))

def stateDists(stateName):
	reloadData()
	stateDistrictsText = 'Districts with numbers in {}:\n'.format(stateName)
	if stateName in totalData:
		for districtBoi in totalData[stateName]:
			stateDistrictsText += districtBoi +':\nInfected : {}\nDead : {}\n\n'.format(totalData[stateName][districtBoi]["infected"], totalData[stateName][districtBoi]["dead"])
		return stateDistrictsText
	return "Found nothing for {}".format(stateName)

def distNAstate(stateName):
	reloadData()
	text = 'DIST_NAs in {} :\n'.format(stateName)
	if(stateName in totalData):
		if("DIST_NA" in totalData[stateName]):
			text += 'Infected : {}\nDeath : {}'.format(totalData[stateName]['DIST_NA']["infected"], totalData[stateName]['DIST_NA']["dead"])
		return text
	return "Good news! No DIST_NA for {}".format(stateName)