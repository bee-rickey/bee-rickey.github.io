import json
from datetime import datetime, timedelta
import pandas as pd

dateDict = {}
with open("listOfFiles.meta") as listOfFiles:
  for line in listOfFiles:
    fileTS = line.split('-')[0].split('T')
    if fileTS[0] not in dateDict.keys():
      dateDict[fileTS[0]] = []
    dateDict[fileTS[0]].append(int(fileTS[1].split("Z")[0]))

firstDate = datetime.strptime("2020/03/24", '%Y/%m/%d')
dateObj = firstDate

jsonFileToConsider = {}

while dateObj.strftime("%Y%m%d") != "20200427":
  dateDict[dateObj.strftime("%Y%m%d")].sort()
  jsonFileToConsider[dateObj.strftime("%d/%m/%Y")] =  "districts_history_upto26th/" + dateObj.strftime("%Y%m%d") + "T"  + str(dateDict[dateObj.strftime("%Y%m%d")][-1]) + "Z-state_district_wise.json"
  dateObj = dateObj + timedelta(days=1)

dailyDict = {}
dfOriginal = pd.read_csv("test.csv")
#print(df[df['State'] == "Andaman and Nicobar Islands"])

'''
with open("test.csv") as dailyCount:
  for line in dailyCount:
    lineArray = line.split(',')
    if lineArray[0] not in dailyCount.keys():
      dailyDict[lineArray[0]] = {}
    if lineArray[1] not in dailyDict[lineArray[0]].keys():
      dailyDict[lineArray[0]][lineArray[1]] = {}
    if lineArray
    dailyDict[lineArray[0]][lineArray[1]]["confirmed"] = 

  '''
raw_data = {}

correctionsDict = {}
with open("corrections.txt") as corrections:
  for line in corrections:

    lineArray = line.split(',')
    if len(lineArray) != 5:
      continue
    if lineArray[1].strip() not in correctionsDict.keys():
      correctionsDict[lineArray[1].strip()] = {}
    if lineArray[2].strip() not in correctionsDict[lineArray[1].strip()].keys():
      correctionsDict[lineArray[1].strip()][lineArray[2].strip()] = {}
    if lineArray[0].strip() not in correctionsDict[lineArray[1].strip()][lineArray[2].strip()].keys():
      correctionsDict[lineArray[1].strip()][lineArray[2].strip()][lineArray[0].strip()] = {"confirmed": 0, "recovered": 0, "deceased": 0}
    if lineArray[3].strip() == "Hospitalised":
      correctionsDict[lineArray[1].strip()][lineArray[2].strip()][lineArray[0].strip()]["confirmed"] = int(lineArray[4])
    if lineArray[3].strip() == "Recovered":
      correctionsDict[lineArray[1].strip()][lineArray[2].strip()][lineArray[0].strip()]["recovered"] = int(lineArray[4])
    if lineArray[3].strip() == "Deceased":
      correctionsDict[lineArray[1].strip()][lineArray[2].strip()][lineArray[0].strip()]["deceased"] = int(lineArray[4])
print(correctionsDict)

