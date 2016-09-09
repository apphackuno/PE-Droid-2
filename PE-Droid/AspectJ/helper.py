import os, commands, argparse, uuid, sys, subprocess, errno, shutil
def decompileAPK(apkLocation2, mainPath):
	command = './dex2jar-0.0.9.15/d2j-dex2jar.sh {0} --force -o {1}/work/originalAPKAsJar.jar'.format(apkLocation2, mainPath)
	#verbosePrint('[>] ' + command)
	#print command
	#process = subprocess.Popen(command.split(), shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#output = process.communicate()[1]
	dex2Jar=os.system(command+' > /dev/null')
	print "done dex2jar"
	command = '/usr/bin/unzip -o {0}/work/originalAPKAsJar.jar -d {0}/work/src/'.format(mainPath)
	#verbosePrint('[>] ' + command)
	#process = subprocess.Popen(command.split(), shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#output = process.communicate()[1]
	dexZip=os.system(command +' > /dev/null')
	print "done unzip"
	
def signAPK(apkLocation2):
	command = './dex2jar-0.0.9.15/d2j-apk-sign.sh -f -o {0}-signed.apk {0}'.format(apkLocation2)
	#command = 'd2j-apk-sign.sh -f -o {0}-signed.apk {0}'.format(apkLocation2)
	#verbosePrint('[>] ' + command)
	#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	#output = process.communicate()[0]
	sign=os.system(command +' > /dev/null')
	print "done sign"

def replaceDexFile(apkLocation2):
    command = '/usr/bin/zip -r {0} classes.dex'.format(apkLocation2)
    #verbosePrint('[>] ' + command)
    #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #output = process.communicate()[0]
    dexZip=os.system(command +' > /dev/null')
    print "done replace"

def generateDexFromJar(mainPath):
    command = './dex2jar-0.0.9.15/d2j-jar2dex.sh -f -o classes.dex '+mainPath+'/output/output2.jar'
    #verbosePrint('[>] ' + command)
    #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #output = process.communicate()[0]
    #return 'classes.dex'
    jar2Dex=os.system(command +' > /dev/null')
    print "done jar2Dex"
    
def jarOut(mainPath):
	os.chdir(mainPath+"/output/out")
	command = "/usr/bin/jar cf "+ mainPath + "/output/output.jar ."
	#verbosePrint(command)
	#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	#output = process.communicate()[0]
	out=os.system(command +' > /dev/null')
	print "done jarOut"
	os.chdir(mainPath)
