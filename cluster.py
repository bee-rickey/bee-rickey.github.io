import json
import pandas as pd

def fetch_KA_data(writeJson=False):
    '''
    Returns KA data as pd.DataFrame, fetched from Vikram sir's sheet.
    Switch `writeJson` to save to file.
    '''

    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRp1Wz_VBpM54n04JzYdTGGrrvghLVf-6BjPAw9Ahwzr2uGPsoLlDTKNvhtLLUsW2oSZ_jxRQGRs2xC/pubhtml?gid=1042945172&single=true'
    l = pd.read_html(url, encoding='utf8')
    cd = l[0]
    cd.columns = cd.iloc[0]
    cd = cd[1:]

    cd.rename(columns={'Date Announced':"date",
              'State Patient Number':'p_num',
              'Age Bracket':'age',
              'Gender':'gender',
              'Detected District':'distrct',
              'Current Status':'status',
              'Status Change Date':'change_date',
              'Notes':'notes',
              'Infected from': 'infection_type',
              'Inter District - Infected from':'infected_district',
              'Contact - Infected from':'contracted_from'},
             inplace=True)
    if writeJson:
        cd.to_json("ka_sheet.json",orient='records')

    return cd
	
#fetch_KA_data(True)

with open('ka_sheet.json') as f:
  data = json.load(f)

linkArray = []
nodeLinkCount = {}
for obj in data: 
	'''
	if len(obj['note_extract']) > 0:
		for parents in obj['note_extract']:
			link = {}
			link["source"] = parents
			link["target"] = obj['p_num']
			linkArray.append(link)
	'''
		
	if obj['contracted_from'] != None:
		for parents in obj['contracted_from'].split(','):
			link = {}
			try:
				nodeLinkCount[parents] += 1 
			except KeyError:
				nodeLinkCount[parents] = 1 

			try:
				nodeLinkCount[obj['p_num']] += 1 
			except KeyError:
				nodeLinkCount[obj['p_num']] = 1 
			link["source"] = parents
			link["target"] = obj['p_num']
			linkArray.append(link)

nodesSet = set()

nodesArray = []
finalLinkArray = []

for link in linkArray:
	if nodeLinkCount[link['source']] <= 1 and nodeLinkCount[link['target']] <= 1:
		continue
	else:
		finalLinkArray.append(link)
	nodesSet.add(link['source'])
	nodesSet.add(link['target'])
	
for node in nodesSet:
	nodeObj = {}
	nodeObj["id"] = node
	nodesArray.append(nodeObj)

masterObj = {}
masterObj['nodes'] = nodesArray
masterObj['links'] = finalLinkArray

print(masterObj)
