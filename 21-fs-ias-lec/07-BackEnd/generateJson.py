import json


# Assumption that we have a follow list of each person in the given list.
import os
from pathlib import Path

def generateJson(personList):
    links = []
    nodes = []
    nodeIDs = {}

    # make ids
    for person in personList:
        followList = person.getFollowList()
        curBACnetID = person.id.decode("utf-8")
        curNodeID = makeNumeric(curBACnetID)
        nodeIDs[curBACnetID] = curNodeID
        for BACnetID, friend in followList.items():
            curBACnetID = BACnetID.decode("utf-8")
            curNodeID = makeNumeric(curBACnetID)
            nodeIDs[curBACnetID] = curNodeID

    for person in personList:
        node = {}
        followList = person.getFollowList()
        node['BACnetID'] = person.id.decode("utf-8")
        node['id'] = nodeIDs[node['BACnetID']]
        node['name'] = node['BACnetID']  # TODO: this is just for testing
        node['gender'] = None
        node['birthday'] = None
        node['country'] = None
        node['town'] = None
        node['language'] = None
        node['status'] = None
        nodes.append(node)
        for friend in followList:
            link = {'source': node['id'],
                    'target': nodeIDs[friend.decode("utf-8")]}
            links.append(link)
    data = {'nodes':nodes, 'links': links}

    path = Path('socialgraph/static/socialgraph/')
    path = path / 'loadedData.json'

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


def makeNumeric(BACnetID):
    chars = list(BACnetID)
    for i in range(0, len(chars)):
        if chars[i].isalpha():
            chars[i] = str(ord(chars[i]))
    return int("".join(chars))

