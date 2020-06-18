import json

with open('ka.json') as f:
  data = json.load(f)

linkArray = []
for obj in data: 
	if len(obj['note_extract']) > 0:
		for parents in obj['note_extract']:
			link = {}
			link["source"] = parents
			link["target"] = obj['p_num']
			linkArray.append(link)
		
	if len(obj['contracted_from']) > 0:
		for parents in obj['contracted_from'].split(','):
			link = {}
			link["source"] = parents
			link["target"] = obj['p_num']
			linkArray.append(link)

nodesSet = set()

nodesArray = []
for link in linkArray:
	nodesSet.add(link['source'])
	nodesSet.add(link['target'])
	
for node in nodesSet:
	nodeObj = {}
	nodeObj["id"] = node
	nodesArray.append(nodeObj)

masterObj = {}
masterObj['nodes'] = nodesArray
masterObj['links'] = linkArray

print(masterObj)
