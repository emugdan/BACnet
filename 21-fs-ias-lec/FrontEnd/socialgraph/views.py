import json
import os
from pathlib import Path
import pdb;

from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView

from .importer import create_profiles
from .models import Profile, FollowRecommendations
from .utils.jsonUtils import extract_connections, getRoot

# Create your views here.

path = Path('socialgraph/static/socialgraph/')
path2 = path / 'testData.json'
path = path / 'loadedData.json'
# path = path / 'loadedData1.json'
data_file = open(path)
data = json.load(data_file)
data_file.close()



def home(request):
    data_file = open(path)
    data = json.load(data_file)
    data_file.close()
    root = getRoot(data['nodes'])

    context = {
        'connections': extract_connections(data, "1 1"),
        'root': root
    }

    return render(request, 'socialgraph/home.html', context)

def users(request):

    data_file = open(path)
    data = json.load(data_file)
    data_file.close()
    root = getRoot(data['nodes'])

    if request.method == "POST":
        response = request.POST['text']
        j = extract_connections(data, response)
        return HttpResponse(j)

    context = {
        'data': json.dumps(data),
        'root': root,
        'nodes': sorted(data['nodes'], key=lambda item: item["hopLayer"]),
        'links': data['links']
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
    data_file = open(path)
    data = json.load(data_file)



    #Create Initial follow recommendation
    recommendationList = FollowRecommendations.createRecommendationList(jsonData= data)

    #Add the recommendationList to the context which will be passed to the render function
    context = {
        'data': json.dumps(data),
        'nodes': data['nodes'],
        'links': data['links'],
        'recommendations': recommendationList
    }

    #In case we have received an Ajax call from the UI-Layer:
    if request.method == "POST":
        #This response is the name of the User that was searched
        response = request.POST['text']

        #Gender Query
        if (response == 'male' or response =='female'):
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data,attribute = response, criteria='gender')
        #User has searched for name
        elif (response.startswith("nq")):
            name = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=name,
                                                                            criteria='name')
        # User has searched for name
        elif (response.startswith("tq")):
            town = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=town,
                                                                             criteria='town')
        elif (response.startswith("lq")):
            layer = int(response[2])
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=layer,
                                                                             criteria='hopLayer')
        #User wants to follow another user
        elif (response.startswith("fo")):
            # #Get the id
            # id = int(response[2:len(response)])
            #
            # #Open the jsonFile
            # with open(path, "r") as jsonFile:
            #     temp = json.load(jsonFile)
            #
            # #Overwrite the hoplayer
            # for x in temp['nodes']:
            #     if x.get('id') == id:
            #         x['hopLayer'] = 1
            # #Save new json file
            # with open(path, "w") as jsonFile:
            #     json.dump(temp, jsonFile)
            # data_file = open(path)
            # data = json.load(data_file)
            # #Create new recommendations
            queryList = FollowRecommendations.createRecommendationList(jsonData=data, maxLayer=hoplayer)

        else:
            queryList = recommendationList

        #Create a new context variable
        text = {
            'data': json.dumps(data),
            'nodes': data['nodes'],
            'links': data['links'],
            'recommendations': queryList
        }


        #Rerender the HTML file
        return render(request, 'socialgraph/FollowBody.html', text)

    return render(request, 'socialgraph/Follow.html', context)

def followBody(request):
    return render(request, 'socialgraph/FollowBody.html')

class PostDetailView(DetailView):
    model = Profile

def update_profile(request):

    context = None
    for node in data['nodes']:
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
            if fn in request.POST and (node.get(fn) is not None and node.get(fn) != request.POST[fn] or node.get(fn) is None and request.POST[fn] != ''):
                update[fn] = request.POST[fn]
        if 'gender' in update.keys() and update['gender'] == 'other' and request.POST['other'] != '':
            update['gender'] = request.POST['other']


        if len(request.FILES)>0:
            for f in request.FILES.keys():
                profile_pic_path = handle_uploaded_file(request.FILES[f], node.get('BACnetID'))
                update['profile_pic']= profile_pic_path
        #print(update)

        #TODO trigger function call to backend with update-info.

        return HttpResponseRedirect("/profile/" + str(node.get('id')))


    return render(request, 'socialgraph/profile_update.html', context)

def handle_uploaded_file(f, id):
    path = os.path.join('media', 'profile_pics', id + '.' + f.content_type[f.content_type.index('/')+1:])
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

    print(data)