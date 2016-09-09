#!/usr/bin/python


import os, commands, argparse, uuid, sys, subprocess, errno, shutil, time
from helper import *
from myUtil import *
from myInst import *

parser = argparse.ArgumentParser(description='Apply given aspect to a given Android APK')
parser.add_argument('apks', metavar='a', type=str, help='the location of the app to hack')
parser.add_argument('templateLocation', metavar='t', type=str, help='the location of the aspect template (a sample is provided in aspects/logger.aj')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action="store_true")
args = parser.parse_args()
    
def main():
	templateLocation = os.path.abspath(args.templateLocation)
	#apkLocation = os.path.abspath(args.apkLocation)
	act, pkg =getInfo (apkLocation)
	if (act !='' or pkg !=''):
		mainPath = os.getcwd()
		apkLocation2 = copyApk2(mainPath, apkLocation)
		apkName= apkLocation2[apkLocation2.rfind("/")+1:]
		ajFile= templateLocation[templateLocation.rfind("/")+1:]
		newTemplate = mainPath+'/AppLocation/'+ajFile
		pkgLogger (templateLocation, pkg,newTemplate )
		prepareDirectory(mainPath)
		checkPathExecutables()
		checkLibraries(mainPath)
		createSourceFile(newTemplate)
		#verbosePrint('[...] Decompiling apk')
		decompileAPK(apkLocation2, mainPath)
		dirs=os.listdir(mainPath+"/work/src")
		# verbosePrint('[-] Excluding libs from logging')
		# copyDexLib(mainPath, dirs, "./work/src/", " ./output")
		#verbosePrint('[-] Instrumenting Logger')
		runAJC(mainPath+'/config/ajc.properties',getAJCClasspath() , mainPath+'/work/source.lst')
		g = open(mainPath+"/myLog", "r")
		#if "[error]" in g.read():
			#g = open("./myLog", "r")
			#print ' '.join([m for m in g.readlines() if "when weaving type" in m])
			#buf.append(apkName+":AJC Error")
		#else:
			#verbosePrint('[-] Copying AspectJ Lib')
		#copyAJT(mainPath)
			#verbosePrint('[-] Recopying Excluded Libs')
			#copyDexLib(mainPath, dirs, "./output/", " output/out/")
			#verbosePrint('[-] Jar files')
		jarOut(mainPath)
		callProguard()
			#verbosePrint('[-] Generating dex from jar..')
		#sys.exit(0);
		generateDexFromJar(mainPath)
			#verbosePrint('[-] Replacing dex file..')
		replaceDexFile(apkLocation2)
			#verbosePrint('[-] Signing apk..')
		signAPK(apkLocation2)
		os.chdir(mainPath)
		if os.path.isfile(mainPath+'/classes.dex'):
			command = "cp "+apkLocation2+"-signed.apk " +mainPath+"/database/"
			print command
			#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
			#output = process.communicate()[0]
			os.system(command +' > /dev/null')
			print 'done copy'
			newPath=os.path.abspath(mainPath+"/database/"+apkName+"-signed.apk")
			buf.append(newPath+";Apphack Completed:PKG;"+pkg+":MAINACT;"+act)
			os.remove(mainPath+"/classes.dex")
		else:
			buf.append(apkName+":Error in Repackaging")
	try:
		shutil.rmtree(mainPath+"/output/")
		shutil.rmtree(mainPath+"/work/")
		shutil.rmtree(mainPath+"/AppLocation/")
		os.remove(mainPath+"/myLog")
	except:
		print ("ref main b4 assignment")

if __name__=="__main__":
	buf=[]
	apks = os.path.abspath(args.apks)
	start_time = time.time()
	if apks.endswith(".apk"):
		apkLocation =apks
		main()
		end_time = time.time()
		print("total time taken "+ apks, end_time - start_time)
	else:
		for root, dirs, files in os.walk(apks):
			for name in files:
				start_time = time.time()
				if name.endswith('.apk') and not name.startswith('.'):
					apkLocation = os.path.abspath(os.path.join(root, name))
					main()
					end_time = time.time()
					print("total time taken "+ name, end_time - start_time)
	print '\n'.join(buf)