with open("tmp/csv/compare_gospel_v1v2.csv") as gospel:
  for line in gospel:
    if line.startswith("#"):
      continue
    lineArray = line.split(",")
    if float(lineArray[12]) != 0.0 or float(lineArray[13]) != 0.0 or float(lineArray[14]) != 0.0:
      
      print("PROCESSING ------------> {}, {}, {}, {}, {}".format(lineArray[2], lineArray[4], lineArray[12], lineArray[13], lineArray[14]))
      #print(df[(df['State'] == lineArray[2]) & (df['District'] == lineArray[4])])
      #print(df)

      dateObj = firstDate
      while dateObj.strftime("%Y%m%d") != "20200427":
        #print("---------------------{}--------------------".format(dateObj.strftime("%d/%m/%Y")))
        df = dfOriginal[(dfOriginal['State'] == lineArray[2]) & (dfOriginal['District'] == lineArray[4]) & (dfOriginal['Date'] == dateObj.strftime("%Y-%m-%d"))]

        #print(df)
        #df.style.hide_index()
        previousDay = dateObj + timedelta(days=-1)
        if not df.empty:
          confirmedUpdated = False
          recoveredUpdated = False
          deceasedUpdated = False
          
          for index, row in df.iterrows():
            #print("---> {}, {}, {}, {}".format(row['State'], row['District'], row['Status'], row['Count'], row['Date']))
            if lineArray[2] not in raw_data.keys():
              raw_data[lineArray[2]] = {}
            if lineArray[4] not in raw_data[lineArray[2]].keys():
              raw_data[lineArray[2]][lineArray[4]] = {}
            if dateObj.strftime("%d/%m/%Y") not in raw_data[lineArray[2]][lineArray[4]].keys():
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")] = {"confirmed": 0, "recovered": 0, "deceased": 0}

            if dateObj <= firstDate:
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] = 0
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] = 0
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] = 0 
            if previousDay <= firstDate:
              raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")] = {"confirmed": 0, "recovered": 0, "deceased": 0}
              

            if row['Status'] == "confirmed":
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] 
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] = row['Count'] + raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["confirmed"]
              confirmedUpdated = True 
            if row['Status'] == "recovered":
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] = row['Count'] + raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["recovered"]
              recoveredUpdated = True 
            if row['Status'] == "deceased":
              raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] = row['Count'] + raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["deceased"]
              deceasedUpdated = True 

          if confirmedUpdated == False:
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["confirmed"]

          if recoveredUpdated == False:
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["recovered"]

          if deceasedUpdated == False:
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["deceased"]

        else:
          if lineArray[2] not in raw_data.keys():
            raw_data[lineArray[2]] = {}
          if lineArray[4] not in raw_data[lineArray[2]].keys():
            raw_data[lineArray[2]][lineArray[4]] = {}
             

          raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")] = {"confirmed": 0, "recovered": 0, "deceased": 0}
          if dateObj <= firstDate:
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] = 0
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] = 0
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] = 0 
          else:
          #print(raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")])

            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["confirmed"] 
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["recovered"]
            raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] = raw_data[lineArray[2]][lineArray[4]][previousDay.strftime("%d/%m/%Y")]["deceased"]
        
        try:
          raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"] += correctionsDict[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"]
        except:
          pass

        try:
          raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] += correctionsDict[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"]
        except:
          pass

        try:
          raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"] += correctionsDict[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"]
        except:
          pass

        try:

          
          rawC = raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["confirmed"]
          
          rawR = raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["recovered"] 
        
          rawD = raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]["deceased"]
          

          f = open(jsonFileToConsider[dateObj.strftime("%d/%m/%Y")])
          data = json.load(f)
          confirmed = 0
          recovered = 0
          deceased = 0

          stateSheetObj = {}
    
          districtName = lineArray[4]
          if "Y.S.R" in lineArray[4]:
            districtName = "Y.S.R."

          if "Ahmedabad" in lineArray[4]:
            districtName = "Ahmadabad"

          if "Budgaum" in lineArray[4]:
            districtName = "Badgam"

          if "Bandipora" in lineArray[4]:
            districtName = "Bandipore"

            

          try:
            confirmed = data[lineArray[2]]["districtData"][districtName]["confirmed"]
          except KeyError:
            confirmed = 0
          try:
            recovered = data[lineArray[2]]["districtData"][districtName]["recovered"]
          except KeyError:
            recovered = 0
          try:
            deceased = data[lineArray[2]]["districtData"][districtName]["deceased"]
          except KeyError:
            deceased = 0

          if rawC != confirmed or rawR != recovered or rawD != deceased:
            print("---RAW: {}, {}, {}, {}".format(dateObj.strftime("%d/%m/%Y"), lineArray[2], lineArray[4], raw_data[lineArray[2]][lineArray[4]][dateObj.strftime("%d/%m/%Y")]))
            print("---AGG: {}, {}, {}, {}, {}, {}".format(dateObj.strftime("%d/%m/%Y"), lineArray[2], lineArray[4], confirmed, recovered, deceased))


          stateSheetObj["confirmed"] = confirmed
          stateSheetObj["recovered"] = recovered
          stateSheetObj["deceased"] = deceased


        except KeyError:
          #print("IGNORING ----> {}".format(jsonFileToConsider[dateObj.strftime("%d/%m/%Y")]))
          dateObj = dateObj + timedelta(days=1)
          continue
        dateObj = dateObj + timedelta(days=1)
      print("RAW DATA {}, {}, {}".format(lineArray[10], lineArray[11], lineArray[9]))
