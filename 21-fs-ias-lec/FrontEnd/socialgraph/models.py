from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Profile(models.Model):
    bacnet_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=6, blank=True, null=True, default=None)
    birthday = models.DateField(blank=True, null=True, default=None)
    country = models.CharField(max_length=64, blank=True, null=True, default=None)
    town = models.CharField(max_length=64, blank=True, null=True, default=None)
    language = models.CharField(max_length=256, blank=True, null=True, default=None) #https://stackoverflow.com/questions/22340258/django-list-field-in-model
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    myself = models.BooleanField(default=False)
    node_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f'{self.name} Profile / {self.bacnet_id}'

    def get_details(self):
        details = {}
        if self.gender is not None:
            details['Gender']= self.gender
        if self.birthday is not None:
            details['Birthday']= self.birthday
        if self.country is not None:
            details['Country']= self.country
        if self.town is not None:
            details['Town']= self.town
        if self.language is not None:
            details['Language']= self.language
        return details

class FollowRecommendations(models.Model):
    layer = models.IntegerField(default=None)
    bacnet_id = models.CharField(max_length=64, primary_key=True)
    id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=6, blank=True, null=True, default=None)
    birthday = models.DateField(blank=True, null=True, default=None)
    country = models.CharField(max_length=64, blank=True, null=True, default=None)
    town = models.CharField(max_length=64, blank=True, null=True, default=None)
    language = models.CharField(max_length=256, blank=True, null=True,
                                default=None)  # https://stackoverflow.com/questions/22340258/django-list-field-in-model
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    @classmethod
    def create(cls, layerNode, bacnet_idNode, id, nameNode,
               genderNode, birthdayNode, countryNode,
               townNode, languageNode, profile_picNode):
        recommendation = cls(layer = layerNode, bacnet_id = bacnet_idNode, id = id, name = nameNode,
                    gender = genderNode, birthday = birthdayNode, country = countryNode,
                    town = townNode, language = languageNode, profile_pic = profile_picNode)
        return recommendation


    def __str__(self):
        return f'{self.name} Profile / {self.bacnet_id}'

    def get_details(self):
        details = {}
        if (self.layer < 3):
            details['layer'] = self.layer
            if self.gender is not None:
                details['Gender'] = self.gender
            if self.birthday is not None:
                details['Birthday'] = self.birthday
            if self.country is not None:
                details['Country'] = self.country
            if self.town is not None:
                details['Town'] = self.town
            if self.language is not None:
                details['Language'] = self.language
        return details

    @classmethod
    def createRecommendationList(self, jsonData):
        recommendationList = []
        for node in jsonData['nodes']:
            hoplayer = node.get('hopLayer')
            if (hoplayer >1):
                recommendationList.append(
                    FollowRecommendations.create(layerNode=node.get('hopLayer'), bacnet_idNode=node.get('BACnetID'), id = node.get("id"),
                                                 nameNode=node.get('name'), genderNode=node.get('gender'),
                                                 birthdayNode=node.get('birthday'), countryNode=node.get('country'),
                                                 townNode=node.get('town'),
                                                 languageNode=node.get('language'),
                                                 profile_picNode=node.get('profile_pic') if node.get(
                                                     'profile_pic') is not None else 'default.jpg'))
        return recommendationList

    @classmethod
    def createRecommendationsFromQuery(self, jsonData, attribute, criteria):
        recommendationList = []
        for node in jsonData['nodes']:
            if (node.get(criteria) == attribute and node.get('hopLayer') > 1):
                recommendationList.append(
                    FollowRecommendations.create(layerNode=node.get('hopLayer'), bacnet_idNode=node.get('BACnetID'), id = node.get("id"),
                                                 nameNode=node.get('name'), genderNode=node.get('gender'),
                                                 birthdayNode=node.get('birthday'), countryNode=node.get('country'),
                                                 townNode=node.get('town'),
                                                 languageNode=node.get('language'),
                                                 profile_picNode=node.get('profile_pic') if node.get(
                                                     'profile_pic') is not None else 'default.jpg'))
        return recommendationList

    @classmethod
    def createRecommendationsHopLayer(self, jsonData, criteria):
        recommendationList = []
        for node in jsonData['nodes']:
            if (node.get('hopLayer') == criteria):
                recommendationList.append(
                    FollowRecommendations.create(layerNode=node.get('hopLayer'), bacnet_idNode=node.get('BACnetID'), id = node.get("id"),
                                                 nameNode=node.get('name'), genderNode=node.get('gender'),
                                                 birthdayNode=node.get('birthday'), countryNode=node.get('country'),
                                                 townNode=node.get('town'),
                                                 languageNode=node.get('language'),
                                                 profile_picNode=node.get('profile_pic') if node.get(
                                                     'profile_pic') is not None else 'default.jpg'))
        return recommendationList

    @classmethod
    def createRecommendationsRemove(self, jsonData, criteria):
        recommendationList = []
        for node in jsonData['nodes']:
            if not (node.get('BACnetID') == criteria):
                recommendationList.append(
                    FollowRecommendations.create(layerNode=node.get('hopLayer'), bacnet_idNode=node.get('BACnetID'), id = node.get("id"),
                                                 nameNode=node.get('name'), genderNode=node.get('gender'),
                                                 birthdayNode=node.get('birthday'), countryNode=node.get('country'),
                                                 townNode=node.get('town'),
                                                 languageNode=node.get('language'),
                                                 profile_picNode=node.get('profile_pic') if node.get(
                                                     'profile_pic') is not None else 'default.jpg'))
        return recommendationList



