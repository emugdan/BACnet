import sys

# add the lib to the module folder
sys.path.append("lib")

import os
import crypto
import feed
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

    return myFeed


def generateDirectories():
    yasmin = generate("yasmin")
    esther = generate("esther")
    vera = generate("vera")
    pascal = generate("pascal")
    phillip = generate("phillip")
    sebastian = generate("sebastian")
    aline = generate("aline")
    ben = generate("ben")
    caroline = generate("caronline")
    david = generate("david")
    eveline = generate("eveline")
    fitzgerald = generate("fitzgerald")
    georgia = generate("georgia")
    henry = generate("henry")
    isabelle = generate("isabelle")
    julius = generate("julius")
    veri = generate("veri")

    yasmin.write(["bacnet/following", time.time(), 'f72f625b778fb17a']) # folgt Vera
    yasmin.write(["bacnet/following", time.time(), 'ab44472d7d630eeb']) # folgt Esther
    yasmin.write(["bacnet/following", time.time(), '7a87c429f64bc698']) # folgt Julius

    vera.write(["bacnet/following", time.time(), 'ab44472d7d630eeb'])  # folgt Esther
    vera.write(["bacnet/following", time.time(), '538c0e7c437376a8'])  # folgt Yasmin
    vera.write(["bacnet/following", time.time(), '8142d31c996c2c12'])  # folgt Sebastian
    vera.write(["bacnet/following", time.time(), 'cffc82fc8d272164'])  # folgt Pascal
    vera.write(["bacnet/following", time.time(), '45bdfbfede5d0973'])  # folgt Phillip

    esther.write(["bacnet/following", time.time(), '538c0e7c437376a8'])  # folgt Yasmin
    esther.write(["bacnet/following", time.time(), 'f72f625b778fb17a']) # folgt Vera
    esther.write(["bacnet/following", time.time(), '2d06f5f5cab6ae2a'])  # folgt David

    pascal.write(["bacnet/following", time.time(), '8142d31c996c2c12'])  # folgt Sebastian
    pascal.write(["bacnet/following", time.time(), '45bdfbfede5d0973'])  # folgt Phillip

    phillip.write(["bacnet/following", time.time(), '8142d31c996c2c12'])  # folgt Sebastian
    phillip.write(["bacnet/following", time.time(), 'cffc82fc8d272164'])  # folgt Pascal

    sebastian.write(["bacnet/following", time.time(), '45bdfbfede5d0973'])  # folgt Phillip
    sebastian.write(["bacnet/following", time.time(), 'cffc82fc8d272164'])  # folgt Pascal

    aline.write(["bacnet/following", time.time(), '538c0e7c437376a8'])  # folgt Yasmin
    aline.write(["bacnet/following", time.time(), '9c7fee9731d01193'])  # folgt Georgia
    aline.write(["bacnet/following", time.time(), '917a951a80a2d601'])  # folgt Henry

    julius.write(["bacnet/following", time.time(), 'd35f7b7f8e94abc2'])  # folgt Aline
    julius.write(["bacnet/following", time.time(), '9ec9eef4394169a0'])  # folgt Ben

    ben.write(["bacnet/following", time.time(), 'd35f7b7f8e94abc2'])  # folgt Aline
    ben.write(["bacnet/following", time.time(), 'f72f625b778fb17a'])  # folgt Vera
    ben.write(["bacnet/following", time.time(), 'ab44472d7d630eeb'])  # folgt Esther
    ben.write(["bacnet/following", time.time(), '538c0e7c437376a8'])  # folgt Yasmin
