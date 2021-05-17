import sys

sys.path.append("../Feed")
import Feed


class Person:
    name = ""
    id = 0
    feed = None
    followlist = None

    def __init__(self, id, name, feed):
        self.id = id
        self.name = name
        self.followlist = dict()

        if feed == None:
            self.feed = None
            self.followList = None

        else:
            self.feed = feed

    def initialFollowList(self): # TODO: am Anfang alle follows die schon in Feed sind auslesen und in followlist einfügen -> unfollow auch beachten!!
        return


    def follow(self, id, name):
        friend = Person(id, name, None)
        self.followlist[id] = friend
        if friend.feed != None:
            self.feed.writeFollowToFeed(friend.feed)
        else:
            print("couldn't find feed for person")

    def unfollow(self, id):
        self.followlist.pop(id)
        # TODO: unfollow auch in Feed schreiben

    def getFollowList(self):
        return self.followlist

    def printFollowList(self):
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.followlist.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")