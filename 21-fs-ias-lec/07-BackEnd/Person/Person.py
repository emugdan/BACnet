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

    def __init__(self, id, name, feed):
        self.id = id
        self.name = name
        self.followlist = dict()
        self.gender = None
        self.birthday = None
        self.country = None
        self.town = None
        self.language = None
        self.status = None
        self.influencer = False

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
        #TODO: follow wird nie i Feed gschriebe, will immer e person mit emene feed wo none isch erstellt wird, me müesst also im konstruktor de feed go sueche? oder so? oder bim follow scho e perso oder feed biigeh?
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
            # TODO: generate JSON for changes
            generateJson(list(self.followlist.values()), self)

        else:
            print("couldn't find feed for person")

        # TODO: unfollow auch in Feed schreiben

    def get_follow_list(self):
        return self.followlist

    def print_follow_list(self):
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.followlist.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")

    # writes all the attributes into the feed except influencer
    def put_attributes(self):
        self.put_gender()
        self.put_birthday()
        self.put_town()
        self.put_country()
        self.put_language()
        self.put_status()

    def put_gender(self):
        self.feed.write_gender_to_feed(self, self.gender)

    def put_birthday(self):
        self.feed.write_birthday_to_feed(self, self.birthday)

    def put_country(self):
        self.feed.write_country_to_feed(self, self.country)

    def put_town(self):
        self.feed.write_town_to_feed(self, self.town)

    def put_language(self):
        self.feed.write_language_to_feed(self, self.language)

    def put_status(self):
        self.feed.write_status_to_feed(self, self.status)

    def put_influencer(self):
        self.feed.write_influencer_to_feed(self, self.influencer)