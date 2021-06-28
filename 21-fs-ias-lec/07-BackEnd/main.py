import generateDirectories
from Person import Person
from generateJson import generate_json
from Feed import Feed

import sys

# add the lib to the module folder
sys.path.append("lib")

import os
import crypto
import feed


def main():  # generates dummy feeds, later not used anymore -> feeds should be generated through feedSyc/ feedCtrl

    generateDirectories.generate_directories()
    # for testing large node number use: directoriesGenerator.create_directories_for_random_names(300, 5)

    # read the feeds that are saved in the directory
    digestmod = "sha256"
    rootdir = "./data"
    list_of_persons = []  # list of all persons of whom a feed exists
    main_person = None

    for subdir, dirs, files in os.walk(rootdir):  # iterate through all folders in 'data'
        for name in dirs:
            with open("data/" + name + "/" + name + "-secret.key", 'r') as f:  # read key of each person
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

            if name == "vera":  # main person is 'vera' in our case, should be determine from a login or similar
                main_person = person

    for pers in list_of_persons:  # for each person read the attributes from the entries in the feed
        follow_list = pers.feed.read_follow_from_feed()
        birthday = pers.feed.read_birthday_from_feed()
        gender = pers.feed.read_gender_from_feed()
        country = pers.feed.read_country_from_feed()
        town = pers.feed.read_town_from_feed()
        language = pers.feed.read_language_from_feed()
        status = pers.feed.read_status_from_feed()
        pers.list_of_persons = list_of_persons

        for follow_entry in follow_list:  # creates follow list
            for p in list_of_persons:  # go through all persons
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

    # Json file for FrontEnd
    generate_json(list_of_persons, main_person)


if __name__ == "__main__":
    main()
