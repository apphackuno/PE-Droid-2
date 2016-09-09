<?php
#function for streaming file to client
function streamFile($location, $filename, $myDir){	
	$locPath = $myDir.'/'.$location;
	chdir($locPath );
	if(!file_exists($filename)){	
		return;
  }
 
  header('Content-Description: File Transfer');	
  header("Content-Type: application/zip"); 
  header('Cache-Control: public, must-revalidate, max-age=0');
  header('Accept-Ranges: bytes');
  $size=filesize($filename);
  header('Content-Length:'.($size));
  header("Content-Disposition: inline; filename=".basename($filename));
  header("Content-Transfer-Encoding: binary\n");
  $time=date('r',filetime($filename));
  header("Last-Modified: $time");
  header('Connection: close');  
  var_dump($size);    

  ob_clean();
  flush();
  readfile($filename);
  exit;
}
	
#instrumentation function
function instAPK($apk){
	#chdir to apphack dir
	$instHome='/var/www/html/PE-Droid/AspectJ';
	chdir($instHome);
	flush();
	$command = ("python ./hackChat.py ".$apk ." PE-Aspects/PeLogger.aj");
	$output = shell_exec($command);
	echo $output;
	# if no error return path to instrumneted app
}

#Server Connection
#declare client request variable
#ini_set('output_buffering', 'off');
#ini_set('display_errors', 0);
#ini_set('safe_mode', 0);
error_reporting(E_ALL | E_STRICT);

$myDir = '/var/www/html/PE-Droid';
$apkName = $_POST['apkName'];
error_log(print_r($apkName, TRUE)); 
#$apkName="com.whatsapp";
#$apkName = 'com.whatsapp';
# when user install PE-client
	#get gmail account info and imei number for downloads
# when communication receive
	# 1) if apk string download and instrument apk then upload
	# 2) else if classes.dex instrument and upload
#new thread keep checking for update on data in mySql every morning
	#go through db check download apk get version, see if version change, 
		#if yes download, instrument and push to client
		#else quit thread for the day
if($apkName) {
	#set path for work dir
	# download in work dir
	# get user info, apkname, version, timestamp
	#store in db
	chdir($myDir);
	$command = ("python googleapi/download.py ".$apkName ." 2>&1");
	$output = shell_exec($command);
	if(file_exists ( $apkName .".apk" )){
		$apkPath = realpath($apkName .".apk");
		instAPK($apkPath);	
	}
	# check database dir
	
	chdir('database');
	$newApk=$apkName .".apk-signed.apk";
	if(file_exists($newApk)){
		$newApkPath = realpath($newApk);
		chdir($myDir);
		$destAPK = $myDir."/final/".$newApk;
		system("mv ".$newApkPath ." ".$destAPK);
		$filename = $newApk;
		$name='whatsapp.apk';
		streamFile($destAPK, $name, $myDir, $mimeType='application/octet-stream');
	}else {
		chdir($myDir);
	}
	#streamFile($location, $filename, $mimeType='application/octet-stream')
	#get apk full path
	#instrument
	#exec($command);
}
?>
