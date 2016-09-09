import os, commands, argparse, uuid, sys, subprocess, errno, shutil
from myUtil import *
# ajc -Xlintfile:ajc.properties -cp $CLASSPATH -inpath $CLASSES_DIR -source 1.5 @source.lst -outjar $JAR_DIR/output.jar 
# Weave your results using the ajc compiler (must be on path)
def runAJC(config, classpath, sourcelist):
    checkPathExecutables()
    #command = "/var/www/html/PE-Droid/aspectj1.8/bin/ajc -g:none -proceedOnError -Xjoinpoints:arrayconstruction -Xlintfile:{0} -cp {1} -inpath ./work/src/ -source 1.8 AD-Aspects/LogService.java AD-Aspects/upLoadDex.java @{2} -d ./output/out -log myLog".format(config, classpath, sourcelist)
    command = "/var/www/html/PE-Droid/aspectj1.8/bin/ajc -g:none -proceedOnError -preserveAllLocals -verbose -Xlintfile:{0} -cp {1} -inpath work/src/ -source 1.8 @{2} -d output/out -log myLog".format(config, classpath, sourcelist)
    #verbosePrint(command)
    #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #output = process.communicate()[0]
    os.system(command +' > /dev/null')
    print 'done instrumentation'
    
def copyDexLib(mainPath, dirs, a, b):
	os.chdir(mainPath)
	apis=[i for i in dirs if i in ["android", "java", "javax", "dalvik"]]
	#apis =[]
	#apis=[i for i in dirs if i in ["android", "java", "org", "javax", "dalvik"]]
	#for i in dirs:
		#for j in ["com/google/android", "com/googlecode"]:
			#if i+"/" in j:
				#if j not in apis:
				#	apis.append(j)
	#[apis.append(i) for i in dirs if i in ["android"]]
	for j in apis:
		#command = "mkdir -p " + a +j + b+ "/"+j
		#os.system(command +' > /dev/null')
		#verbosePrint(command)
		#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		#output = process.communicate()[0]
		command = "/bin/mv -f " + a +j + b
		#command = "/bin/mv -f " + a +j + b+"/"+j
		os.system(command +' > /dev/null')
		print 'done copyDexLib'
def removeLogger(mainPath):
	os.chdir(mainPath)
	filelist = [ f for f in os.listdir("./output/out") if (f.startswith("Logger") or f.startswith("LogService") or f.startswith("upLoadDex") )]
	for x in filelist:
		os.remove(mainPath+"/output/out/"+x)
		#def removeLogger(mainPath):
	#os.chdir(mainPath)
	#filelist = [ f for f in os.listdir("./output/out") if (f.startswith("Logger") or f.startswith("LogService") or f.startswith("upLoadDex") )]
	#for x in filelist:
	#	print x
	#	os.
		#command = "/bin/rm -f "+mainPath+"/output/out/"+x
		#os.system(command +' > /dev/null')

def copyDexLib2(mainPath, dirs, a, b):
	os.chdir(mainPath)
	apis=[i for i in dirs if i in ["android", "java", "javax", "dalvik"]]
	#apis =[]
	#apis=[i for i in dirs if i in ["android", "java", "org", "javax", "dalvik"]]
	#for i in dirs:
		#for j in ["com/google/android", "com/googlecode"]:
			#if i+"/" in j:
				#if j not in apis:
					#apis.append(j)
	#[apis.append(i) for i in dirs if i in ["android"]]
	for j in apis:
		#command = "/bin/mv -f " + a +j + b+j
		command = "/bin/mv -f " + a +j + b
		verbosePrint(command)
		#verbosePrint(command)
		#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		#output = process.communicate()[0]
		os.system(command +' > /dev/null')
		print 'done copyDexLib'
    
def copyAJT(mainPath): 
	os.chdir(mainPath)   
	print mainPath+"/output/out"
	command = "/bin/cp -a "+"/var/www/html/PE-Droid/AspectJ/lib/org " +mainPath+"/output/out"
	#verbosePrint(command)
	#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	#output = process.communicate()[0] 
	os.system(command)
	print 'done copyAJT'
    
def callProguard():
	command = "java -jar /var/www/html/PE-Droid/proguard5.2.1/lib/proguard.jar -libraryjars lib/android.jar:./lib/aspectjrt.jar:./lib/google-play-services.jar @proguard.cfg -outjars ./output/output2.jar -ignorewarnings -dontoptimize -dontpreverify -dontshrink -keepattributes *Annotation*"
	os.system(command)
	print 'done proguard'
	
def callProguard2():
	command = "java -jar /var/www/html/PE-Droid/proguard5.2.1/lib/proguard.jar -libraryjars lib/android.jar:./lib/aspectjweaver.jar:./lib/rxjava.jar:./lib/okhttp-2.3.0.jar @proguard.cfg -outjars ./output/output2.jar -ignorewarnings -dontoptimize -dontpreverify -dontshrink -keepattributes *Annotation*"
	os.system(command)
	print 'done proguard'
	
	
def moveIt(mainPath):
	command = "/bin/cp -a "+mainPath+"/work/src/ " +mainPath+"/output/out"
	os.system(command)
