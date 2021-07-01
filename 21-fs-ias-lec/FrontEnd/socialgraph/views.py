import json
import os
import pathlib
from pathlib import Path
import pdb
import sys

from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView

from .importer import create_profiles
from .models import Profile, FollowRecommendations
from .utils.jsonUtils import extract_connections, getRoot, getRootFollowsSize, getRootFollowersSize, saveSettings

x = os.getcwd()
from .utils.callToBackend import followCall, unfollowCall, profileUpdateCall


os.chdir(x)

# Create your views here.

path = pathlib.Path('socialgraph/static/socialgraph/')
path2 = path / 'testData.json'
path = path / 'loadedData.json'
# path = path / 'loadedData1.json'

data_file = open(path)
data = json.load(data_file)
data_file.close()

settingsPath = Path('socialgraph/static/socialgraph/')
settingsPath = settingsPath / 'settings.json'
settings_data_file = open(settingsPath)
settings_data = json.load(settings_data_file)
settings_data_file.close()


def home(request):
    x = pathlib.Path(__file__)
    print(x.parent.parent)
    os.chdir(x.parent.parent)
    data_file = open(path)
    data = json.load(data_file)
    data_file.close()
    root = getRoot(data['nodes'])
    follows = getRootFollowsSize(data['links'], root.get("id"))
    followers = getRootFollowersSize(data['links'], root.get("id"))

    settings_data_file = open(settingsPath)
    settings_data = json.load(settings_data_file)
    settings_data_file.close()

    if request.method == "POST":
        response = request.POST['text']
        newSettings = saveSettings(settings_data, response, settingsPath)
        return HttpResponse(newSettings)

    context = {
        'connections': extract_connections(data, "1 1"),
        'root': root,
        'follows': follows,
        'followers': followers,
        'all': len(data['nodes']),
        'graph': settings_data
    }

    return render(request, 'socialgraph/home.html', context)

def users(request):
    x = pathlib.Path(__file__)
    print(x.parent.parent)
    os.chdir(x.parent.parent)
    data_file = open(path)
    data = json.load(data_file)
    data_file.close()
    root = getRoot(data['nodes'])

    settings_data_file = open(settingsPath)
    settings_data = json.load(settings_data_file)
    settings_data_file.close()

    if request.method == "POST":
        response = request.POST['text']
        j = extract_connections(data, response)
        return HttpResponse(j)

    context = {
        'data': json.dumps(data),
        'root': root,
        'nodes': sorted(data['nodes'], key=lambda item: item["hopLayer"]),
        'links': data['links'],
        'graph': settings_data
    }
    create_profiles(data)
    return render(request, 'socialgraph/users.html', context)


# def feed(request):
#     return render(request, 'socialgraph/Feed.html', {'title': 'Feed'})

# def about(request):
#     return render(request, 'socialgraph/about.html', {'title': 'About'})


