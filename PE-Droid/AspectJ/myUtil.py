import os, commands, argparse, uuid, sys, subprocess, errno, shutil
# build AJC classpath
def getAJCClasspath():
    return './lib/aspectjrt.jar:./lib/aspectjweaver.jar:./lib/android.jar:./lib/maps.jar:./lib/amazon_home.jar:./lib/amazon_msg.jar:./lib/google-play-services.jar:./lib/google-play-services.jar:./lib/commons-lang3-3.4.jar:./lib/spring-core-2.5.6.jar:'+ getAndroidHome()
	#return './lib/aspectjrt.jar:./lib/aspectjweaver.jar:./lib/android_19.jar:./lib/android.jar:./lib/maps.jar:./lib/amazon_home.jar:./lib/amazon_msg.jar:./lib/google-play-services.jar:./lib/google-play-services.jar:./lib/commons-lang3-3.4.jar:./lib/spring-core-2.5.6.jar:'+ getAndroidHome()

# get Android home directory
def getAndroidHome():
    try:
      return '/home/aisha/Android/Android_1/sdk'
     # return os.environ['ANDROID_HOME']
    except KeyError as exception:
        print '[!] $ANDROID_HOME not defined! Please set to Android SDK directory'
        sys.exit(1)

# Ensure required libraries for AJC are present
def checkLibraries(mainPath):
    #if not os.path.exists('./lib/aspectjtools.jar'):
     #   print '[!] Library "aspectjtools.jar" not found in lib directory'
     #   sys.exit(1)
  #  if not os.path.exists('./lib/aspectjrt.jar'):
  #      print '[!] Library "aspectjrt.jar" not found in lib directory'
  #      sys.exit(1)
    if not os.path.exists(mainPath+'/lib/aspectjweaver.jar'):
        print '[!] Library "aspectjweaver.jar" not found in lib directory'
        sys.exit(1)
    if not os.path.exists(getAndroidHome() + '/platforms/android-19/android.jar'):
        print '[!] Library "android.jar" not found in Android home directory (looking for android-19.jar)'
        sys.exit(1)
    if not os.path.exists(mainPath+'/config/ajc.properties'):
        print '[!] Config "ajc.properties" not found in config directory'
        sys.exit(1)

# Create directories needed for AJC
def prepareDirectory(mainPath):
    createDirectory(mainPath+'/work/src')
    createDirectory(mainPath+'/output/')

# Try/except will avoid any race condition (OS-X related problem)
def createDirectory(directory):
    try: 
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def verbosePrint(*args):
    for arg in args:
        print arg,
    print
#else:
#    verbosePrint = lambda *a: None  # do nothing

def getInfo (apkLocation):
	command = '/var/www/html/PE-Droid/aapt dump badging '+apkLocation
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output = process.communicate()[0]
	z=output.split('\n')
	activities=[i for i in z if i.startswith("launchable-activity")]
	packages=[i for i in z if i.startswith("package")] 
	if activities:
		activity = activities[0]
		act=activity[activity.index("name='")+6:activity.index("' ")]
	else:
		act=""
	if packages:
		package = packages[0]
		pkg=package[package.index("name='")+6:package.index("' ")]
	else:
		pkg=""
	return act, pkg
	
def pkgLogger (templateLocation,pkg,newTemplate):
	outAJfile=open(templateLocation, "r")
	inAJfile = open(newTemplate, "w")
	for lines in outAJfile.readlines():
		inAJfile.write(lines.replace('static String Path = "data/data";', 'static String Path = "data/data/'+pkg+'";'))
	    
def copyApk2(mainPath, apkLocation):  
	apkName=os.path.basename(apkLocation)
	if not os.path.isdir("AppLocation"):
		os.makedirs(mainPath+"/AppLocation")
	apkLocation2 = mainPath+"/AppLocation/"+apkName
	command = "cp -f "+ apkLocation + " "+apkLocation2
	#verbosePrint(command)
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	return apkLocation2

def createSourceFile(filename):
    command = 'echo "{0}" > work/source.lst'.format(filename)
    #verbosePrint('[>] ' + command)
    commands.getoutput(command)

def cmd_exists(cmd):
	return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
def cmd_exists2(cmd):
	command = 'type ' + cmd
	process =subprocess.Popen(command.split(), shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output = process.communicate()[0]
	return process

def checkPathExecutables():
    if cmd_exists2('ajc') == False:
        print '[!] ajc was not found on path -- please put it there!'
        sys.exit(1)
    if cmd_exists2('d2j-jar2dex.sh') == False:
        print '[!] d2j tools not found on path -- please put the bin directory on your path!'
        sys.exit(1)
    if cmd_exists('zip') == False:
        print '[!] zip not found on path'
        sys.exit(1)

