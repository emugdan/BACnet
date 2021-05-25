import sys

# add the lib to the module folder


import os
import BackEnd.lib.crypto as crypto
import BackEnd.lib.feed as feed
import time


def generate(name):
    if not os.path.isdir("data"):
        os.mkdir("data")

    if not os.path.isdir("data/" + name):
        os.mkdir("data/" + name)

    # Generate a key pair

    # generate a feed
    digestmod = "sha256"
    h, signer = None, None

    # Generate a Key if non exists
    if not os.path.isfile("data/" + name + "/" + name + "-secret.key"):
        # print("Create " + name + "'s key pair at data/" + name + "/" + name + "-secret.key")
        h = crypto.HMAC(digestmod)
        h.create()
        with open("data/" + name + "/" + name + "-secret.key", "w") as f:
            f.write('{\n  ' + (',\n '.join(h.as_string().split(','))[1:-1]) + '\n}')
            signer = crypto.HMAC(digestmod, h.get_private_key())

    # print("Read " + name + "'s secret key.")
    with open("data/" + name + "/" + name + "-secret.key", 'r') as f:
        key = eval(f.read())
        h = crypto.HMAC(digestmod, key["private"], key["feed_id"])
        if sys.platform.startswith("linux"):
            signer = crypto.HMAC(digestmod, bytes.fromhex(h.get_private_key()))
        else:
            signer = crypto.HMAC(digestmod, h.get_private_key())

    # print("Create or load " + name + "'s feed at data/" + name + "/" + name + "-feed.pcap")
    myFeed = feed.FEED(fname="data/" + name + "/" + name + "-feed.pcap", fid=h.get_feed_id(),
                       signer=signer, create_if_notexisting=True, digestmod=digestmod)

    return myFeed, key["feed_id"]


def generateDirectories():
    yasmin, yasmins_id = generate("yasmin")
    esther, esthers_id = generate("esther")
    vera, veras_id = generate("vera")
    pascal, pascals_id = generate("pascal")
    phillip, phillips_id = generate("phillip")
    sebastian, sebastians_id = generate("sebastian")
    aline, alines_id = generate("aline")
    ben, bens_id = generate("ben")
    caroline, carolines_id = generate("caroline")
    david, davids_id = generate("david")
    eveline, evelines_id = generate("eveline")
    fitzgerald, fitzgeralds_id = generate("fitzgerald")
    georgia, georgias_id = generate("georgia")
    henry, henrys_id = generate("henry")
    isabelle, isabelles_id = generate("isabelle")
    julius, julius_id = generate("julius")
    veri, veris_id = generate("veri")



    yasmin.write(["bacnet/following", time.time(), veras_id]) # folgt Vera
    yasmin.write(["bacnet/following", time.time(), esthers_id]) # folgt Esther
    yasmin.write(["bacnet/following", time.time(), julius_id]) # folgt Julius

    vera.write(["bacnet/following", time.time(), esthers_id])  # folgt Esther
    vera.write(["bacnet/following", time.time(), yasmins_id])  # folgt Yasmin
    vera.write(["bacnet/following", time.time(), sebastians_id])  # folgt Sebastian
    vera.write(["bacnet/following", time.time(), pascals_id])  # folgt Pascal
    vera.write(["bacnet/following", time.time(), phillips_id])  # folgt Phillip

    esther.write(["bacnet/following", time.time(), yasmins_id])  # folgt Yasmin
    esther.write(["bacnet/following", time.time(), veras_id]) # folgt Vera
    esther.write(["bacnet/following", time.time(), davids_id])  # folgt David

    pascal.write(["bacnet/following", time.time(), sebastians_id])  # folgt Sebastian
    pascal.write(["bacnet/following", time.time(), phillips_id])  # folgt Phillip

    phillip.write(["bacnet/following", time.time(), sebastians_id])  # folgt Sebastian
    phillip.write(["bacnet/following", time.time(), pascals_id])  # folgt Pascal

    sebastian.write(["bacnet/following", time.time(), phillips_id])  # folgt Phillip
    sebastian.write(["bacnet/following", time.time(), pascals_id])  # folgt Pascal

    aline.write(["bacnet/following", time.time(), yasmins_id])  # folgt Yasmin
    aline.write(["bacnet/following", time.time(), georgias_id])  # folgt Georgia
    aline.write(["bacnet/following", time.time(), henrys_id])  # folgt Henry

    julius.write(["bacnet/following", time.time(), alines_id])  # folgt Aline
    julius.write(["bacnet/following", time.time(), bens_id])  # folgt Ben

    ben.write(["bacnet/following", time.time(), alines_id])  # folgt Aline
    ben.write(["bacnet/following", time.time(), veras_id])  # folgt Vera
    ben.write(["bacnet/following", time.time(), esthers_id])  # folgt Esther
    ben.write(["bacnet/following", time.time(), yasmins_id])  # folgt Yasmin


