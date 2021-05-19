from generateDirectories import generateDirectories
from Person import Person
from generateJson import generateJson
import os

def main():
    # dummy Feeds erstellen
    generateDirectories()
    Persons = {}
    persList = []

    # TODO: über alle Ordner in Data iterieren und Personen erstellen
    rootdir = "./data"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".pcap"):  # BACnet
                print(os.path.join(subdir, file))
                # TODO read feed-Id and name from feed
                #name =
                #id =
                #Persons[name] = Person.Person(feed.id, feed.name, feed)

    # List of all persons in local database
    for person in Persons.values():
        person.printFollowList()
        persList.append(person)

    '''
    # TODO: Das da in main (oder gar ned nötig will wird durch gui usglöst)
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
    '''

    # Takes a list of all Persons and the Person we are as arguments
    # generateJson(persList, Persons['vera'])

if __name__ == "__main__":
    main()
