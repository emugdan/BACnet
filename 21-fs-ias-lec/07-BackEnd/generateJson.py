import json
import sys


import os
from pathlib import Path

# Assumption that we have a follow list of each person in the given list.
def generateJson(personList, weAre):
    links = []
    nodes = []
    nodeIDs = {}

    for i in range(0, len(personList)):
        person = personList[i]
        curBACnetID = person.id         # .decode("utf-8")]}
        nodeIDs[curBACnetID] = i

    ourID = 0
    for i in range(0, len(personList)):
        person = personList[i]
        if person == weAre:
            ourID = i
        node = {}
        followList = person.get_follow_list()
        if sys.platform.startswith("linux"):
            node['BACnetID'] = person.id
        else:
            node['BACnetID'] = person.id.decode("utf-8")
        node['id'] = nodeIDs[person.id] # .decode("utf-8")]
        node['name'] = person.name
        node['gender'] = person.gender
        node['birthday'] = person.birthday
        node['country'] = person.country
        node['town'] = person.town
        node['language'] = person.language
        node['status'] = person.status
        node['hopLayer'] = 10000
        nodes.append(node)
        for friend in followList:
            link = {'source': node['id'],
                    'target': nodeIDs[friend]} # .decode("utf-8")]}
            links.append(link)

    calculateHops(ourID, links, nodes, 0)

    data = {'nodes':nodes, 'links': links}

    path = Path('socialgraph/static/socialgraph/')
    path = path / 'loadedData.json'
    # path = path / 'loadedData1.json'

    #Change workingdirectory to Frontend
    backEnd = os.getcwd()
    frontEnd = backEnd.replace("07-BackEnd", "FrontEnd")
    os.chdir(frontEnd)

    #Write file
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    #Change back the working directory
    os.chdir(backEnd)

    return json.dumps(data)

#Calculates the Hoplayer of each node recursively
def calculateHops(curID, Links, nodes, layer):
    nodes[curID]['hopLayer'] = layer
    for link in Links:
        if link['source'] == curID:
            if nodes[link['target']]['hopLayer'] > layer+1:
                calculateHops(link['target'], Links, nodes, layer+1)



