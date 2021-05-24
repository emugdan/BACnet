import sys
import os
import crypto
import feed
import random
import time

firstnames = ["Mia", "Lara", "Emma", "Laura", "Anna", "Sara", "Lea", "Elena", "Lina", "Alina", "Julia", "Emilia",
              "Lena", "Nina", "Sophia", "Lia", "Elin", "Sophie", "Sofia", "Nora", "Jana", "Mila", "Elina", "Melina",
              "Livia", "Luana", "Giulia", "Emily", "Chiara", "Valentina", "Noemi", "Lorena", "Selina", "Alessia",
              "Hanna", "Ronja", "Lynn", "Lisa", "Ella", "Amelie", "Luisa", "Mara", "Sarah", "Elisa", "Jael", "Fiona",
              "Olivia", "Amelia", "Zoe", "Noah", "Liam", "Luca", "Gabriel", "Leon", "David", "Matteo", "Elias", "Louis",
              "Levin", "Samuel", "Julian", "Tim", "Jonas", "Robin", "Diego", "Nico", "Leo", "Jan", "Ben", "Leandro",
              "Dario", "Lukas", "Rafael", "Elia", "Nino", "Simon", "Lenny", "Gian", "Benjamin", "Alessio", "Fabio",
              "Finn", "Loris", "Aaron", "Daniel", "Lucas", "Livio", "Andrin", "Nevio", "Leonardo", "Alexander",
              "Nathan", "Lian", "Mattia", "Enzo", "Luis", "Joel", "Raphael"]

lastnames = ["Amsler", "Amstutz", "Andrist", "Andros", "Ankeney", "Ankeny", "Ankney", "Anliker", "Annen", "Arn",
             "Arner", "Arnet", "Bally", "Balthis", "Bandi", "Batliner", "Batz", "Batz", "Beachy", "Benziger",
             "Berlinger", "Berna", "Berna", "Berry", "Bertschy", "Bichsel", "Bieri", "Bryner", "Buchli", "Bullinger",
             "Buol", "Burckhalter", "Burgi", "Burgin", "Burgy", "Buri", "Burk", "Burkhalter", "Burri", "Burry", "Buser",
             "Bussinger", "Henggeler", "Herda", "Hilfiker", "Hilty", "Hirschi", "Hirschy", "Hochstedler", "Hochstetler",
             "Hoesly", "Hoffstetter", "Holdener", "Hopler", "Hostetler", "Hostetter", "Hum", "Hunkler", "Hunziker",
             "Hurliman", "Inabinett", "Inabnit", "Ingold", "Isch", "Iseli", "Isely", "Jacky", "Jaecks", "Jenni",
             "Jenny", "Jud", "Kadis", "Kamer", "Schudel", "Schurter", "Sprunger", "Stager", "Staheli", "Sterchi",
             "Stoecklin", "Struchen", "Stuessy", "Surbeck", "Tanner", "Theiler", "Thoeny", "Torian", "Treichel",
             "Treichler", "Tresch", "Tritten", "Trollinger", "Troxler", "Truby", "Trumpy", "Tschappat", "Tschoepe",
             "Tschopp", "Ummel", "Vetsch", "Walliser", "Wehrli", "Wehrly", "Weltner", "Welty", "Weyker", "Wiget",
             "Willan", "Winzenried", "Wirthlin", "Wurgler", "Wyss"]


def createRandomNames(size):
    names = []
    while len(names) < size:
        rf = firstnames[random.randint(0, len(firstnames)-1)]
        rl = lastnames[random.randint(0, len(lastnames)-1)]

        if rf + "_" + rl not in names:
            names.append(rf + "_" + rl)

    return names


def createDirectories(size, maxConnections):
    names = createRandomNames(size)
    persons = []

    for name in names:
        f, id = generate(name)
        persons.append([f, id])

    for person in persons:
        for i in range(random.randint(1, maxConnections)):
            tmp = random.randint(0, len(persons)-1)
            followPerson = persons[tmp]
            person[0].write((["bacnet/following", time.time(), followPerson[1]]))


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
