from bs4 import BeautifulSoup
import requests
import json
import re
import datetime

#url = "https://dashboard.kerala.gov.in/index.php"
#response = requests.request("GET", url)
#cookie=(response.headers['Set-Cookie']).split(';')[0]
#
#url = "https://dashboard.kerala.gov.in/testing-view-public.php"
#
#payload = {}
#headers = {
#  'Host': 'www.dashboard.kerala.gov.in',
#  'Connection': 'keep-alive',
#  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#  'Accept-Encoding': 'gzip, deflate, br',
#  'Accept-Language': 'en-US,en;q=0.5',
#  'Referer': 'https://dashboard.kerala.gov.in/index.php',
#  'Cookie': cookie
#}
#
#response = requests.request("GET", url, headers=headers, data = payload)
#soup = BeautifulSoup(response.content, 'html5lib')
#table = soup.find("table")
#rows=table.find_all("tr")
#
#for row in rows:
#	data = row.find_all("td")
#	if len(data) > 0 :
#		print(data[0].get_text() + "," + data[1].get_text() + "," + data[2].get_text())
#
#url = "http://hmfw.ap.gov.in/covid_dashboard.aspx"
#response = requests.request("GET", url)
#soup = BeautifulSoup(response.content, 'html5lib')
#samplesTested = soup.find("span", id="lblSamples")
#samplesNegative = soup.find("span", id="lblNegative")
#
#print("AP: Samples tested: " + samplesTested.get_text())
#print("AP: Samples negative: " + samplesNegative.get_text())
#
#
#url = "http://www.rajswasthya.nic.in"
#response = requests.request("GET", url)
#soup = BeautifulSoup(response.content, 'html5lib')
#rows=soup.find("blockquote").find("tbody").find_all("tr")
#
#for row in rows:                                                                               
#	data = row.find_all("font")
#	if len(data) > 0:
#		print(re.sub(' +', ' ', data[1].get_text()) + "," + re.sub(' +', ' ', data[2].get_text()))


#masterUrl="http://chdcovid19.in/"
#response = requests.request("GET", masterUrl)
#soup = BeautifulSoup(response.content, 'html5lib')
#table = soup.find_all("div", {"class":"card stats bg-danger text-white text-center"})
#print(table)
#print(soup.prettify())
        

metaArray = []
class ExtractMeta:  
	def __init__(self, url, stateName, district):
		if district == "":
			self.districtRequired = False
		else:
			self.districtRequired = True
		self.url = url
		self.stateName = stateName

with open("extract.meta", "r") as metaFile:
	for line in metaFile:
		lineArray = line.strip().split(',') 
		metaObject = ExtractMeta(lineArray[0].strip(), lineArray[1].strip(), lineArray[2].strip())
		metaArray.append(metaObject)


def getDataForStates():
	outputToWrite=[]
	for metaObject in metaArray:
		if metaObject.districtRequired == True:
			outputToWrite.append(districtDetailsExtractor(metaObject))
		else:
			outputToWrite.append(stateDetailsExtractor(metaObject))

def writeToOutputCsv(fileName, dataToWrite):
	testingNumbersFile = open(fileName, "w")
	testingNumbersFile.writelines(dataToWrite)
	testingNumbersFile.close()


def stateDetailsExtractor(metaObject):
	outputString=""
	url = metaObject.url
	response = requests.request("GET", url)
	soup = BeautifulSoup(response.content, 'html5lib')
    
#if metaObject.stateName == "Andhra Pradesh":
#		samplesTested = soup.find("span", id = "lblSamples").get_text()
#		samplesNegative = soup.find("span", id = "lblNegative").get_text()
#		lastUpdated = datetime.datetime.strptime(soup.find("span", id = "lblLast_Update").get_text(), "%d-%m-%Y %I:%M:%S %p")
#		outputString = "Andhra Pradesh, " + lastUpdated.strftime("%d/%m/%Y") + ", " + samplesTested + ", " + samplesNegative
#		return outputString
#	
#if metaObject.stateName == "Arunachal Pradesh":
#		row = soup.find("tbody").find("tr")
#		for index, data in enumerate(row.find_all("td")):
#			if index == 0:
#				lastUpdated = datetime.datetime.strptime(data.get_text().split(' ')[0], "%d-%b-%Y")
#			if index == 1:
#				samplesTested = data.get_text()
#			if index == 2:
#				samplesNegative = data.get_text()
#				
#		outputString = "Arunachal Pradesh, " + lastUpdated.strftime("%d/%m/%Y") + ", " + samplesTested + ", " + samplesNegative
#		print(outputString)

	
def nagalandTableExtractor(soupObject, districtDictionary, firstPass):
	for index, row in enumerate(soupObject):
		if index == 0:
			dataElements = row.find_all("th")
		else:
			dataElements = row.find_all("td")

		rowString=""
		currentDistrict = ""
		for data in dataElements:
			if len(rowString) == 0:
				currentDistrict = data.get_text() 
			rowString = data.get_text() if len(rowString) == 0 else rowString + "," + data.get_text()

		rowString = rowString.replace('-', '/')
		if firstPass == False:
			rowString = rowString + "\n"
		districtDictionary[currentDistrict] = rowString if firstPass == True else districtDictionary[currentDistrict] + "," + rowString 
		
