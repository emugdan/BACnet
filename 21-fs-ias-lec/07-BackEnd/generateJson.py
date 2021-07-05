import json
import sys

import os
from pathlib import Path


def generate_json(person_list, we_are):  # Assumption that we have a follow list of each person in the given list
    links = []
    nodes = []
    nodeIDs = {}

    for i in range(0, len(person_list)):
        person = person_list[i]
        curBACnetID = person.id  # .decode("utf-8")
        nodeIDs[curBACnetID] = i

    ourID = 0
    for i in range(0, len(person_list)):
        person = person_list[i]
        if person == we_are:
            ourID = i
        node = {}
        followList = person.get_follow_list()
        if sys.platform.startswith("linux"):  # compatibility for all operating systems
            node['BACnetID'] = person.id
        else:
            node['BACnetID'] = person.id.decode("utf-8")
        node['id'] = nodeIDs[person.id]  # .decode("utf-8")]
        node['name'] = person.name
        node['gender'] = person.gender
        node['birthday'] = person.birthday
        node['country'] = person.country
        node['town'] = person.town
        node['language'] = person.language
        node['status'] = person.status
        node['status_list'] = person.status_list
        node['activity level'] = person.get_activity()
        node['influencer'] = person.influencer
        node['hopLayer'] = 10000
        node['profile_pic'] = person.profile_pic
        nodes.append(node)
        for friend in followList:
            link = {'source': node['id'],
                    'target': nodeIDs[friend]}  # .decode("utf-8")]}
            links.append(link)

        # TODO: In the future refreshes Profilepics.
        #if person.profile_pic is not None:
        #    person.feed.load_profile_pic(person.profile_pic)

    calculate_hops(ourID, links, nodes)

    data = {'nodes': nodes, 'links': links}

    path = Path('socialgraph/static/socialgraph/')
    path = path / 'loadedData.json'
    # for testing: path = path / 'loadedData1.json'

    # Change working directory to Frontend
    backEnd = os.getcwd()
    #If we called the callToBackEnd function from the Frontend:
    if (backEnd.endswith("21-fs-ias-lec")):
        os.chdir("07-BackEnd")
        backEnd = os.getcwd()
    frontEnd = backEnd.replace("07-BackEnd", "FrontEnd")
    os.chdir(frontEnd)

    # Write file
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    # Change back the working directory
    os.chdir(backEnd)

    return json.dumps(data)


def calculate_hops(root_id, links, nodes):  # Calculates the hop layer of each node iteratively
    nodes[root_id]['hopLayer'] = 0
    distances = []
    for node in nodes:
        distances.append(10000)

    oldDistances = distances.copy()
    distances[root_id] = 0
    while distances != oldDistances:
        oldDistances = distances.copy()
        for link in links:
            if distances[link['source']] + 1 < distances[link['target']]:
                distances[link['target']] = distances[link['source']] + 1

    for node in nodes:
        node['hopLayer'] = distances[node['id']]