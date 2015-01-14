import os
import shutil
import sys

revealed = []
# Function definitions
def getTile(img):
	h = img.getH()
	w = img.getW()
	x = img.getTarget().getX()
	y = img.getTarget().getY()
	return capture(x-w/2,y-h/2,w,h)
def clickPairs(tiles,pairs,unclearedtile):
	clicked=0
	for p in pairs:
		t0 = tiles[p[0]]
		t1 = tiles[p[1]]
		#t0.waitVanish(t0,0.5)
		click(t0)
		clicked +=1
		#t1.waitVanish(t1,0.5)
		click(t1)
		clicked +=1
	print clicked, len(tiles) 

def makeGrid(region,tile):
	kikoIter = region.findAll(tile)
	kikoList = sorted(list(kikoIter), key=lambda t: t.getTarget().getY())
	firstRowY = kikoList[0].getTarget().getY()
	firstRow = filter(lambda t: t.getTarget().getY() == firstRowY, kikoList)
	totalTiles = len(kikoList)
	columns = len(firstRow)
	#if totalTiles % columns != 0:
		#popup("Warning! The column count does not evenly divide into the total tile count!")
	return kikoList

def revealTiles(tiles):
	print len(tiles)
	revealed = []
	#for t in tiles:
		#t.onChange()
		#t.waitVanish(t,0.5)
		#click(t)
		#hover(t)
		#revealed.append(getTile(t))
	for ti in range(len(tiles)):
		#t.onChange()
		#t.waitVanish(t,0.5)
		click(tiles[ti])
		hover(tiles[(ti+1)%len(tiles)])
		revealed.append(getTile(tiles[ti]))
	#popup(str(revealed[0]))
	print revealed
	return revealed

def findPairs(revealed):
	matched = [0 for x in range(len(revealed))]
	pairs = []
	ci=0
	while ci < len(revealed):
		ct = revealed[ci]
		ctf = Finder(ct)
		for t in range(ci+1,len(revealed)):
			matches = ctf.find(revealed[t])
			if ctf.hasNext() and matched[ci]==0 and matched[t]==0:
				matched[ci]=1
				matched[t]=1
				pairs.append([ci,t])
				break
		#ctf.destroy()
		ci+=1
	print pairs
	return pairs

def solve(img,level):
	# First determine grid
	pass

# Script
Settings.MoveMouseDelay = 0.4
Settings.MinSimilarity = 0.8

#tmpimgs = "tmpimgs"
#if not os.path.exists(tmpimgs):
#    os.makedirs(tmpimgs)

kikoRegion = selectRegion("Select the region in which the tiles will appear.")
if kikoRegion == None:
	print "A region was not selected. Exiting."
	sys.exit()
kikoTile = capture("Select a tile.")
if kikoRegion == None:
	print "A region was not selected. Exiting."
	sys.exit()

#kikoRegion.onChange()
click(kikoRegion)
hover(kikoRegion)
#onChangeFlag = False
#while onChangeFlag:
#	pass
kikoList = makeGrid(kikoRegion,kikoTile)
revealed = revealTiles(kikoList)
pairs = findPairs(revealed)
clickPairs(kikoList,pairs,kikoTile)

#if os.path.exists(tmpimgs):
#	shutil.rmtree(tmpimgs)