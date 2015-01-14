import os
import shutil
import sys
import time

idir = os.path.dirname(os.path.realpath(sys.argv[0]))
execfile(idir+'/kikomatch.sikuli/functions.py')

# Script
Settings.MoveMouseDelay = 0.2
Settings.MinSimilarity = 0.75

# User-defined regions
kikoRegion = selectRegion("Select the region in which the tiles will appear.")
if kikoRegion == None:
	print "A region was not selected. Exiting."
	sys.exit()
kikoTile = capture("Select a tile.")
if kikoRegion == None:
	print "A region was not selected. Exiting."
	sys.exit()



#Test block
#kikoIter = kikoRegion.findAll(kikoTile)
#kikoList = sorted(list(kikoIter), key=lambda t: t.getTarget().getY())
#print len(kikoList)



click(kikoRegion)
time.sleep(0.5)
kikoList = makeGrid(kikoRegion,kikoTile)
revealed = revealTiles(kikoList)
pairs = findPairs(revealed)
clickPairs(kikoList,pairs,kikoTile)
