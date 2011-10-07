#!/usr/bin/python
#mc-nbt-edit 0.1 by sakisds <sakisds@gmx.com>
#Uses the NBT library by Thomas Woolford <woolford.thomas@gmail.com>
#Based on the NBT specifications by Markus Persson

from nbt import *
import sys

def help(): #Prints help
		print "mc-nbt-edit by sakisds <sakisds@gmx.com>\n\nUsage: mc-nbt-edit file tag datatype value\n"
		print "File: level.dat, usually inside .minecraft/saves/[mapname]\nTag: Tag to edit, possible values are GameType and hardcore"
		print "Value: 1 for true, 0 for false. For GameType it's 1 for Creative and 0 for Survival.\n\n\nOptions:"
		print "--print: Prints the contents of the file and exits\n--help: Displays this message."
		exit()

def complain(): #Complains on wrong options.
	print "Invalid options. Try --help."
	exit(1)

def loadfile(filepath): #Loads the NBT file
	try:
		return NBTFile(filepath,'rb')
	except Exception:
		print "Could not open file "+sys.argv[1]
		exit(1)

def savefile(nbt):
	try:
		nbt.write_file()
	except Exception:
		print "Could not save buffer to disk. Chances are discarded."
		exit(1)

def settag(name, dtype, value): #Sets wanted tag
	if dtype == "byte":
		tag= TAG_Byte(name)
		tag.value = int(value)
	elif dtype == "int":
		tag = TAG_Int(name)
		tag.value = int(value)
	elif dtype == "float":
		tag = TAG_Float(name)
		tag.value = float(value)
	elif dtype == "long":
		tag = TAG_Long(name)
		tag.value = long(value)
	elif dtype == "string":
		tag = TAG_String(name)
		tag.value = value
	elif dtype == "short":
		tag = TAG_Short(name)
		tag.value = int(value)
	elif dtype == "double":
		tag = TAG_Double(sys.argv)
		tag.value = float(value)
	else:
		print "Unknown tag data type. "
		exit()
	tag.name = name
	return tag

#Decide about printing help or complaining
if len(sys.argv) == 1 :
	help()
elif len(sys.argv) == 2:
	if sys.argv[1] == "--help":
		help()
	else:
		complain()
elif len(sys.argv) == 3:
	complain()

#Load file
nbt = loadfile(sys.argv[1])

#Parse tag
path = sys.argv[2].split('.')

#Do the editing
if len(path) == 1:
	tag = settag(path[0], sys.argv[3], sys.argv[4])
	nbt.__setitem__(path[0], tag)
elif len(path) == 2:
	compound = nbt.__getitem__(path[0])
	tag = settag(path[1], sys.argv[3], sys.argv[4])
	compound.__setitem__(path[1], tag)
elif len(path) == 3:
	compound = nbt.__getitem__(path[0])
	subcompound = compound.__getitem__(path[1])
	tag = settag(path[2], sys.argv[3], sys.argv[4])
	subcompound.__setitem__(path[2], tag)

#Save changes to disk
savefile(nbt)
