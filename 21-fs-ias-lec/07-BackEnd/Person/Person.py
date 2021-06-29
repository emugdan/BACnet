import sys

sys.path.append("../Feed")
sys.path.append("../lib")

import crypto
import feed as fe

from generateJson import generate_json
from Feed import Feed


class Person:

    name = ""  # name of the user
    id = 0  # BacNet id of the user
    feed = None  # feed of the user (refers to Feed.py)

    def __init__(self, id, name, feed):  # creates a new person with a feed and an id
        self.id = id
        self.name = name
        self.feed = feed
        self.follow_list = dict()  # list of all users who this user is following (id mapped to person object)

        self.list_of_persons = None  # list of all known (= feed is in folder system) users
        self.main = None  # main Person (=Person who is logged in)

        # Attributes of this user
        self.gender = " "
        self.birthday = None
        self.country = None
        self.town = None
        self.language = None
        self.status = None
        self.profile_pic = "./media/default_pic.jpg"
        self.activity = 0  # number of events on the feed
        self.influencer_count = 0
        self.influencer = False

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
            self.feed = Feed.Feed(self.id, feed_obj, name)

        else:
            self.feed = feed

        if feed is not None:
            for _ in feed.myFeed:
                self.activity += 1  # count the activities that are already on the feed

    def follow(self, id, name):    # follow appears: follow is written to feed and the json file gets updated
        friend = Person(id, name, None)
        self.follow_list[id] = friend
        if friend.feed is not None:
            self.feed.write_follow_to_feed(friend.feed)  # generates a feed entry for the following
            self.activity += 1  # new activity of this user
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count += 1  # to know if friend is influencer now
                        person.put_influencer()
                generate_json(self.list_of_persons, self.main)  # update Json

        else:
            print("couldn't find feed for person")

    def unfollow(self, id, name):    # unfollow appears: unfollow is written to feed and the json file gets updated
        exfriend = Person(id, name, None)
        self.follow_list.pop(id)  # remove friend from the follow list
        if exfriend.feed is not None:
            self.feed.write_unfollow_to_feed(exfriend.feed)  # generates feed entry for the unfollowing
            self.activity += 1  # new activity of this user
            if self.list_of_persons is not None:
                for person in self.list_of_persons:
                    if person.id == id:
                        person.influencer_count -= 1  # to know if friend is influencer
                        person.put_influencer()
                generate_json(self.list_of_persons, self.main)  # update Json

        else:
            print("couldn't find feed for person")

    def get_follow_list(self):    # method to get the follow list of this user
        return self.follow_list

    def print_follow_list(self):     # print follow list to the console
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.follow_list.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")

    def put_attributes(self, gender, birthday, town, country, language, status, profile_pic):    # writes given attributes to feed
        self.put_gender(gender)
        self.put_birthday(birthday)
        self.put_town(town)
        self.put_country(country)
        self.put_language(language)
        self.put_status(status)
        self.put_profile_pic(profile_pic)

    def put_gender(self, gender):    # writes new gender to feed and updates Json for FrontEnd
        self.gender = gender
        self.feed.write_gender_to_feed(self.gender)
        self.activity += 1
        generate_json(self.list_of_persons, self.main)

    def put_birthday(self, birthday):    # writes new birthday to feed and updates Json for FrontEnd
        self.birthday = birthday
        self.feed.write_birthday_to_feed(self.birthday)
        self.activity += 1
        generate_json(self.list_of_persons, self.main)

    def put_country(self, country):    # writes new country to feed and updates Json for FrontEnd
        self.country = country
        self.feed.write_country_to_feed(self.country)

    def put_town(self, town):
        self.town = town
        self.feed.write_town_to_feed(self.town)

    def put_language(self, language):
        self.language
        self.feed.write_language_to_feed(self.language)

    def put_status(self, status):
        self.status
        self.feed.write_status_to_feed(self.status)

    def put_influencer(self):
        self.feed.write_influencer_to_feed(self.influencer)