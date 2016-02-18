import pyautogui
from time import sleep
import sys

def colorMatch(rgb1,rgb2,tolerance):
	match = True
	for i in range(3):
		aboveMin = rgb1[i] >= rgb2[i]-tolerance
		belowMax = rgb1[i] <= rgb2[i]+tolerance
		if not (aboveMin and belowMax): 
			match = False
			break;
	return match

def greenMatch(px,py,image):
	rgb1 = (96, 153, 33)
	tol = 20 #rgb color tolerance
	rgb2 = image.getpixel((px,py))
	return colorMatch(rgb1,rgb2,tol)
	# return pyautogui.pixelMatchesColor(px,py,rgb,tol)

def orangeMatch(px,py,image):
	rgb1 = (246, 168, 8)
	tol = 20 #rgb color tolerance
	rgb2 = image.getpixel((px,py))
	return colorMatch(rgb1,rgb2,tol)


def findGameArea(topLeftCornerImage):
	"""
	Returns the coordinates of the top left corner of the game area.
	Finding this reduces the search time considerably.
	"""
	tlc = pyautogui.locateOnScreen(topLeftCornerImage)
	if tlc==None:
		print "Top left corner of game screen not found! Exiting."
		sys.exit()
	else:
		#print "Top left corner found at:",tlc[0],tlc[1]
		pyautogui.moveTo(tlc[0],tlc[1])
		#print pyautogui.pixel(tlc[0],tlc[1])
		return tlc

def findTilePixel(start,color,screenshot,backtrack):
	"""
	Find the tile pixel from a start pixel (px,py)
	color is enumerated to colors of the tile.
	screenshot is an image of the game board.
	backtrack is a boolean. if true, the lowest color-matched x is found.
	"""
	if color=="green":
		matchFunction = greenMatch
		increments = 0#5
		stride = 10
		dy = 150
	elif color=="orange":
		matchFunction = orangeMatch
		increments = 0
		stride = 1
		dy = 150
	elif color=="green2":
		matchFunction = greenMatch
		increments = 0
		stride = 1
		dy = 300
	else:
		print "Color match function not available! Exiting."
		sys.exit()

	first = [-1,-1]
	for py in range(start[1],start[1]+dy):
		for px in range(start[0],start[0]+stride*increments+1,stride):
			pyautogui.moveTo(px,py)
			if matchFunction(px,py,screenshot):
				#print color,"match found at:",px,py," color:",screenshot.getpixel((px,py))
				first = [px,py]
				break;
		if first[0]>=0:
			break;

	ret = [first[0],first[1]]

	if backtrack:
		while matchFunction(ret[0]-1,ret[1],screenshot):
			pyautogui.moveTo(ret[0],ret[1])
			ret[0]-=1

	if ret[0]<0:
		print "The first",color,"pixel was not found! Exiting."
		sys.exit()
	else:
		#print "The first",color,"pixel was found at:",first[0],first[1]
		pyautogui.moveTo(ret[0],ret[1])
		return ret

# BEGIN AUTO SOLVER
print "Starting the auto-solver."
print "Do not move the game screen and make sure it is all visible!"
tlc = findGameArea('topLeftCorner.png')

screenshot = pyautogui.screenshot() # first record the image.

greenStart = [tlc[0],tlc[1]]
greenStart[0]+=120
greenStart[1]+=37
firstGreen = findTilePixel(greenStart,"green",screenshot,True)
orangeStart = [-1,-1]
orangeStart[0] = firstGreen[0]+10
orangeStart[1] = firstGreen[1]
firstOrange = findTilePixel(orangeStart,"orange",screenshot,True)
borderHeight = firstOrange[1]-firstGreen[1]+1
greenStart[0] = firstOrange[0]
greenStart[1] = firstOrange[1]+borderHeight*9
secondGreen = findTilePixel(greenStart,"green2",screenshot,False)

# COMPUTE THE TILE SIZE
#print "firstOrange y, secondGreen y",firstOrange[1],secondGreen[1]
innerHeight = secondGreen[1]-firstOrange[1]+1
#print "Border height, inner height:",borderHeight,innerHeight
tileSize = borderHeight*2+innerHeight
#print "Tile size:",tileSize

firstTileCenter = [-1,-1]
firstTileCenter[0]=secondGreen[0]+innerHeight/2
firstTileCenter[1]=secondGreen[1]-innerHeight/2
pyautogui.moveTo(firstTileCenter[0],firstTileCenter[1])

# DETERMINE GRID DIMENSIONS
vcenter = [secondGreen[0],secondGreen[1]-innerHeight/2]
pyautogui.moveTo(vcenter[0],vcenter[1])
hcenter = [firstGreen[0]+innerHeight/2,firstGreen[1]+borderHeight+2]
pyautogui.moveTo(hcenter[0],hcenter[1])

rows = 1
while orangeMatch(vcenter[0],vcenter[1]+rows*tileSize,screenshot):
	rows+=1

cols = 1
while orangeMatch(hcenter[0]+cols*tileSize,hcenter[1],screenshot):
	cols+=1

print "Grid dimension (row x col):",rows,cols

#DETERMINE CLICK / PROBE LOCATIONS
def init2d(rows,cols):
	mat = []
	for r in range(rows):
		mat.append([])
		for c in range(cols):
			mat[r].append(cols)
	return mat

backgrounds = init2d(rows,cols)
colors = init2d(rows,cols)

bgstart = (firstOrange[0]+cols,firstOrange[1]+rows)
colorOffset = (tileSize/2,tileSize/2)
for r in range(rows):
	for c in range(cols):
		bgx = bgstart[0]+c*tileSize
		bgy = bgstart[1]+r*tileSize
		backgrounds[r][c] = (bgx,bgy)
		colors[r][c] = (bgx+colorOffset[0],bgy+colorOffset[1])

# START THE GAME!
#pyautogui.click()