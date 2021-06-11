import sys


sys.path.append("../Feed")
sys.path.append("../lib")

import os
import crypto
import feed as fe

from generateJson import generateJson
from Feed import Feed


class Person:
    name = ""
    id = 0
    feed = None
    followlist = None
    activity = 0

    def __init__(self, id, name, feed):
        self.id = id
        self.name = name
        self.followlist = dict()
        self.gender = " "
        self.birthday = None
        self.country = None
        self.town = None
        self.language = None
        self.status = None
        self.influencer = False
        self.profile_pic = None #TODO default pic - Y

        if feed == None:
            digestmod = "sha256"
            with open("./data/" + name + "/" + name + "-secret.key", 'r') as f:
                key = eval(f.read())
                h = crypto.HMAC(digestmod, key["private"], key["feed_id"])
                if sys.platform.startswith("linux"):
                    signer = crypto.HMAC(digestmod, bytes.fromhex(h.get_private_key()))
                else:
                    signer = crypto.HMAC(digestmod, h.get_private_key())

            feedObj = fe.FEED(fname="./data/" + name + "/" + name + "-feed.pcap", fid=h.get_feed_id(),
                      signer=signer, create_if_notexisting=True, digestmod=digestmod)
            self.feed = Feed.Feed(self.id, feedObj)


        else:
            self.feed = feed


    def follow(self, id, name):
        friend = Person(id, name, None)
        self.followlist[id] = friend
        if friend.feed != None:
            self.feed.write_follow_to_feed(friend.feed)
            generateJson(list(self.followlist.values()), self)

        else:
            print("couldn't find feed for person")

    def unfollow(self, id, name):
        exfriend = Person(id, name, None)
        self.followlist.pop(id)
        if exfriend.feed != None:
            self.feed.write_unfollow_to_feed(exfriend.feed)
            generateJson(list(self.followlist.values()), self)

        else:
            print("couldn't find feed for person")

    def get_follow_list(self):
        return self.followlist

    def print_follow_list(self):
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.followlist.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")

    # writes all the attributes into the feed except influencer
    def put_attributes(self, gender, birthday, town, country, language, status):
        self.put_gender(gender)
        self.put_birthday(birthday)
        self.put_town(town)
        self.put_country(country)
        self.put_language(language)
        self.put_status(status)

    def put_gender(self, gender):
        self.gender = gender
        self.feed.write_gender_to_feed(self.gender)
        generateJson(list(self.followlist.values()), self)

    def put_birthday(self, birthday):
        self.birthday = birthday
        self.feed.write_birthday_to_feed(self.birthday)
        generateJson(list(self.followlist.values()), self)

    def put_country(self, country):
        self.country = country
        self.feed.write_country_to_feed(self.country)
        generateJson(list(self.followlist.values()), self)

    def put_town(self, town):
        self.town = town
        self.feed.write_town_to_feed(self.town)
        generateJson(list(self.followlist.values()), self)

    def put_language(self, language):
        self.language = language
        self.feed.write_language_to_feed(self.language)
        generateJson(list(self.followlist.values()), self)

    def put_status(self, status):
        self.status = status
        self.feed.write_status_to_feed(self.status)
        generateJson(list(self.followlist.values()), self)

    def put_influencer(self):
        self.feed.write_influencer_to_feed(self.influencer)

    def put_profile_pic(self):
        self.feed.write_profile_pic_to_feed(self.profile_pic)