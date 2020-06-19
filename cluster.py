import json
import pandas as pd

def fetch_KA_data(writeJson=False):
    '''
    Returns KA data as pd.DataFrame, fetched from Vikram sir's sheet.
    Switch `writeJson` to save to file.
    '''

    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRp1Wz_VBpM54n04JzYdTGGrrvghLVf-6BjPAw9Ahwzr2uGPsoLlDTKNvhtLLUsW2oSZ_jxRQGRs2xC/pubhtml?gid=1042945172&single=true'
    l = pd.read_html(url, encoding='utf8')
    cd = l[0].copy()
    cd.columns = cd.iloc[0]
    cd = cd[1:]

    cd.rename(columns={'Date Announced':"date",
              'State Patient Number':'p_num',
              'Age Bracket':'age',
              'Gender':'gender',
              'Detected District':'district',
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
	
nodeLinkCount = {}
patientIdMap = {}
linkArray = []
ignoredNodeList = set()

def readSheetJson():
	with open('ka_sheet.json') as f:
		data = json.load(f)

	for obj in data: 
		'''
		if len(obj['note_extract']) > 0:
			for parents in obj['note_extract']:
				link = {}
				link["source"] = parents
				link["target"] = obj['p_num']
				linkArray.append(link)
		'''
		if obj['p_num'] is None:
			continue
		patientIdMap[obj['p_num'].strip()] = obj
			
		if obj['contracted_from'] != None:
			for parents in obj['contracted_from'].split(','):
				link = {}
				try:
					nodeLinkCount[parents.strip().replace('.', '')] += 1 
				except KeyError:
					nodeLinkCount[parents.strip().replace('.', '')] = 1 

				try:
					nodeLinkCount[obj['p_num'].strip().replace('.', '')] += 1 
				except KeyError:
					nodeLinkCount[obj['p_num'].strip().replace('.', '')] = 1 

				link["source"] = parents.strip().replace('.', '')
				link["target"] = obj['p_num'].strip().replace('.', '')
				linkArray.append(link)

def buildIgnoreList():
	global ignoredNodeList
	queue = []
	masterExplored = set()

	for key, value in nodeLinkCount.items():
		if key in masterExplored:
			continue
		else:
			masterExplored.add(key)

			explored = set()
			explored.add(key)
			queue.append(key)

			while len(queue) != 0:
				visitingNode = queue.pop(0);
				neighbouringNodes = []
				for link in linkArray:
					if link['source'] == visitingNode:
						neighbouringNodes.append(link['target'])
					if link['target'] == visitingNode:
						neighbouringNodes.append(link['source'])

				for node in neighbouringNodes:
					if node in explored:
						continue
					else:
						explored.add(node)
						masterExplored.add(node)
						queue.append(node)
			if len(explored) < 5:
				ignoredNodeList = ignoredNodeList.union(explored) if len(ignoredNodeList) > 0 else explored

def buildFinalList():
	global ignoredNodeList
	nodesSet = set()
	nodesArray = []
	finalLinkArray = []
	for link in linkArray:
		if link['source'] in ignoredNodeList or link['target'] in ignoredNodeList:
			continue
		else:
			finalLinkArray.append(link)
		nodesSet.add(link['source'])
		nodesSet.add(link['target'])
		
	for node in nodesSet:
		nodeObj = {}
		
		node = node.strip().replace('.', '')
		nodeObj["id"] = node
		try:
			nodeObj["a"] = patientIdMap[node]['age']
			nodeObj["s"] = patientIdMap[node]['gender']
			nodeObj["l"] = patientIdMap[node]['district']
		except KeyError:
			nodeObj["a"] = "N/A"
			nodeObj["s"] = "N/A"
			nodeObj["l"] = "N/A"
		nodesArray.append(nodeObj)

	masterObj = {}
	masterObj['nodes'] = nodesArray
	masterObj['links'] = finalLinkArray
	print(masterObj)

fetch_KA_data(True)
readSheetJson()
buildIgnoreList()
buildFinalList()

