import generateDirectories
import directoriesGenerator
from Person import Person
from generateJson import generateJson
from Feed import Feed

import sys

# add the lib to the module folder
sys.path.append("lib")

import os
import crypto
import feed
import time


def mainGenerator(data):
    # If called from the Frontend we have to change the directory
    oldDir = os.getcwd()
    if data is not None:
        backEnd = oldDir.replace("FrontEnd", "07-BackEnd")
        os.chdir(backEnd)

    # dummy Feeds erstellen -> später feeds die schon geladen sind

    # To use the directories generator swap out comments:
    # - The two just below (this file - l. 27 - 28)
    # - Determination of mainPerson (this file - l. 58 - 61)
    # - Path in generateJson.py to save in different json file (l. 50 - 51)
    # - Path in views.py to choose desired json file (l. 18 - 19)

    generateDirectories.generateDirectories()
    # directoriesGenerator.createDirectories(300, 5)

    # die schon bestehenden Feeds auslesen und Feed und Personenobjekte erstellen
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
            feed_obj = Feed.Feed(key["feed_id"], my_feed)

            person = Person.Person(key["feed_id"], name, feed_obj)
            # Update or add the Attributes if there any in the updatedata.
            if data is not None and 'BACnetID' in data.keys() and key["feed_id"] == data['BACnetID'].encode('utf-8'):
                person.put_attributes(data)
            list_of_persons.append(person)

            # TODO: Wie wird Hauptperson bestimmt?
            # Hauptperson ist vera
            if (name == "vera"):
                mainPerson = person

            # mainPerson = dirs[0]

    for pers in list_of_persons:
        follow_list = pers.feed.read_follow_from_feed()
        birthday = pers.feed.readBirthdayFromFeed()
        gender = pers.feed.readGenderFromFeed()
        country = pers.feed.readCountryFromFeed()
        town = pers.feed.readTownFromFeed()
        language = pers.feed.readLanguageFromFeed()
        status = pers.feed.readStatusFromFeed()

        # Followliste vervollständigen
        for follow_entry in follow_list:
            for p in list_of_persons:
                if follow_entry["Feed ID"] == p.id:
                    pers.follow(follow_entry["Feed ID"], p.name)
                    break

        pers.print_follow_list()
        pers.birthday = birthday
        pers.gender = gender
        pers.country = country
        pers.town = town
        pers.language = language
        pers.status = status

    # Json file for FrontEnd
    # mainPerson.put_attributes({'gender': "female", 'birthday': "1999-02-13", 'town': "Basel", 'country': "Schweiz", 'language': "Deutsch", 'status': "ich bi s verii"})
    generateJson(list_of_persons, mainPerson)
    os.chdir(oldDir)


def main():
    mainGenerator(None)


if __name__ == "__main__":
    main()
