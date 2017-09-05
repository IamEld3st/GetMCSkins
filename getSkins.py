import sys
import os
import time
from io import BytesIO
from PIL import Image
import requests
from ratelimit import rate_limited
import base64
import json

args = sys.argv[1:]

def getList(page):
    url = "https://mcskinsearch.com/api/getUsers/"+str(page)
    return requests.get(url)

def getUUIDs(usernameList):
    print("Getting UUIDs for "+str(len(usernameList))+" players...")
    req = requests.post("https://api.mojang.com/profiles/minecraft", json=usernameList)
    res = req.json()
    print(len(res))
    uuidList = []
    for i in range(0,len(res)):
        uuidList.append(res[i]['id'])
    print("Got UUIDs for "+str(len(uuidList))+" players!")
    return uuidList

def getSkinUrl(uuid):
    reqOK = False
    while reqOK == False:
        global userRaw
        userRaw = requests.get("https://api.4lex.de/skin/"+uuid)
        if userRaw.status_code == 200:
            reqOK = True
    userJson = userRaw.json()
    decodedRes = json.loads(base64.b64decode(userJson['properties'][0]['value']))
    return decodedRes['textures']['SKIN']['url']

@rate_limited(1)
def processSkin(uuid, sType, path):
    imageName = uuid+".png"
    savePath = os.path.join(path, imageName)
    skinUrl = getSkinUrl(uuid)
    req = requests.get(skinUrl)
    img = BytesIO(req.content)
    try:
        imgIn = Image.open(img)
        w, h = imgIn.size
        if sType == "0":
            if h == 32:
                imgOut = Image.new("RGBA", (64, 64))
                imgOut.paste(imgIn, (0, 0, 64, 32))
                rl = imgIn.crop((0, 16, 16, 32))
                imgOut.paste(rl, (16, 48, 32, 64))
                ra = imgIn.crop((40, 16, 56, 32))
                imgOut.paste(ra, (32, 48, 48, 64))
                imgOut.save(savePath)
            else:
                imgIn.save(savePath)
        if sType == "1":
            if h == w:
                imgOut = Image.new("RGBA", (64, 32))
                box = (0, 0, 64, 32)
                imgOut.paste(imgIn.crop(box), box)
                imgOut.save(savePath)
            else:
                imgIn.save(savePath)
    except:
        print("Image failed... UUID: "+uuid)

@rate_limited(1)
def getUsernames(offset):
    print("Attempting to get 20 usernames...")
    responseList = []
    gotOKResponse = False
    page = offset+1
    while gotOKResponse == False:
        global req
        req = getList(page)
        if req.status_code == 200:
            gotOKResponse = True
    jreq = req.json()
    reqList = jreq['list']
    for i in range(0, 20):
        responseList.append(reqList[i]['username'])
    print("Got "+str(len(responseList))+" usernames!")
    return responseList

def checkDirectory(path):
    print("Checking if path exist...")
    currDir = os.path.dirname(__file__)
    saveDir = os.path.join(currDir, path)
    if os.path.exists(saveDir):
        print("Folder exist!")
    else:
        print("Folder doesn't exist... Creating...")
        os.makedirs(saveDir)
    return saveDir

savePath = checkDirectory(args[2])
skinReq = int(args[0]) // 20
progress = 0
startOffset = int(args[3])
for i in range(0, skinReq):
    uuidList = getUUIDs(getUsernames(i))
    for x in range(0, len(uuidList)):
        y = x + startOffset
        processSkin(uuidList[x], args[1], savePath)
        if ((x+1) % 10) == 0:
            progress += 10
            if x != 0:
                print("Progress: "+str(progress)+"/"+args[0])

print("All done!")
