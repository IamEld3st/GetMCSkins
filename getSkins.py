import sys
import os
import time
from io import BytesIO
from PIL import Image
import requests

args = sys.argv[1:]
convStat = 0

def getFullList(skinCount):
    print("Getting list of ", skinCount, " skins...")
    skinList = []
    term = 0
    if (int(skinCount) % 21) > 0:
        pagesNeeded = (int(skinCount) // 21) + 1
    else:
        pagesNeeded = int(skinCount) // 21
    for x in range(0, pagesNeeded):
        if term == 1:
            break
        if (x % 10) == 0:
            time.sleep(0)
        url = "https://mcskinsearch.com/api/getUsers/"+str(x+1)
        req = requests.get(url)
        jreq = req.json()
        reqList = jreq['list']
        for i in range(0, 21):
            skinList.append(reqList[i]['skinHash'])
            if len(skinList) == int(skinCount):
                print("Got ", len(skinList)," skins terminating loop...")
                term = 1
                break
    print("Loop terminated!")
    return skinList

def processSkin(skinHash, sType, path):
    imageName = skinHash+".png"
    savePath = os.path.join(path, imageName)
    url = "https://mcskinsearch.com/texture/skin/"+skinHash+".png"
    req = requests.get(url)
    imgIn = Image.open(BytesIO(req.content))
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
            return 1
        else:
            imgIn.save(savePath)
            return 0
    if sType == "1":
        if h == w:
            imgOut = Image.new("RGBA", (64, 32))
            box = (0, 0, 64, 32)
            imgOut.paste(imgIn.crop(box), box)
            imgOut.save(savePath)
            return 1
        else:
            imgIn.save(savePath)
            return 0

progress = -10
sList = getFullList(args[0])
print("Checking if path exist...")
currDir = os.path.dirname(__file__)
saveDir = os.path.join(currDir, args[2])
if os.path.exists(saveDir):
    print("Folder exist!")
else:
    print("Folder doesn't exist... Creating...")
    os.makedirs(saveDir)
print("Starting download of all skins...")
for y in range(0,len(sList)):
    convStat += processSkin(sList[y], args[1], saveDir)
    if (y % 10) == 0:
        progress += 10
        print("Progress: ", progress, "/", args[0])
        time.sleep(1)
print("Downloaded all skins!\nConverted ",convStat)
