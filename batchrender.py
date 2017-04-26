
import os
import subprocess
import shutil

import Tkinter
from Tkinter import *
import tkMessageBox
import ttk

########################################
######### Render Application ###########
########### By: Erin Terre #############
############## Version 1 ###############
########################################

def setup(*args):
	
	## setup your variables based on user input
	sourceFolder = str(source.get())
	package = '/' + str(pack.get())
	desFolder = str(dest.get())
	sec = int(seconds.get())

	## get camera checkbox values
	checkboxes = [camera1.get(), camera2.get(), camera3.get(), camera4.get(), camera5.get(), camera6.get()]
	cameras = ['1_front', '2_right', '3_back', '4_left', '5_top', '6_bottom']

	## see which cameras were checked and run camRender for them
	for i in range(0,6):
		if checkboxes[i] == 1:
			camName = cameras[i]
			print camName
			camRender(sourceFolder, desFolder, package, sec, cameras[i])

	## display a popup when all rendering && sorting is complete
	tkMessageBox.showinfo('Completed', 'Rendering and sorting complete!')

def camRender(sourceFolder, desFolder, package, sec, camName):

	## set the path for your destination folder
	## check if the destination folder exists && make it 
	camPath = desFolder + '/' + camName
	if not os.path.exists(camPath):
		os.makedirs(camPath)

	## if seconds is greater than 0 run subprocess with seconds 
	if(sec == 0):
		subprocess.call('%s%s.exe %s -benchmark -dumpmovie -resx=1024 -resy=1024' %(sourceFolder, package, camName))
	else: 
		subprocess.call('%s%s.exe %s -benchmark -dumpmovie -resx=1024 -resy=1024 -seconds=%d' %(sourceFolder, package, camName, sec))
	
	print 'done'

	moveFiles(sourceFolder, package, camName, camPath)

def moveFiles(sourceFolder, package, camName, camPath):

	## create path for image location
	src = sourceFolder + package + '/Saved/Screenshots/WindowsNoEditor/'

	## make a list of the files in src && sort them
	srcFiles = os.listdir(src)
	srcFiles.sort()
	count = 1

	## for each file create your old/new file path
	## move and rename each file
	for fileName in srcFiles:
		oldFilePath = os.path.join(src, fileName)
		newFilePath = camPath + '/' + camName + '_' + str(count).zfill(5) + '.png'
		count = count + 1

		if(os.path.isfile(oldFilePath)):
			shutil.move(oldFilePath, newFilePath)


## create the ui
root = Tk()
root.title("Batch Render Program")

mainframe = ttk.Frame(root, padding="5 5 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

## package ui 
pack = StringVar()
ttk.Label(mainframe, text="Package Name:").grid(column=1, row=1, sticky=W)
packageEntry = ttk.Entry(mainframe, width=30, textvariable=pack)
packageEntry.grid(column=2, row=1, sticky=(W,E))

## source ui
source = StringVar()
ttk.Label(mainframe, text="Source Directory:").grid(column=1, row=2, sticky=W)
sourceDirectoryEntry = ttk.Entry(mainframe, width=30, textvariable=source)
sourceDirectoryEntry.grid(column=2, row=2, sticky=(W,E))

## destination ui
dest = StringVar()
ttk.Label(mainframe, text="Destination Directory:").grid(column=1, row=3, sticky=W)
destinationDirectoryEntry = ttk.Entry(mainframe, width=30, textvariable=dest)
destinationDirectoryEntry.grid(column=2, row=3, sticky=(W,E))

## seconds ui
seconds = StringVar()
seconds.set('0')
ttk.Label(mainframe, text="Seconds:").grid(column=1, row=4, sticky=W)
secondsEntry = ttk.Entry(mainframe, width=10, textvariable=seconds)
secondsEntry.grid(column=2, row=4, sticky=(W,E))

# camera checkboxes ui
camera1 = IntVar()
camera1.set(1)
Checkbutton(mainframe, text="1_front", variable=camera1).grid(column=1, row=5, sticky=(W,E))

camera2 = IntVar()
camera2.set(1)
Checkbutton(mainframe, text="2_right", variable=camera2).grid(column=2, row=5, sticky=(W,E))

camera3 = IntVar()
camera3.set(1)
Checkbutton(mainframe, text="3_back", variable=camera3).grid(column=1, row=6, sticky=(W,E))

camera4 = IntVar()
camera4.set(1)
Checkbutton(mainframe, text="4_left", variable=camera4).grid(column=2, row=6, sticky=(W,E))

camera5 = IntVar()
camera5.set(1)
Checkbutton(mainframe, text="5_top", variable=camera5).grid(column=1, row=7, sticky=(W,E))

camera6 = IntVar()
camera6.set(1)
Checkbutton(mainframe, text="6_bottom", variable=camera6).grid(column=2, row=7, sticky=(W,E))

## button ui
ttk.Button(mainframe, text="Render", command=setup).grid(column=2, row=8, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', setup)
root.mainloop()