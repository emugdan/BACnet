import sys

# add the lib to the module folder
sys.path.append("../lib")

import time


class Feed:

    def __init__(self, id, myFeed):
        self.myFeed = myFeed
        self.id = id
        self.timestamp = None

    # adds new Follow to the Feed
    def write_follow_to_feed(self, newFriendsFeed):
        self.myFeed.write(["bacnet/following", time.time(), newFriendsFeed.id])

    # adds new Unfollow to the Feed
    def write_unfollow_to_feed(self, exFriendsFeed):
        self.myFeed.write(["bacnet/unfollowing", time.time(), exFriendsFeed.id])

    # reads the followList from the Feed
    def read_follow_from_feed(self):
        followList = []
        IDlist = []

        for event in self.myFeed:
            if event.content()[0] == "bacnet/following":
                friends_id = event.content()[2]
                if friends_id not in IDlist:
                    followList.append({"Root": self.id, "time": event.content()[1], "Feed ID": event.content()[2]})
                    IDlist.append(friends_id)
            if event.content()[0] == "bacnet/unfollowing":
                friends_id = event.content()[2]
                for entry in followList:
                    if (entry["Feed ID"] == friends_id):
                        followList.remove(entry)
                        IDlist.remove(friends_id)

        followList.sort(key=lambda msg: msg["time"])
        return followList

    def readBirthdayFromFeed(self):
        myBirthday = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/birthday":
                myBirthday = event.content()[2]

        return myBirthday

    def readGenderFromFeed(self):
        gender = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/gender":
                gender = event.content()[2]

        return gender

    def readCountryFromFeed(self):
        country = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/country":
                country = event.content()[2]

        return country

    def readTownFromFeed(self):
        town = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/town":
                town = event.content()[2]

        return town

    def readLanguageFromFeed(self):
        language = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/language":
                language = event.content()[2]

        return language

    def readStatusFromFeed(self):
        status = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/status":
                status = event.content()[2]

        return status

    def write_gender_to_feed(self, gender):
        self.myFeed.write(["bacnet/gender", time.time(), gender])

    def write_birthday_to_feed(self, birthday):
        self.myFeed.write(["bacnet/birthday", time.time(), birthday])

    def write_country_to_feed(self, country):
        self.myFeed.write(["bacnet/country", time.time(), country])

    def write_town_to_feed(self, town):
        self.myFeed.write(["bacnet/town", time.time(), town])

    def write_language_to_feed(self, language):
        self.myFeed.write(["bacnet/language", time.time(), language])

    def write_status_to_feed(self, status):
        time_var = time.time()
        self.myFeed.write(["bacnet/status", time_var, status])
        if self.timestamp is None:
            self.timestamp = time_var

    def write_influencer_to_feed(self, influencer):
        self.myFeed.write(["bacnet/influencer", time.time(), influencer])
