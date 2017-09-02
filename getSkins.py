import sys
import os
import time
from io import BytesIO
from PIL import Image
import requests

args = sys.argv[1:]

def processSkin(skinHash, sType, path):
    imageName = skinHash+".png"
    savePath = os.path.join(path, imageName)
    url = "https://mcskinsearch.com/texture/skin/"+skinHash+".png"
    req = requests.get(url)
    img = BytesIO(req.content)
    try:
        global imgIn
        imgIn = Image.open(img)
    except:
        print("Image failed... Hash: "+skinHash)

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

def getSkins(page, sType, path):
    url = "https://mcskinsearch.com/api/getUsers/"+str(page)
    req = requests.get(url)
    jreq = req.json()
    reqList = jreq['list']
    for i in range(0, 20):
         processSkin(reqList[i]['skinHash'], sType, path)
    print("Page done.")

print("Checking if path exist...")
currDir = os.path.dirname(__file__)
saveDir = os.path.join(currDir, args[2])
if os.path.exists(saveDir):
    print("Folder exist!")
else:
    print("Folder doesn't exist... Creating...")
    os.makedirs(saveDir)
skinReq = int(args[0]) // 20
print("Will get "+str(skinReq)+" pages.")
for i in range(0, skinReq):
    print("Downloading page: "+str(i+1))
    getSkins(i+1, args[1], saveDir)
    time.sleep(1)
print("All done!")
