
__author__="Leonidus"
__date__ ="$6 Oct, 2010 1:32:07 AM$"

import anydbm
#epaths=dict()
epaths = anydbm.open("allPaths.db", "c")
tran=anydbm.open("transaction.db", "c")
searchC=anydbm.open("currDirList.db","c")

def findPath(ext,srcpath):
    #print epaths
    if ext in epaths:
        return epaths[ext]
    else:
        return srcpath


def chDict(key,val):
    #print epaths
    if key in epaths:
        epaths[key]=val
        return 1
    else:
        epaths[key]=val
        return 0

def originalPath(fullOPath,Dpath):
    tran[fullOPath]=Dpath

def forSearch(fName,currDir):
    searchC[fName]=currDir

def searchThis(fName):
    if fName in searchC:
        return searchC[fName]
    else:
        return "Not Found!"


