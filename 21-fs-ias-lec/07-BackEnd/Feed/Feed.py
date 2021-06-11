import sys

# add the lib to the module folder
sys.path.append("../lib")

import time


class Feed:

    def __init__(self, id, myFeed):
        self.myFeed = myFeed                # Feed from lib/feed.py
        self.id = id                        # BacNetID
        self.timestamp = None               # TODO: ??

    # writes a new follow to the feed
    def write_follow_to_feed(self, newFriendsFeed):
        self.myFeed.write(["bacnet/following", time.time(), newFriendsFeed.id])

    # writes a new unfollow to the feed
    def write_unfollow_to_feed(self, exFriendsFeed):
        self.myFeed.write(["bacnet/unfollowing", time.time(), exFriendsFeed.id])

    # reads the followList from the feed
    def read_follow_from_feed(self):
        follow_list = []
        id_list = []

        for event in self.myFeed:
            if event.content()[0] == "bacnet/following":
                # if event is a following, add follow to list
                friends_id = event.content()[2]
                if friends_id not in id_list:
                    follow_list.append({"Root": self.id, "time": event.content()[1], "Feed ID": event.content()[2]})
                    id_list.append(friends_id)
            if event.content()[0] == "bacnet/unfollowing":
                # if it is an unollowing, remove the follow from the list
                friends_id = event.content()[2]
                for entry in follow_list:
                    if entry["Feed ID"] == friends_id:
                        follow_list.remove(entry)
                        id_list.remove(friends_id)

        follow_list.sort(key=lambda msg: msg["time"])
        return follow_list

    # reads the current birthday from the feed
    def read_birthday_from_feed(self):
        my_birthday = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/birthday":
                my_birthday = event.content()[2]

        return my_birthday

    # reads the current gender from the feed
    def read_gender_from_feed(self):
        gender = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/gender":
                gender = event.content()[2]

        return gender

    # reads the current country from the feed
    def read_country_from_feed(self):
        country = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/country":
                country = event.content()[2]

        return country

    # reads the current town from the feed
    def read_town_from_feed(self):
        town = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/town":
                town = event.content()[2]

        return town

    # reads the current language from the feed
    def read_language_from_feed(self):
        language = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/language":
                language = event.content()[2]

        return language

    # reads the current status from the feed
    def read_status_from_feed(self):
        status = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/status":
                status = event.content()[2]

        return status

    # reads the path of the current profile pic - Y
    def read_profile_pic_from_feed(self):
        path = None
        for event in self.myFeed:
            if event.content()[0] == "bacnet/profile_pic":
                path = event.content()[2]
        # if path not valid return .. path to a default pic..
        return path

    # writes the new gender to the feed
    def write_gender_to_feed(self, gender):
        self.myFeed.write(["bacnet/gender", time.time(), gender])

    # writes the new birthday to the feed
    def write_birthday_to_feed(self, birthday):
        self.myFeed.write(["bacnet/birthday", time.time(), birthday])

    # writes the new country to the feed
    def write_country_to_feed(self, country):
        self.myFeed.write(["bacnet/country", time.time(), country])

    # writes the new town to the feed
    def write_town_to_feed(self, town):
        self.myFeed.write(["bacnet/town", time.time(), town])

    # writes the new language to the feed
    def write_language_to_feed(self, language):
        self.myFeed.write(["bacnet/language", time.time(), language])

    # writes the new status to the feed
    def write_status_to_feed(self, status):
        time_var = time.time()
        self.myFeed.write(["bacnet/status", time_var, status])
        if self.timestamp is None:
            self.timestamp = time_var

    # writes the influencer status to feed
    def write_influencer_to_feed(self, influencer):
        self.myFeed.write(["bacnet/influencer", time.time(), influencer])

    # writes the new profile picture to the feed
    def write_profile_pic_to_feed(self, path):
        self.myFeed.write(["bacnet/profile_pic", time.time(), path])
