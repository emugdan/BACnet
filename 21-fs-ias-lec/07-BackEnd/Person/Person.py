import sys

sys.path.append("../Feed")
sys.path.append("../lib")

import os
import crypto
import feed as fe

from generateJson import generateJson
from Feed import Feed


class Person:
    list_of_persons = None
    main = None

    name = ""
    id = 0
    feed = None
    followlist = dict()

    gender = " "
    birthday = None
    country = None
    town = None
    language = None
    status = None
    profile_pic = None  # TODO default pic - Y

    activity = 0
    influencer_count = 0
    influencer = False

    def __init__(self, id, name, feed):
        self.id = id
        self.name = name

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

        if feed is not None:
            for event in feed.myFeed:
                self.activity += 1

    def follow(self, id, name):
        friend = Person(id, name, None)
        self.followlist[id] = friend
        if friend.feed is not None:
            self.feed.write_follow_to_feed(friend.feed)
            self.activity += 1
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count += 1
                        person.put_influencer()
                generateJson(self.list_of_persons, self.main)

        else:
            print("couldn't find feed for person")

    def unfollow(self, id, name):
        exfriend = Person(id, name, None)
        self.followlist.pop(id)
        if exfriend.feed is not None:
            self.feed.write_unfollow_to_feed(exfriend.feed)
            self.activity += 1
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count -= 1
                        person.put_influencer()
                generateJson(self.list_of_persons, self.main)

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
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    def put_birthday(self, birthday):
        self.birthday = birthday
        self.feed.write_birthday_to_feed(self.birthday)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    def put_country(self, country):
        self.country = country
        self.feed.write_country_to_feed(self.country)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    def put_town(self, town):
        self.town = town
        self.feed.write_town_to_feed(self.town)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    def put_language(self, language):
        self.language = language
        self.feed.write_language_to_feed(self.language)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

    def put_status(self, status):
        self.status = status
        self.feed.write_status_to_feed(self.status)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

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

    def put_profile_pic(self, picture):
        self.profile_pic = picture
        self.feed.write_profile_pic_to_feed(self.profile_pic)
        self.activity += 1
        generateJson(self.list_of_persons, self.main)

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
