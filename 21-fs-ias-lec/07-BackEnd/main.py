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


def main(argv):  # generates dummy feeds, later not used anymore -> feeds should be generated through feedSyc/ feedCtrl
    generateDirectories.generate_directories()
    # for testing large node number use: directoriesGenerator.create_directories_for_random_names(300, 5)

    # read the feeds that are saved in the directory
    digestmod = "sha256"
    rootdir = "./data"
    list_of_persons = []  # list of all persons of whom a feed exists
    main_person = None
    # TODO: Vera: wenns ned klappet nur s else verwende
    if(argv[0] == "FrontEnd"):
        name_main_person = argv[1]
    else:
        if len(argv) != 1: # more than one parameter --> print error
            print("ERROR: wrong number of parameters, please insert one parameter with the name of the main person")
            return
        name_main_person = argv[0]

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
            feed_obj = Feed.Feed(key["feed_id"], my_feed, name)

            # initialize person object and add it to the list
            person = Person.Person(key["feed_id"], name, feed_obj)
            list_of_persons.append(person)

            if name == name_main_person:  # main person is 'vera' in our case, should be determine from a login or similar
                main_person = person
    if main_person == None: # main person could not be found
        print("ERROR: main person not found, try a different name")
        return
    for pers in list_of_persons:  # for each person read the attributes from the entries in the feed
        follow_list = pers.feed.read_follow_from_feed()
        birthday = pers.feed.read_birthday_from_feed()
        gender = pers.feed.read_gender_from_feed()
        country = pers.feed.read_country_from_feed()
        town = pers.feed.read_town_from_feed()
        language = pers.feed.read_language_from_feed()
        status, status_list = pers.feed.read_status_from_feed()
        profile_pic = pers.feed.read_profile_pic_from_feed()  # TODO profile pic, profile_pic_data
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
        # pers.profile_pic_data = profile_pic_data # TODO profile pic changes

        # tell each person who the mainPerson is and what persons we "know" (= have the feed at the moment)
        pers.main = main_person

    # Json file for FrontEnd
    generate_json(list_of_persons, main_person)
    #TODO: Vera: wenns ned klappet lösche
    if argv[0] == "FrontEnd":
        return (main_person, list_of_persons)


if __name__ == "__main__":
    main(sys.argv[1:])
