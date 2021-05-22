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


def main():
    # dummy Feeds erstellen -> später feeds die schon geladen sind
    # generateDirectories.generateDirectories()
    directoriesGenerator.createDirectories(100, 20)

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
            list_of_persons.append(person)

            # TODO: Wie wird Hauptperson bestimmt?
            # Hauptperson ist vera
            # if (name == "vera"):
                # mainPerson = person

            mainPerson = dirs[0]

    for pers in list_of_persons:
        follow_list = pers.feed.readFollowFromFeed()
        # Followliste vervollständigen
        for follow_entry in follow_list:
            for p in list_of_persons:
                if follow_entry["Feed ID"] == p.id:
                    pers.follow(follow_entry["Feed ID"], p.name)
                    break
        pers.printFollowList()


    # Json file for FrontEnd
    generateJson(list_of_persons, mainPerson)

if __name__ == "__main__":
    main()