def readAllEntriesForATable(table, outputString, itemToSearch, itemsToAppend, itemsToRemove):
	for index, row in enumerate(table):
		data = row.find_all(itemToSearch) 

		if len(itemsToRemove) != 0:
			for sub in data('font'):
				sub.decompose()

		rowString = ""
		for value in data:
			rowString = str(value.get_text()).strip() if len(rowString) == 0 else rowString + "," + str(value.getText()).strip()
			rowString = re.sub('\n', '', rowString)
			rowString = re.sub(' +', ' ', rowString)

		if len(rowString) > 0:
			rowString = rowString + "," + str(itemsToAppend) + "\n" if len(itemsToAppend) > 0 else rowString + "\n"
			outputString.append(rowString)
	


def districtDetailsExtractor(metaObject):
	outputString = []
	url = metaObject.url

	response = requests.request("GET", url)
	soup = BeautifulSoup(response.content, 'html5lib')

	if metaObject.stateName == "Nagaland":
		table = soup.find("table").find_all("tr")
		districtDictionary = {}
		nagalandTableExtractor(table, districtDictionary, True)

		soup = BeautifulSoup(open("x.html"), 'html5lib')
		table = soup.find("div", {"class":"modal-body"}).find("table").find_all("tr")
		nagalandTableExtractor(table, districtDictionary, False)

		outputString.append(districtDictionary['District'])
		for k, v in districtDictionary.items():
			if str(k) != 'District':
				outputString.append(str(v))

		writeToOutputCsv("nagalandDistrict.csv", outputString)
	
	if metaObject.stateName == 'Odisha':
		url = "https://statedashboard.odisha.gov.in/ajax/heatMapHospital?type=Current"
		response = requests.request("GET", url)
		outputString.append("DistrictName,NoOfHospitals,NoOfBeds,NoOfICU\n")
		for data in response.json():
			dataString = data['vchDistrctName'] + "," + str(data['intNoOfHospital']) + "," + str(data['intNoOfBed']) + "," + str(data['intNoOfICU']) + "\n"
			outputString.append(dataString)
		writeToOutputCsv("OdishaDistrictBeds.csv", outputString)

	
	if metaObject.stateName == 'Puducherry':
		div = soup.find_all("div", {"class": "col-md-6"})
		date = div[1].find("h5").get_text().replace('-', '/')
		table = div[1].find("table").find_all("tr")

		readAllEntriesForATable(table, outputString, "th", date, '')
		readAllEntriesForATable(table, outputString, "td", date, '')

		writeToOutputCsv("Puducherry.csv", outputString)
	
	
	if metaObject.stateName == "Gujarat":
		div = soup.find("div", {"class": "card-body p-1"})
		date = soup.find("span", id="ctl00_body_lblDate").get_text()
		table = div.find("table").find_all("tr")
            
		tempOutputString = []
		readAllEntriesForATable(table, tempOutputString, "th", 'Last Updated', '')
        

		table = div.find("table").find_all("tr")
		readAllEntriesForATable(table, tempOutputString, "span", date, '')

		districtNames = []

		for row in table:
			data = row.find("td")
			if data is not None:
				districtNames.append(data.get_text().strip())

		for index, value in enumerate(tempOutputString):
			if index == 0:
				outputString.append(value)
			else:
				districtString = districtNames[index - 1] + "," + value
				outputString.append(districtString)
			
		writeToOutputCsv("GujaratDistrict.csv", outputString)
	
	if metaObject.stateName == 'Andhra Pradesh':
		response = requests.request("POST", url).json()
		districtDictionary = {}

		districtDictionary['District'] = "Cases,Active,Recovered,Death,Total Samples,Total Positive,Total Negative,Total Inprogress, Total, Beds, Hall, Rooms"
		for cases in (response['cases_district']):
			districtDictionary[cases['district_name']] = cases['cases'] +","+ cases['active'] +","+ cases['recovered'] +","+ cases['death'] 

		for cases in (response['samples_district']):
			districtDictionary[cases['district_name']] = districtDictionary[cases['district_name']] + "," + cases['total'] +","+ cases['positive'] +","+ cases['negitive'] +","+ cases['inprogress'] 

		for cases in (response['infra_district']):
			districtDictionary[cases['district_name']] = districtDictionary[cases['district_name']] + "," + cases['total'] +","+ cases['beds'] +","+ cases['hall'] +","+ cases['rooms'] 

			
		for k, v in districtDictionary.items():
			outputString.append(str(k) + "," + str(v) + "\n")

		writeToOutputCsv("APDistrict.csv", outputString)

	if metaObject.stateName == 'Rajasthan':
		table = soup.find('blockquote').find('table').find_all('tr')

		tempOutputString = []
		readAllEntriesForATable(table, tempOutputString, "font", '', '')


		for index, row in enumerate(tempOutputString):
			if 'Discharged' in row:
				row = "SR. No, District - Country,Total Sample Received,Todays Positive,Cumulative Positive,Recovered,Discharged\n"
			if 'Other District' in row:
				row = "," + row
			if 'Total,' in row:
				rowValue = row.split(',')
				rowString = "";
				for headerIndex, data in enumerate(rowValue):
					if headerIndex%2 == 0:
						rowString = rowString + "," + data
				row = rowString + "\n"
			if 'Grand Total' in row:
				row = "," + row
			if 'BSF' in row:
				row = ",," + row
			if 'Evacuees' in row:
				row = ",,"
			if 'Italy' in row:
				row = ",,"

			outputString.append(row)

		writeToOutputCsv("Rajasthan.csv", outputString)

		
getDataForStates()




