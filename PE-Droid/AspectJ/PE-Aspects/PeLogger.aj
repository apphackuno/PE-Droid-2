import java.net.HttpURLConnection;
import java.net.URL;
import org.apache.http.client.HttpClient;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.Service;
import android.app.AlertDialog.Builder;
import android.content.ContentUris;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.Uri;
import android.os.Handler;
import android.os.IBinder;
//import java.util.Iterator;
import android.os.Looper;
import android.os.Message;
import android.telephony.SmsManager;
import android.webkit.WebView;
//import java.util.Iterator;
import android.widget.Toast;


public aspect PeLogger extends Service{
	Context instCont;
	private  SharedPreferences sharedPreferences;
	public static final String PREFS_Name = "PE_DroidPolicy";
	static String locPolicy = "Block";
	static String smsPolicy = "Ask";
	static String callPolicy = "Block";
	static String netPolicy = "Restrict Access";
	static String locRestrict;//GPS, MOBILE
	static String smsRestrict;//RECEIVED, SMSREAD, SEND
	static String callRestrict;//CALLREAD, CALLSEND
	static int netRestrict=1; //WIFI, MOBILE
	
	
	//Get privacy policy data from sharedPreferences file attached to the PE-Client if not available use default (You can manually change the policies from the code...................................................................................
	public void getShared(Context context){
		Context otherAppsContext = null;
		String myPrefs;
	 	try{
	 		otherAppsContext = context.getApplicationContext().createPackageContext("com.Android.pe_droidpolicy", Context.CONTEXT_IGNORE_SECURITY);
	 		sharedPreferences = otherAppsContext.getSharedPreferences(PREFS_Name, MODE_WORLD_READABLE);
	     	myPrefs = sharedPreferences.getString("test.Aisha.helloworld", "Empty");
	 		if (!myPrefs.equals("Empty")){
	 			String[] myVals = myPrefs.split(",");
	 			locPolicy = myVals[0].substring(myVals[0].indexOf(":")+1);
	 			smsPolicy = myVals[1].substring(myVals[0].indexOf(":")+1);
	 			callPolicy = myVals[2].substring(myVals[0].indexOf(":")+1);
	 			netPolicy = myVals[3].substring(myVals[0].indexOf(":")+1);
	 			if (locPolicy.contains("Restrict Access")){
	 				String[] newVals = locPolicy.split(",{");
	 				locPolicy = "Restrict Access";
	 				locRestrict = newVals[1].substring(newVals[0].indexOf("}"));
	 			}else if (smsPolicy.contains("Restrict Access")){
	 				String[] newVals = locPolicy.split(",{");
		 			smsPolicy = "Restrict Access";
		 			smsRestrict = newVals[1].substring(newVals[0].indexOf("}"));
		 		}else if (callPolicy.contains("Restrict Access")){
		 			String[] newVals = locPolicy.split(",{");
		 			callPolicy = "Restrict Access";
		 			callRestrict = newVals[1].substring(newVals[0].indexOf("}"));
		 		}else if (netPolicy.contains("Restrict Access")){
		 			String[] newVals = locPolicy.split(",{");
		 			netPolicy = "Restrict Access";
		 			//netRestrict = newVals[1].substring(newVals[0].indexOf("}"));
		 		}
		 	}
	 	} catch (Exception e) {
	 		myPrefs=null;	
	 	}
	}
	
		
	
	
	//Get DoalogBox....................................................................................
	private static int contOption=0;
	public static Dialog onCreateDialog(Context cont, String dat) {
    	final Handler handler = new Handler() {
            @Override
            public void handleMessage(Message mesg) {
                throw new RuntimeException();
            } 
        };
    	      Builder builder = new AlertDialog.Builder(cont);
    	      builder.setMessage(dat);
    	      builder.setCancelable(true);
    	      builder.setNegativeButton("Block", new DialogInterface.OnClickListener() {
    	          public void onClick(DialogInterface dialog, int whichButton) {
    	              contOption = 0;
    	              handler.sendMessage(handler.obtainMessage());
    	          }
    	      });
    	      builder.setPositiveButton("Allow", new DialogInterface.OnClickListener() {
    	          public void onClick(DialogInterface dialog, int whichButton) {
    	              contOption = 1;
    	              handler.sendMessage(handler.obtainMessage());
    	          }
    	      });
    	      AlertDialog dialog = builder.create();
    	      dialog.show();
    	      try { Looper.loop(); }
    	      catch(RuntimeException e2) {}
    	      return dialog;
    	}	
	
//	public Context myContext(){
	//	return this.getBaseContext();
//	}
	
 //Exclude AspectJ Code.............................................................................
	pointcut Test() :
		!within(PeLogger);
	
	//Application Context on initiliazation................................................................
	pointcut getContext(Context obj): target(obj) && Test() && if (thisJoinPoint.getKind().equals("initialization"));
	//pointcut getContext(): execution(* android.app.Activity.onCreate(..)) && Test();

	 before(Context cont) :getContext(cont){
	    	instCont = cont;
	    	if(instCont!=null){
	    		getShared(instCont);
	    	}
	   }
    
  //Location.........................................................................
    pointcut getLoc(LocationManager tar, String arg):call(* *..*(..)) &&  target(tar) && args(arg, ..) && Test();
    	
    Object around(LocationManager tar, String arg): getLoc(tar, arg){
    	//instCont = myContext();
    	if (locPolicy.equals("Block")){
    		return proceed(tar, "block");
    	}else if(locPolicy.equals("Restrict Access")){
    		if(arg.toUpperCase().contains(locRestrict)){
    			arg="block";
    		}
    		return proceed(tar, arg);
    	}else if(locPolicy.equals("Ask")){
    		onCreateDialog(instCont, "Allow Location for "+instCont.getPackageName());
    		if (contOption == 0){
    			arg = "block";
    		}
    		contOption=0;
    		return proceed(tar, arg);
    	}else{
    		return proceed(tar, arg);
    	}
    }
    
    //SMS from SmsManager
    pointcut getSMS(SmsManager tar):call(* *..*(..)) && target(tar) && Test();
    
    Object around(SmsManager tar): getSMS(tar){
    	//instCont = myContext();
    	String methName = thisJoinPoint.getSignature().getName().toUpperCase();
    	if (smsPolicy.equals("Block")){
    		return null;
    	}else if(smsPolicy.equals("Restrict Access")){
    		if(methName.contains(smsRestrict)){//If restrict SMSSend/write
    			return null;
    		}else{
    			return proceed(tar);
    		}
    	}else if(smsPolicy.equals("Ask")){
    		onCreateDialog(instCont, "Allow SMSSend From "+instCont.getPackageName());
    		if (contOption == 0){
    			return null;
    		}else{
    			contOption=0;
    			return proceed(tar);
    		}
    	}else{
    		return proceed(tar);
    	}
    }
    //SMS or Call from Intent
    pointcut fromIntent(Intent intent):execution(* *..*onReceive(..)) && args(*, intent) 
    && if (intent.getAction().toLowerCase().contains("sms") || 
    		(intent.getAction().toLowerCase().contains("call") 
    	 || intent.getAction().toLowerCase().contains("dial")))&& Test();
    
    Object around(Intent intent): fromIntent(intent){
    	//instCont = myContext();
    	String action = intent.getAction();
    	if (action.toLowerCase().contains("sms")){
    		if (smsPolicy.equals("Block")){
    			return null;
    		}else if(smsPolicy.equals("Restrict Access") ){
    			if(action.contains(smsRestrict)){//if restrict SMSRECEIVE
    				return null;
    			}else{
    				return proceed(intent);
    			}
    		}else if(smsPolicy.equals("Ask")){
    			onCreateDialog(instCont, "Allow SMSRECEIVE@ "+instCont.getPackageName());
    			if (contOption == 0){
    				return null;
    			}else{
    				contOption=0;
    				return proceed(intent);
    			}
    		}else{
    			return proceed(intent);
    		}
    	}else if (action.toLowerCase().contains("call") || action.toLowerCase().contains("dial")){
        		if (callPolicy.equals("Block")){
        			return null;
        		}else if(callPolicy.equals("Restrict Access") ){
        			if(action.contains(callRestrict)){//if restrict CALLSEND
        				return null;
        			}else{
        				return proceed(intent);
        			}
        		}else if(callPolicy.equals("Ask")){
        			onCreateDialog(instCont, "Allow CALLSEND @ "+instCont.getPackageName());
        			if (contOption == 0){
        				return null;
        			}else{
        				contOption=0;
        				return proceed(intent);
        			}
        		}else{
        			return proceed(intent);
        		}
        	}else{
    		return proceed(intent);
    	}
    }
    
    //Reading Calllog or smslog from provider
    pointcut queryCont(Uri uri): call(* *..*.query(..)) && args(uri, ..) && if (uri.getAuthority().toLowerCase().contains("call") 
    		|| uri.getAuthority().toLowerCase().contains("sms")) &&  Test();
  	Object around(Uri uri):queryCont(uri){
  		//instCont = myContext();
  		String auth = uri.getAuthority().toLowerCase();
  		if (auth.contains("sms")){
  			Uri newUri = ContentUris.withAppendedId(uri, 0);
    		if (smsPolicy.equals("Block")){
    			return proceed(newUri);
    		}else if(smsPolicy.equals("Restrict Access") ){
    			if(smsRestrict.toUpperCase().contains("SMSREAD")){//if restrict SMSREAD from provider
    				return proceed(newUri);
    			}else{
    				return proceed(uri);
    			}
    		}else if(smsPolicy.equals("Ask")){
    			onCreateDialog(instCont, "Allow SMS @ "+instCont.getPackageName());
    			if (contOption == 0){
    				return proceed(newUri);
    			}else{
    				contOption=0;
    				return proceed(uri);
    			}
    		}else{
    			return proceed(uri);
    		}
    	}else if (auth.contains("call")){
  			Uri newUri = ContentUris.withAppendedId(uri, 0);
    		if (smsPolicy.equals("Block")){
    			return proceed(newUri);
    		}else if(smsPolicy.equals("Restrict Access") ){
    			if(smsRestrict.toUpperCase().contains("CALLREAD")){//if restrict CALLLOG from provider
    				return proceed(newUri);
    			}else{
    				return proceed(uri);
    			}
    		}else if(smsPolicy.equals("Ask")){
    			onCreateDialog(instCont, "Allow SMS @ "+instCont.getPackageName());
    			if (contOption == 0){
    				return proceed(newUri);
    			}else{
    				contOption=0;
    				return proceed(uri);
    			}
    		}else{
    			return proceed(uri);
    		}
    	}
  		
  		else{
    		return proceed(uri);
    	}
  	}
  	
  //Network access .........................................................s
  //  pointcut getHttp(HttpClient tar):call(* *..*(..)) && target(tar) && Test();
  //  pointcut getHttpUrl(HttpURLConnection tar):call(* *..*(..)) && target(tar) && Test();
  //  pointcut getWeb(WebView tar):call(* *..*(..)) && target(tar) && Test();
   
    
    public URL voidnet(){
    	URL  url=null;
    	try{
    		url = new URL("Empty");
    	}catch(Exception e){
    		
    	}
    	return url;
    }
    
    public int getNetRestrict(String netRestrict){
    	if (netRestrict.equals("WIFI")){
    		return 1;
    	}else if (netRestrict.equals("MOBILE")){
    		return 0;
    	}else{
    		return 2;
    	}
    }
    pointcut getConMgr(ConnectivityManager tar):call(* *..*(..)) && target(tar) && Test();
    Object around (ConnectivityManager tar):getConMgr( tar){
    	//instCont = myContext();
    	if (netPolicy.equals("Block")){
    	//tar = new URL ("Empty");
    		return null;
    	}else if(netPolicy.equals("Restrict Access")){
    		if (tar.getActiveNetworkInfo().getType()==netRestrict){
    			if (netRestrict==1){
    				tar.setNetworkPreference(2);
    			}else{
    				tar.setNetworkPreference(1);
    			}
    		}
    			return proceed(tar);
    	}else if(netPolicy.equals("Ask")){
    		onCreateDialog(instCont, "Allow Network Access "+instCont.getPackageName());
    		if (contOption == 0){
    			return null;
    		}else{
    			contOption=0;
    			return proceed(tar);
    		}
    	}else{
    		return proceed(tar);
    	}
    }
   
    pointcut getUrl(URL tar):call(java.net.URLConnection *..*.openConnection(..)) && target(tar) && Test();
    Object around (URL tar):getUrl( tar){
    	//instCont = myContext();
    	if (netPolicy.equals("Block")){
    	//tar = new URL ("Empty");
    		return proceed(voidnet());
    	}else if (netPolicy.equals("Restrict Access")){
    		ConnectivityManager connMgr = (ConnectivityManager)instCont.getSystemService(CONNECTIVITY_SERVICE);
    		int netType = connMgr.getActiveNetworkInfo().getType();
    		if (netType==netRestrict){
    			return null;
    		}else{
    			return proceed(tar);
    		}
    	}else if(netPolicy.equals("Ask")){
    		onCreateDialog(instCont, "Allow Network Access "+instCont.getPackageName());
    		if (contOption == 0){
    			return proceed(voidnet());
    		}else{
    			contOption=0;
    			return proceed(tar);
    		}
    	}else{
    		return proceed(tar);
    	}
    }
    
  /**  Object around(SmsManager tar): getNet(tar){
    	instCont = myContext();
    	String methName = thisJoinPoint.getSignature().getName().toUpperCase();
    	if (smsPolicy.equals("Block")){
    		return null;
    	}else if(smsPolicy.equals("Restrict Access")){
    		if(methName.contains(smsRestrict)){//If restrict SMSSend/write
    			return null;
    		}else{
    			return proceed(tar);
    		}
    	}else if(smsPolicy.equals("Ask")){
    		onCreateDialog(instCont, "Allow SMSSend From "+instCont.getPackageName());
    		if (contOption == 0){
    			return null;
    		}else{
    			contOption=0;
    			return proceed(tar);
    		}
    	}else{
    		return proceed(tar);
    	}
    }*/
  	@Override
	public IBinder onBind(Intent intent) {
		// TODO Auto-generated method stub
	return null;
	}

}
