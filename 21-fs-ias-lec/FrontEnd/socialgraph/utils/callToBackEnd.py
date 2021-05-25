import os
import pathlib

from BackEnd.main import main
from BackEnd.writeToFeed import updateDirectoriesOnFollow

def followCall(rootUserName, followID):
    updateDirectoriesOnFollow(rootUserName, followID)
    main()

if __name__ =="__main__":
    a = pathlib.Path(__file__).absolute()
    print(a)