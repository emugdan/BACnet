import json
from pathlib import Path
import pdb;

from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView

from .importer import create_profiles, create_Recommendations
from .models import Profile, FollowRecommendations
from .utils.jsonUtils import extract_connections, getRoot

# Create your views here.

path = Path('socialgraph/static/socialgraph/')
#path = path / 'testData.json'
path = path / 'loadedData.json'
data_file = open(path)
data = json.load(data_file)
data_file.close()
root = getRoot(data['nodes'])


def home(request):

    context = {
        'connections': extract_connections(data, "1 1"),
        'root': root
    }

    return render(request, 'socialgraph/home.html', context)

def users(request):

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

def feed(request):
    return render(request, 'socialgraph/Feed.html', {'title': 'Feed'})

def about(request):
    return render(request, 'socialgraph/about.html', {'title': 'About'})


"""
This function creates and renders Follow recommendations based on the hoplayer.
Per default I chose hoplayer 3 as there are more users within this layer as of now.
Also, the function follow is able to handle ajax calls from the UI Layer in order
to rerender the FollowRecommendation HTML files.
"""
def follow(request):

    #Create Initial follow recommendation
    recommendationList = FollowRecommendations.createRecommendationList(jsonData= data, maxLayer=3)

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
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data,attribute = response, criteria='gender', maxlayer=3)
        #User has searched for name
        elif (response.startswith("nq")):
            name = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=name,
                                                                            criteria='name', maxlayer=3)
        # User has searched for name
        elif (response.startswith("tq")):
            town = response[2:len(response)]
            queryList = FollowRecommendations.createRecommendationsFromQuery(jsonData=data, attribute=town,
                                                                             criteria='town', maxlayer=3)

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
