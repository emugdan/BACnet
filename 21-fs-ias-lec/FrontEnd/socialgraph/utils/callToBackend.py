import sys
import os
import pathlib

#get the momentary path
x = pathlib.Path(__file__)
#move to directory ../21-fs-ias-lec

q = pathlib.Path(__file__).parent.parent / 'views.py'
print(q.parent.parent.parent)
os.chdir(q.parent.parent.parent)


#Append the path to get access to the modules
sys.path.append("07-BackEnd")
sys.path.append("07-BackEnd/Feed")
sys.path.append("07-BackEnd/lib")
sys.path.append("07-BackEnd/Person")


import main


from Feed import Feed
import feed

import generateDirectories
from Person import Person
from generateJson import generate_json
from Feed import Feed

import crypto

"""
iterate though the directories and determine the mainPerson and return the full list of persons
"""
def iterateThroughDirs(mainPersonName, mainPersonID):
    os.chdir("07-BackEnd")

    digestmod = "sha256"

    rootdir = "./data"
    list_of_persons = []
    mainPerson = None

    # durch alle Ordner in data iterieren
    for subdir, dirs, files in os.walk(rootdir):
        for name in dirs:
            # key der jeweiligen Person aulesen
            with open("data/" + name + "/" + name + "-secret.key", 'r') as f:
                key = eval(f.read())
                h = crypto.HMAC(digestmod, key["private"], key["feed_id"])
                if sys.platform.startswith("linux"):
                    signer = crypto.HMAC(digestmod, bytes.fromhex(h.get_private_key()))
                else:
                    signer = crypto.HMAC(digestmod, h.get_private_key())

            # Feed laden
            my_feed = feed.FEED(fname="data/" + name + "/" + name + "-feed.pcap", fid=h.get_feed_id(),
                                signer=signer, create_if_notexisting=True, digestmod=digestmod)

            # Feed objekt erstellen
            feed_obj = Feed.Feed(key["feed_id"], my_feed, name)

            person = Person.Person(key["feed_id"], name, feed_obj)
            list_of_persons.append(person)

            # TODO: Wie wird Hauptperson bestimmt?
            # Hauptperson ist vera
            if (sys.platform == "linux"):
                if (name == mainPersonName and key["feed_id"] == mainPersonID):
                    mainPerson = person
                    mainPerson.main = person
            else:
                if (name == mainPersonName and key["feed_id"] == mainPersonID.encode("utf-8")):
                    mainPerson = person
                    mainPerson.main = person



    return (mainPerson, list_of_persons)



"""
make unfollow call to BackEnd. The function creates an updated JSON file.
"""
def unfollowCall(mainPersonName, mainPersonID,unfollowPersonName, unfollowPersonID):
    os.chdir(q.parent.parent.parent)
    (mainPerson, list_of_persons) = iterateThroughDirs(mainPersonName, mainPersonID)
    helper(list_of_persons, mainPerson)
    if (sys.platform == "linux"):
        mainPerson.unfollow(unfollowPersonID, unfollowPersonName)
    else:
        mainPerson.unfollow(unfollowPersonID.encode("utf-8"), unfollowPersonName)



"""
make follow call to BackEnd. The function creates an updated JSON file.
"""
def followCall(mainPersonName, mainPersonID,followPersonName, followPersonID):
    os.chdir(q.parent.parent.parent)
    (mainPerson, list_of_persons) = iterateThroughDirs(mainPersonName, mainPersonID)
    helper(list_of_persons, mainPerson)
    if (sys.platform == "linux"):
        mainPerson.follow(followPersonID, followPersonName)
    else:
        mainPerson.follow(followPersonID.encode("utf-8"), followPersonName)



"""
make update call to BackEnd. The function creates an updated JSON file.
"""
def profileUpdateCall(mainPersonName, mainPersonID, data):
    print(q)
    os.chdir(q.parent.parent.parent)
    (mainPerson, list_of_persons) = iterateThroughDirs(mainPersonName, mainPersonID)
    helper(list_of_persons, mainPerson)
    mainPerson.put_attributes(data)


def helper(list_of_persons, main_person):
    for pers in list_of_persons:  # for each person read the attributes from the entries in the feed
        follow_list = pers.feed.read_follow_from_feed()
        birthday = pers.feed.read_birthday_from_feed()
        gender = pers.feed.read_gender_from_feed()
        country = pers.feed.read_country_from_feed()
        town = pers.feed.read_town_from_feed()
        language = pers.feed.read_language_from_feed()
        status, status_list = pers.feed.read_status_from_feed()
        profile_pic = pers.feed.read_profile_pic_from_feed()
        pers.list_of_persons = list_of_persons

        for follow_entry in follow_list:  # creates follow list
            for p in list_of_persons:  # go through all persons
                if follow_entry["Feed ID"] == p.id:
                    pers.follow(follow_entry["Feed ID"], p.name)
                    break

        pers.print_follow_list()  # for testing
        pers.birthday = birthday
        pers.gender = gender
        pers.country = country
        pers.town = town
        pers.language = language
        pers.status = status
        pers.status_list = status_list
        pers.profile_pic = profile_pic

        # tell each person who the mainPerson is and what persons we "know" (= have the feed at the moment)
        pers.main = main_person



#For testing purposes
if __name__ =="__main__":

    followCall(mainPersonName="vera", mainPersonID="9ff78df97744c0d5", followPersonName="esther", followPersonID="4076cc22fa40fa84")

