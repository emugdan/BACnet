import generateDirectories
from Person import Person
from generateJson import generateJson
from Feed import Feed

import sys

# add the lib to the module folder
sys.path.append("lib")

import os
import crypto
import feed


def main():
    # generates dummy feeds -> later not used anymore because feeds are generated through feedSyc or feedCtrl ...

    # To use the directories generator swap out comments:
    # - The two just below (this file - l. 27 - 28)
    # - Determination of main_person (this file - l. 58 - 61)
    # - Path in generateJson.py to save in different json file (l. 50 - 51)
    # - Path in views.py to choose desired json file (l. 18 - 19)

    generateDirectories.generateDirectories()
    # directoriesGenerator.createDirectories(300, 5)

    # read the feeds that are saved in the directory
    digestmod = "sha256"
    rootdir = "./data"
    list_of_persons = []  # list of all persons of whom a feed exists
    main_person = None

    # iterate through all folders in "data"
    for subdir, dirs, files in os.walk(rootdir):
        for name in dirs:
            # read key of each person
            with open("data/" + name + "/" + name + "-secret.key", 'r') as f:
                key = eval(f.read())
                h = crypto.HMAC(digestmod, key["private"], key["feed_id"])
                if sys.platform.startswith("linux"):
                    signer = crypto.HMAC(digestmod, bytes.fromhex(h.get_private_key()))
                else:
                    signer = crypto.HMAC(digestmod, h.get_private_key())

            # load feed
            my_feed = feed.FEED(fname="data/" + name + "/" + name + "-feed.pcap", fid=h.get_feed_id(),
                                signer=signer, create_if_notexisting=True, digestmod=digestmod)

            # initialize feed object
            feed_obj = Feed.Feed(key["feed_id"], my_feed)

            # initialize person object and add it to the list
            person = Person.Person(key["feed_id"], name, feed_obj)
            list_of_persons.append(person)

            # TODO: Wie wird Hauptperson bestimmt?
            # main person is "vera" in our case
            if name == "vera":
                main_person = person

    # for each person read the attributes from the entries in the feed
    for pers in list_of_persons:
        follow_list = pers.feed.read_follow_from_feed()
        birthday = pers.feed.read_birthday_from_feed()
        gender = pers.feed.read_gender_from_feed()
        country = pers.feed.read_country_from_feed()
        town = pers.feed.read_town_from_feed()
        language = pers.feed.read_language_from_feed()
        status = pers.feed.read_status_from_feed()

        # follow list
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

        # tell each person who the mainPerson is and what persons we "know" (= have the feed at the moment)
        pers.main = main_person
        pers.list_of_persons = list_of_persons

    # Json file for FrontEnd
    generateJson(list_of_persons, main_person)

    # TODO: das uselösche am schluss lol
    # test the methods in BackEnd
    main_person.put_attributes("female", "1999-02-13", "Basel", "Schweiz", "Deutsch", "ich bi s verii")
    main_person.put_town("Ehrendingen")
    main_person.put_status("lol")


if __name__ == "__main__":
    main()
