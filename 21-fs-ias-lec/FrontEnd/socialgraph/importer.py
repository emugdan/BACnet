# Creates Profile Entries in the Database for each Node.
# TODO: Move somewhere else
import os
import json
from datetime import datetime
import datetime as dt


import pytz
import tzlocal as tzlocal


from socialgraph.models import Profile, FollowRecommendations, Status


def create_profiles(data):
    Profile.objects.all().delete()  # Delete all profile entries in the database.
    Status.objects.all().delete()  # Delete all status entries in the database.
    for node in data['nodes']:
        p = Profile(bacnet_id=node.get('BACnetID'), name=node.get('name'), gender=node.get('gender'),
                    birthday=node.get('birthday'), country=node.get('country'), town=node.get('town'),
                    language=node.get('language'),
                    profile_pic=node.get('profile_pic') if node.get('profile_pic') is not None and os.path.exists(
                        os.path.join(os.getcwd(), 'media', node.get('profile_pic'))) else 'default.jpg',
                    myself=node.get('hopLayer') == 0,
                    node_id=node.get('id'),
                    status=node.get('status'),
                    influencer=node.get('influencer')
                    )
        p.save()

        for status in node.get('status_list'):
            dt = datetime.fromtimestamp(status[1]+7200)  # calculate date and time from ms
            # TODO: the addition is a temporary fix (Something is wrong with the timezone)
            timezone = tzlocal.get_localzone()  # get the local timezone
            dt = timezone.localize(dt)  # adjust for timezone
            s = Status(timestamp=dt, status=status[0])  # create a status entry
            s.save()
            p.status_list.add(s)  # add the status entry to the status list of the current profile entry

    for link in data['links']:
        source = Profile.objects.filter(node_id=link['source']).first()
        target = Profile.objects.filter(node_id=link['target']).first()
        source.follows.add(target)
    print("Updated Database!")


def create_Recommendations(data):
    FollowRecommendations.objects.all().delete()
    for node in data['nodes']:
        r = FollowRecommendations(layer=node.get('hopLayer'), bacnet_id=node.get('BACnetID'), id = node.get('id'), name=node.get('name'),
                                  gender=node.get('gender'),
                                  birthday=node.get('birthday'), influencer = node.get('influencer'), age = calculate_age(node.get('birthday')), country=node.get('country'), town=node.get('town'),
                                  language=node.get('language'),
                                  levenshteinDistName = 100000,
                                  levenshteinDistTown = 100000,
                                  profile_pic=node.get('profile_pic') if node.get(
                                      'profile_pic') is not None else 'default.jpg')
        r.save()
    print("Updated Database!")

def calculate_age(date):
    a = date[0:4]
    b = date[5:7]
    c = date[8:10]
    birth_date = dt.date(int(a), int(b), int(c))
    end_date = dt.date.today()
    time_difference = end_date - birth_date
    age = int(time_difference.days/365)
    return age
