#!/usr/bin/python

import os, argparse, subprocess

def getInfo2 (apkLocation2):
	print apkLocation2
	command = "aapt dump permissions "+apkLocation2
	process =subprocess.Popen(command.split(),stdout=subprocess.PIPE)
	out = process.communicate()[0]
	print out
	if ("CONTACTS" in out):
		ret = "Yes"
	else:
		ret =  "No"
	#y=open("aapt.xml", "r")
	#z=out.split("\n")
	#z=y.readlines()
	#activity=[i for i in z if i.startswith("launchable-activity")][0]
	#package=[i for i in z if i.startswith("package")][0] 
	#act=activity[activity.index("name='")+6:activity.index("' ")]
	#pkg=package[package.index("name='")+6:package.index("' ")]
	#topdir = pkg[:pkg.index(".")]
	#os.remove("aapt.xml")
	#return act, pkg
	return ret
#apks = os.path.abspath(args.apks)
#ret = getInfo(args.apks)
#print act
#print pkg
