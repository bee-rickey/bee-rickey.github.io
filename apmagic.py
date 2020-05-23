from bs4 import BeautifulSoup
import requests
import json
import re
import datetime

def getAPDelta():
	nameMapping = {"Kadapa": "Y.S.R. Kadapa", "Nellore": "S.P.S. Nellore"}
	stateDashboard = requests.request("post", "http://covid19.ap.gov.in/Covid19_Admin/api/CV/DashboardCountAPI").json()
	covidDashboard = requests.request("get", "https://api.covid19india.org/state_district_wise.json").json()


	districtDelta = {} 
	districtDeltaArray = []
	apData = covidDashboard['Andhra Pradesh']['districtData']

	for cases in (stateDashboard['cases_district']):
		districtName = nameMapping[cases['district_name']] if cases['district_name'] in nameMapping else cases['district_name']
		if districtName not in districtDelta:
			districtDelta[districtName] = {} 

		outputString = districtName + "," + str(int(cases['cases']) - apData[districtName]['confirmed']) +","+ str(int(cases['recovered']) - apData[districtName]['recovered']) + "," + str(int(cases['death']) - apData[districtName]['deceased']) 

		print(outputString)



getAPDelta()
