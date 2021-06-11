import sys

sys.path.append("../Feed")
sys.path.append("../lib")

import crypto
import feed as fe

from generateJson import generateJson
from Feed import Feed


class Person:
    list_of_persons = None  # list of all known (= feed is in folder system) users
    main = None  # main Person (=Person who is logged in)

    name = ""  # name of the user
    id = 0  # BacNet id of the user
    feed = None  # feed of the user (refers to Feed.py)
    followlist = dict()  # list of all users who this user is following (id mapped to person object)

    gender = " "  # Attributes of this user
    birthday = None
    country = None
    town = None
    language = None
    status = None
    profile_pic = None  # TODO default pic - Y

    activity = 0  # metrics of this user
    influencer_count = 0
    influencer = False

    def __init__(self, id, name, feed):
        self.id = id
        self.name = name

        # search for feed if feed is not known already
        if feed is None:
            digestmod = "sha256"
            with open("./data/" + name + "/" + name + "-secret.key", 'r') as f:
                key = eval(f.read())
                h = crypto.HMAC(digestmod, key["private"], key["feed_id"])
                if sys.platform.startswith("linux"):
                    signer = crypto.HMAC(digestmod, bytes.fromhex(h.get_private_key()))
                else:
                    signer = crypto.HMAC(digestmod, h.get_private_key())

            feed_obj = fe.FEED(fname="./data/" + name + "/" + name + "-feed.pcap", fid=h.get_feed_id(),
                               signer=signer, create_if_notexisting=True, digestmod=digestmod)
            self.feed = Feed.Feed(self.id, feed_obj)

        else:
            self.feed = feed

        if feed is not None:
            for _ in feed.myFeed:
                self.activity += 1  # count the activities that are already on the feed

    # method if new follow appears: follow is written to feed and the json file for FrontEnd is updated
    def follow(self, id, name):
        friend = Person(id, name, None)
        self.followlist[id] = friend
        if friend.feed is not None:
            self.feed.write_follow_to_feed(friend.feed)  # generates a feed entry for the following
            self.activity += 1  # new activity of this user
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count += 1  # to know if friend is influencer now
                        person.put_influencer()
                generateJson(self.list_of_persons, self.main)  # update Json

        else:
            print("couldn't find feed for person")

    # method if new unfollow appears: unfollow is written to feed and the json file for FrontEnd is updated
    def unfollow(self, id, name):
        exfriend = Person(id, name, None)
        self.followlist.pop(id)  # remove friend from the follow list
        if exfriend.feed is not None:
            self.feed.write_unfollow_to_feed(exfriend.feed)  # generates feed entry for the unfollowing
            self.activity += 1  # new activity of this user
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count -= 1  # to know if friend is influencer
                        person.put_influencer()
                generateJson(self.list_of_persons, self.main)  # update Json

        else:
            print("couldn't find feed for person")

    # method to get the follow list of this user
    def get_follow_list(self):
        return self.followlist

    # print follow list to the console
    def print_follow_list(self):
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.followlist.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")

    # writes all the attributes into the feed except influencer and activity
    def put_attributes(self, gender, birthday, town, country, language, status):
        self.put_gender(gender)
        self.put_birthday(birthday)
        self.put_town(town)
        self.put_country(country)
        self.put_language(language)
        self.put_status(status)

    # writes new gender to feed and updates Json for FrontEnd
    def put_gender(self, gender):
        self.gender = gender
        self.feed.write_gender_to_feed(self.gender)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # writes new birthday to feed and updates Json for FrontEnd
    def put_birthday(self, birthday):
        self.birthday = birthday
        self.feed.write_birthday_to_feed(self.birthday)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # writes new country to feed and updates Json for FrontEnd
    def put_country(self, country):
        self.country = country
        self.feed.write_country_to_feed(self.country)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # writes new town to feed and updates Json for FrontEnd
    def put_town(self, town):
        self.town = town
        self.feed.write_town_to_feed(self.town)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # writes new language to feed and updates Json for FrontEnd
    def put_language(self, language):
        self.language = language
        self.feed.write_language_to_feed(self.language)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # writes new status to feed and updates Json for FrontEnd
    def put_status(self, status):
        self.status = status
        self.feed.write_status_to_feed(self.status)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # calculates if user is influencer or not: more than 3 follows -> influencer
    def put_influencer(self):

        if self.influencer_count > 3 and self.influencer is False:
            self.influencer = True
            self.feed.write_influencer_to_feed(self.influencer)
            self.activity += 1
            if self.list_of_persons is not None:
                generateJson(self.list_of_persons, self.main)

        if self.influencer_count < 3 and self.influencer is True:
            self.influencer = False
            self.feed.write_influencer_to_feed(self.influencer)
            self.activity += 1
            if self.list_of_persons is not None:
                generateJson(self.list_of_persons, self.main)

    # writes path to the new profile picture to feed and updates Json for FrontEnd
    def put_profile_pic(self, picture):
        self.profile_pic = picture
        self.feed.write_profile_pic_to_feed(self.profile_pic)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    # calculates how active a user is
    def get_activity(self):
        if self.activity < 10:
            return 0
        elif self.activity < 25:
            return 1
        elif self.activity < 45:
            return 2
        elif self.activity < 70:
            return 3
        elif self.activity < 100:
            return 4
        else:
            return 5
