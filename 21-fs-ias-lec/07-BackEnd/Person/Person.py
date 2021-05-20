import sys

sys.path.append("../Feed")


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


    def follow(self, id, name):
        #TODO: follow wird nie i Feed gschriebe, will immer e person mit emene feed wo none isch erstellt wird, me müesst also im konstruktor de feed go sueche? oder so? oder bim follow scho e perso oder feed biigeh?
        friend = Person(id, name, None)
        self.followlist[id] = friend
        if friend.feed != None:
            self.feed.writeFollowToFeed(friend.feed)
            # TODO: generate JSON for changes
        else:
            print("couldn't find feed for person")

    def unfollow(self, id, name):
        exfriend = Person(id, name, None)
        self.followlist.pop(id)
        if exfriend.feed != None:
            self.feed.writeUnfollowToFeed(exfriend.feed)
            # TODO: generate JSON for changes
        else:
            print("couldn't find feed for person")

        # TODO: unfollow auch in Feed schreiben

    def getFollowList(self):
        return self.followlist

    def printFollowList(self):
        print("\n", self.name.upper(), "'S FOLLOW LIST\n")
        for key, value in self.followlist.items():
            print("ID:", key, " Name: ", value.name)
        print("\n")