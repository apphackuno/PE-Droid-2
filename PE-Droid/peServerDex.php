<?php
#function for streaming file to client
function streamFile($location, $filename, $myDir){	
	$locPath = $myDir."/dexDownload";
	chdir($locPath );
	if(!file_exists($filename)){	
		return;
  }
  
  $size=filesize($filename);
  $time=date('r',filemtime($filename));
  #html response header
  header('Content-Description: File Transfer');	
  header("Content-Type: $mimeType"); 
  header('Cache-Control: public, must-revalidate, max-age=0');
  header('Pragma: no-cache');  
  header('Accept-Ranges: bytes');
  header('Content-Length:'.($size));
  header("Content-Disposition: inline; filename=$filename");
  header("Content-Transfer-Encoding: binary\n");
  header("Last-Modified: $time");
  header('Connection: close');   
  
  ob_clean();
  flush();
  readfile($filename);
  
 # header('Content-Description: File Transfer');	
#  header("Content-Type: application/zip"); 
 # header('Cache-Control: public, must-revalidate, max-age=0');
 # header('Accept-Ranges: bytes');
 # $size=filesize($filename);
#  header('Content-Length:'.($size));
#  header("Content-Disposition: inline; filename=".basename($filename));
 # echo headers_list;
 # header("Content-Transfer-Encoding: binary");
#  $time=date('r',filetime($filename));
#  header("Last-Modified: $time");
#  header('Connection: close');  
 # var_dump($size);    
#
 # ob_clean();
 # flush();
 # readfile($filename);
 # exit;
}
	
#instrumentation function
function instAPK($apk, $pkg){
	#chdir to apphack dir
	$instHome='/var/www/html/PE-Droid/AspectJ';
	chdir($instHome);
	flush();
	$command = ("python ./hackDex.py ".$apk ." PE-Aspects/PeLogger.aj ".$pkg);
	$output = shell_exec($command);
	# if no error return path to instrumneted app
}

#Server Connection
#declare client request variable
#ini_set('output_buffering', 'off');
#ini_set('display_errors', 0);
#ini_set('safe_mode', 0);
error_reporting(E_ALL | E_STRICT);


$myDir = '/var/www/html/PE-Droid';
$dex_upload_path = $myDir."/dexUpload/";
$dex_upload_path = $dex_upload_path. basename( $_FILES['uploadedfile']['name']);
$posS = strrpos($dex_upload_path,"/")+1;
$posE = strrpos($dex_upload_path,"-" );
$pkg = substr($dex_upload_path, $posS, $posE - $posS);
#<2>set target path for storing result on the server
$dex_output_path = $myDir."/dexDownload/";
$dex_output_path = $dex_output_path. basename( $_FILES['uploadedfile']['name']); 
$downloadFileName = 'newClass.dex';
#<3>modify maximum allowable file size to 10MB and timeout to 300s
ini_set('upload_max_filesize', '10M');  
ini_set('post_max_size', '10M');  
ini_set('max_input_time', 300);  
ini_set('max_execution_time', 300);  

#<4>Get and stored uploaded photos on the server
if(copy($_FILES['uploadedfile']['tmp_name'], $dex_upload_path)) {
	#set path for work dir
	# download in work dir
	# get user info, apkname, version, timestamp
	#store in db
	chdir($myDir);
	#$command = ("python googleapi/download.py ".$apkName ." 2>&1");
	#$output = shell_exec($command);
	#echo $output;
	if(file_exists ( $dex_upload_path)){
		$apkPath = realpath($dex_upload_path);
		instAPK($apkPath, $pkg);	
	}
	# check database dir
	
	chdir(myDir);
	$newApk="classes.dex";
	if(file_exists($newApk)){
		$newApkPath = realpath($newApk);
		$destAPK = $myDir."/dexDownload/".$newApk;
		system("mv ".$newApkPath ." ".$destAPK);
		$filename = $newApk;
		$name='classes.dex';
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
