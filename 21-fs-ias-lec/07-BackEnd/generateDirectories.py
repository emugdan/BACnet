import sys

sys.path.append("lib")

from Feed import Feed

# TODO: villicht das in Feed-Ordner integriere
def generateDirectories():
    # set a name to a feed
    Feeds = {}

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

