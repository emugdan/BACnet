import sys

sys.path.append("lib")

from Feed import Feed
from Person import Person
from generateJson import generateJson


def main():
    # set a name to a feed
    Feeds = {}
    Persons = {}

    Feeds['yasmin'] = Feed.Feed("yasmin")
    Feeds['esther'] = Feed.Feed("esther")
    Feeds['vera'] = Feed.Feed("vera")
    Feeds['pascal'] = Feed.Feed("pascal")
    Feeds['phillip'] = Feed.Feed("phillip")
    Feeds['sebastian'] = Feed.Feed("sebastian")

    Feeds['aline'] = Feed.Feed("aline")
    Feeds['ben'] = Feed.Feed("ben")
    Feeds['caroline'] = Feed.Feed("caroline")
    Feeds['david'] = Feed.Feed("david")
    Feeds['eveline'] = Feed.Feed("eveline")
    Feeds['fitzgerald'] = Feed.Feed("fitzgerald")
    Feeds['georgia'] = Feed.Feed("georgia")
    Feeds['henry'] = Feed.Feed("henry")
    Feeds['isabelle'] = Feed.Feed("isabelle")
    Feeds['julius'] = Feed.Feed("julius")

    # Feeds erstellen
    for name, feed in Feeds.items():
        feed.generateOwnFeed()
        Persons[name] = Person.Person(feed.id, feed.name, feed)

    Persons['vera'].follow(Persons['esther'].id, Persons['esther'].name)
    Persons['vera'].follow(Persons['yasmin'].id, Persons['yasmin'].name)
    Persons['vera'].follow(Persons['aline'].id, Persons['aline'].name)
    Persons['vera'].follow(Persons['caroline'].id, Persons['caroline'].name)
    Persons['esther'].follow(Persons['ben'].id, Persons['ben'].name)
    Persons['esther'].follow(Persons['david'].id, Persons['david'].name)
    Persons['esther'].follow(Persons['pascal'].id, Persons['pascal'].name)
    Persons['yasmin'].follow(Persons['eveline'].id, Persons['eveline'].name)
    Persons['pascal'].follow(Persons['phillip'].id, Persons['phillip'].name)
    Persons['pascal'].follow(Persons['phillip'].id, Persons['phillip'].name)
    Persons['pascal'].follow(Persons['isabelle'].id, Persons['isabelle'].name)
    Persons['phillip'].follow(Persons['yasmin'].id, Persons['yasmin'].name)
    Persons['phillip'].follow(Persons['sebastian'].id, Persons['sebastian'].name)
    Persons['phillip'].follow(Persons['georgia'].id, Persons['georgia'].name)
    Persons['sebastian'].follow(Persons['henry'].id, Persons['henry'].name)

    Persons['fitzgerald'].follow(Persons['pascal'].id, Persons['pascal'].name)
    Persons['fitzgerald'].follow(Persons['julius'].id, Persons['julius'].name)

    persList = []
    for person in Persons.values():
        person.printFollowList()
        persList.append(person)

    # Takes a list of all Persons and the Person we are as arguments
    generateJson(persList, Persons['vera'])


if __name__ == "__main__":
    main()
