import os
import shutil
import sys

execfile('functions.py')

revealed = []
# Function definitions

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