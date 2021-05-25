import sys

# add the lib to the module folder
sys.path.append("../lib")

import time


class Feed:

    def __init__(self, id, myFeed):
        self.myFeed = myFeed
        self.id = id

    # TODO: methode zum geburtstag und so au in feed ine schriibe implementiere


    # adds new Follow to the Feed
    def writeFollowToFeed(self, newFriendsFeed):
        self.myFeed.write(["bacnet/following", time.time(), newFriendsFeed.id])

    # adds new Unfollow to the Feed
    def writeUnfollowToFeed(self, exFriendsFeed):
        self.myFeed.write(["bacnet/unfollowing", time.time(), exFriendsFeed.id])

    # reads the followList from the Feed
    def readFollowFromFeed(self):
        followList = []
        IDlist = []

        for event in self.myFeed:
            if event.content()[0] == "bacnet/following":
                friends_id = event.content()[2]
                if friends_id not in IDlist:
                    followList.append({"Root": self.id, "time": event.content()[1], "Feed ID": event.content()[2]})
                    IDlist.append(friends_id)

        followList.sort(key=lambda msg: msg["time"])
        return followList