"""
This function creates and renders Follow recommendations based on the hoplayer.
Per default I chose max hoplayer provided from json file.
Also, the function follow is able to handle ajax calls from the UI Layer in order
to rerender the FollowRecommendation HTML files.
"""
def follow(request):
    x = pathlib.Path(__file__)
    print(x.parent.parent)
    os.chdir(x.parent.parent)
    data_file = open(path)
    data = json.load(data_file)
    data_file.close()

    # Create Initial follow recommendation
    recommendationList = FollowRecommendations.createRecommendationList(jsonData=data)

    # Add the recommendationList to the context which will be passed to the render function
    context = {
        'data': json.dumps(data),
        'nodes': data['nodes'],
        'links': data['links'],
        'recommendations': recommendationList
    }

    # In case we have received an Ajax call from the UI-Layer:
    if request.method == "POST":
        # This response is the name of the User that was searched
        response = request.POST.get('text', False)
        mode = request.POST.get('mode', False)
        queryList = []

        # Gender Query
        if (response == 'male' or response == 'female'):
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=response,
                                                                             criteria='gender') \
            if mode == "1follow" else FollowRecommendations.createUnfollowRecommendation(jsonData=data, attribute=response,
                                                                             criteria='gender')
        # User has searched for name
        elif (response.startswith("nq")):
            name = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=name,
                                                                             criteria='name')\
            if mode == "1follow" else FollowRecommendations.createUnfollowRecommendation(jsonData=data, attribute=name,
                                                                             criteria='name')
        # User has searched for town
        elif (response.startswith("tq")):
            town = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=town,
                                                                             criteria='town')\
            if mode == "follow" else FollowRecommendations.createUnfollowRecommendation(jsonData=data, attribute=town,
                                                                                     criteria='town')
        #User has altered hoplayer slider
        elif (response.startswith("lq")):
            if(len(response) > 3):
                queryList = FollowRecommendations.createRecommendationList(jsonData=data)
            else:
                layer = int(response[2])
                queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=layer,
                                                                             criteria='hopLayer')
        # User wants to follow another user
        elif (response.startswith("fo")):
            root = getRoot(data['nodes'])
            rootUser = root.get("name")
            rootUserID = root.get("BACnetID")
            followID = str(response[2:18])
            followName = str(response[18:len(response)])
            followCall(mainPersonName=rootUser, mainPersonID=rootUserID, followPersonName=followName,
                       followPersonID=followID)
            x = pathlib.Path(__file__)
            os.chdir(x.parent.parent)
            data_file = open(path)
            data = json.load(data_file)
            data_file.close()
            queryList = FollowRecommendations.createRecommendationList(jsonData=data)

        #User wants to unfollow other user
        elif (response.startswith("uf")):
            root = getRoot(data['nodes'])
            rootUser = root.get("name")
            rootUserID = root.get("BACnetID")
            unfollowID = str(response[2:18])
            unfollowName = str(response[18:len(response)])
            print(unfollowName)
            unfollowCall(mainPersonName=rootUser, mainPersonID=rootUserID, unfollowPersonName=unfollowName,
                       unfollowPersonID=unfollowID)
            x = pathlib.Path(__file__)
            os.chdir(x.parent.parent)
            data_file = open(path)
            data = json.load(data_file)
            data_file.close()
            queryList = FollowRecommendations.createUnfollowRecommendationDefault(jsonData=data)



        #User has reset the filters
        elif(response == ""):
            queryList = FollowRecommendations.createRecommendationList(jsonData=data) \
            if mode == "1follow" else FollowRecommendations.createUnfollowRecommendationDefault(jsonData=data)



            # Create a new context variable
        text = {
            'data': json.dumps(data),
            'nodes': data['nodes'],
            'links': data['links'],
            'recommendations': queryList
        }


        if(mode == "1unfollow"):
            return render(request, 'socialgraph/UnfollowBody.html', text)
        else:
            return render(request, 'socialgraph/FollowBody.html', text)



    return render(request, 'socialgraph/Follow.html', context)


def followBody(request):
    return render(request, 'socialgraph/FollowBody.html')


class PostDetailView(DetailView):
    model = Profile


def update_profile(request):

    context = None

    x = pathlib.Path(__file__)
    print(x.parent.parent)
    os.chdir(x.parent.parent)
    fresh_data_file = open(path)
    fresh_data = json.load(fresh_data_file)
    fresh_data_file.close()
    for node in fresh_data['nodes']:
        if node.get('hopLayer') == 0:
            context = {
                'node': node,
                'profile': Profile.objects.filter(myself=True).first()
            }
            break

    if request.method == "POST":
        update = {'BACnetID': node.get('BACnetID')}
        fieldnames = ['gender', 'birthday', 'country', 'town', 'language', 'status']
        for fn in fieldnames:
            if fn in request.POST:

                if node.get(fn) is not None and node.get(fn) != request.POST[fn] or node.get(fn) is None and \
                        request.POST[fn] != '':
                    if isinstance(request.POST[fn], str):
                        value = request.POST[fn].strip()
                        update[fn] = value if value != '' else None
                    else:
                        update[fn] = request.POST[fn]
        if 'gender' in update.keys() and update['gender'] == 'other' and request.POST['other'] != '':
            update['gender'] = request.POST['other']

        if len(request.FILES) > 0:
            for f in request.FILES.keys():
                profile_pic_path = handle_uploaded_file(request.FILES[f], node.get('BACnetID'))
                update['profile_pic'] = profile_pic_path
        # print(update)

        # TODO trigger function call to backend with update-info.
        root = getRoot(data['nodes'])
        rootUser = root.get("name")
        rootUserID = root.get("BACnetID")

        profileUpdateCall(rootUser, rootUserID, update)

        x = pathlib.Path(__file__)
        print(x.parent.parent)
        os.chdir(x.parent.parent)

        fresh_data_file = open(path)
        fresh_data = json.load(fresh_data_file)
        create_profiles(fresh_data)
        fresh_data_file.close()

        # TODO trigger function call to backend with update-info.

        return HttpResponseRedirect("/profile/" + str(node.get('id')))

    return render(request, 'socialgraph/profile_update.html', context)


def handle_uploaded_file(f, id):
    path = os.path.join('media', 'profile_pics', id + '.' + f.content_type[f.content_type.index('/') + 1:])
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.flush()
        os.fsync(destination.fileno())
        destination.close()
        return path


if __name__ == "__main__":
    followCall(mainPersonName="vera", mainPersonID="9ff78df97744c0d5", followPersonName="esther",
               followPersonID="4076cc22fa40fa84")

