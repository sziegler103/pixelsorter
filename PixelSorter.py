from PIL import Image
import random

def getRGBVal(x, y, pixData):
	r, g, b = pixData[x, y]
	return r + g + b

img = Image.open("tree.jpg")
img = img.convert("RGB")
maxSize = 512
saveEveryYLines = 10

# ---from https://stackoverflow.com/questions/24745857/python-pillow-how-to-scale-an-image---
if img.width > maxSize or img.height > maxSize:
    if img.height > img.width:
        factor = maxSize / img.height
    else:
        factor = maxSize / img.width
    img = img.resize((int(img.width * factor), int(img.height * factor)))
# -------------------------------------------------------------------------------------------

pixData = img.load()

curPixPos = (0, 0)
probePos = (0, 0)
bufferPix = (0, 0, 0)

for y in range(int(img.height)):
	y1 = y # used for noncomplete sorts
	for x in range(img.width): # curPix goes linearly from left to right
		
		curPixPos = (x, y1)
		curMaxPos = curPixPos
		for i in range(img.width - x): # probe scans every pixel on the line besides ones already passed
			probePos = (i + x, y1)
			if getRGBVal(probePos[0], probePos[1], pixData) > getRGBVal(curMaxPos[0], curMaxPos[1], pixData): # if probe RGBval > curMax val, set max to that
				curMaxPos = probePos
		bufferPix = pixData[curPixPos] # Then, set current pix to the max val we found, securing that pixel as THE highest val on the row
		pixData[curPixPos] = pixData[curMaxPos]
		pixData[curMaxPos] = bufferPix
	if (y1 % saveEveryYLines) == 0:
		img.save("GeneratedImage.bmp")
				

img.save("GeneratedImage.bmp")
img.close()

print("Complete")