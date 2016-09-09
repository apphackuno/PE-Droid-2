What is available: 
1. Instrumentation aspect for SMS, Calls, Network and Location privacy policy (PeLogger.aj)
2. Instrumentation framework (Unpackaginng, repackaging, weaving and re-signing) — you can take a look at all the python scripts in AspectJ dir
3. Dockerfile for creating docker container
4. PHP server scripts for accepting apk and dynamic class
5. Test App - Helloworld.apk

What is missing:
1. PE-Client
2. Dynamic class advice
3. Update tracking module

Issues on ground: If an app exceeds 64K methods the instrumentation engine breaks. Working on a fix to dynamically weave advice instead of static weaving. 
  
#############

To build the docker container, install docker and apache on a linux system. 
Change the Device ID, username and password to a valid google play account in config.py in googleplayapi dir.
Go to the parent directory of where you pull the project to and then run the following commands:
	docker build -t apache/myphp .
	docker run -it -p 80:80  -e ALLOW_OVERRIDE=true --name="pedroid_ondemand" apache/myphp


#############

To run PE-Droid without PE-Client type the following Url
	localhost:80/PE-Droid/test.html
	enter name of an app (It has to be a complete package name e.g com.lionmobi.battery


###############
To run the instrumentation engine without using server execute the command as:
./hackChat.py HelloWorld.apk PE-Aspects/PeLogger.aj


