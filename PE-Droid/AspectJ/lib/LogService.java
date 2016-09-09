import java.io.File;
import java.util.ArrayList;
import java.util.Date;
import java.util.WeakHashMap;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.reflect.MethodSignature;

import android.util.Log;

public class LogService {
	public static void newDTSBody(JoinPoint jp, Object toTaint, Object arg, WeakHashMap<String, String> taintItems, ArrayList<String>tainteds, File dumpFile){
		String sig = jp.getSignature().getDeclaringTypeName().toString()+(".")+jp.getSignature().getName();
		String id = Integer.toString(System.identityHashCode(toTaint));
		String api= taintItems.get(arg.toString());
		//String params = (buildParam(thisJoinPoint.getArgs())).toString();
		tainteds.add(id);
		taintItems.put(id, api);
		Logger.outWrite(sig +" newDTS tainted "+ id +" oldtaint "+  arg.toString()+ " tainted source is  "+ api, dumpFile);
	}
	public static void argDTSBody(JoinPoint jp, Object toTaint, Object tar, WeakHashMap<String, String> taintItems, ArrayList<String>tainteds, File dumpFile){
		Object[] params = jp.getArgs();
  		StringBuilder apiBuilder = new StringBuilder();
  		StringBuilder taintedParams = new StringBuilder();
  		String api ="";
  		int chk=0;
  		if (params!=null){
  			for (int i=0; i<params.length; i++){
  				if (params[i]!=null && Logger.chkTaint(params[i], tainteds)){
  					if (api!=null){
  						if (!api.contains(taintItems.get(params[i].toString()))){
  							chk = 1;
  							apiBuilder.append(taintItems.get(params[i].toString()));
  						}
  						else{
  							if (taintItems.get(params[i].toString())!=null){
  								api=taintItems.get(params[i].toString());
  								chk = 1;
  								apiBuilder.append(taintItems.get(params[i].toString()));
  							}
  						}
  					}
  				}
  			}
  		}
  		if (chk==1){
  			String sig = jp.getSignature().getDeclaringTypeName().toString()+(".")+jp.getSignature().getName();
  			String id = Integer.toString(System.identityHashCode(tar));
  			api = apiBuilder.toString();
  			// outWrite(api+" "+ id +" " + tar.toString() + " "+ toTaint.toString(), dumpFile);
  			tainteds.add(id);
  			taintItems.put(id, api);
  			Logger.outWrite(sig +" argDTS tainteds = "+ id + " oldtaint "+  taintedParams.toString()+ " tainted source is  "+ api, dumpFile);
  		}

	}
	public static void retArgsBody(JoinPoint jp, Object toTaint, Object arg, WeakHashMap<String, String> taintItems, ArrayList<String>tainteds, File dumpFile){
		String sig = jp.getSignature().getDeclaringTypeName().toString()+(".")+jp.getSignature().getName();
		String api = taintItems.get(arg.toString());
		//if (!chkTaint(toTaint.toString(), tainteds)){
  		tainteds.add(toTaint.toString());
  		taintItems.put(toTaint.toString(), api);
      	Logger.outWrite(sig +" retArgs tainted = "+toTaint.toString()+" oldtaint "+  arg.toString() + " tainted source is  "+ api, dumpFile);
      	//}
	}
	public static void retTarBody(JoinPoint jp, Object toTaint, Object tar, WeakHashMap<String, String> taintItems, ArrayList<String>tainteds, File dumpFile){
		String sig = jp.getSignature().getDeclaringTypeName().toString()+(".")+jp.getSignature().getName();
		String tarHash="";
		if (tar.getClass().getName().startsWith("[") || sig.startsWith("java.lang.Object")){
			tarHash = Integer.toString(System.identityHashCode(tar));
		}else {
			tarHash = tar.toString();
		}
		String retHash = Integer.toString(System.identityHashCode(toTaint));
		String api = taintItems.get(tarHash);
		Object[] params = jp.getArgs();
		StringBuilder apiBuilder = new StringBuilder();
		int chk=0;
		//try{
		if (params!=null){
			for (int i=0; i<params.length; i++){
				if (params[i]!=null && Logger.chkTaint(params[i], tainteds)){
					Logger.outWrite(api+params[i], dumpFile);
					if (api!=null){
						if (!api.contains(taintItems.get(params[i].toString()))){
							chk = 1;
							apiBuilder.append(taintItems.get(params[i].toString()));
						}
						else{
							if (taintItems.get(params[i].toString())!=null){
								api=taintItems.get(params[i].toString());
								chk = 1;
								apiBuilder.append(taintItems.get(params[i].toString()));
							}
						}
					}
				}
			}
		}
		if (chk==1){
			api+= apiBuilder.toString();
		}
		MethodSignature meth = (MethodSignature)jp.getSignature();
		String type = meth.getReturnType().getName();
		if (api!=null && toTaint!=null){
			if(toTaint!=null && !Logger.getRet(toTaint)){
				if (type.endsWith("String") || type.endsWith("int") || type.endsWith("byte")
  					||type.endsWith("[java") || type.endsWith("[int") || type.endsWith("[B")){
					String ret= toTaint.toString();
					tainteds.add(ret);
					taintItems.put(ret, api);
					Logger.outWrite(sig +" retTar new primitive tainted= "+ ret +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}else if (!Logger.chkTaint(retHash, tainteds)){
					tainteds.add(retHash);
					taintItems.put(retHash, api);
					Logger.outWrite(sig + " retTar new Object tainted= "+ retHash +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}else{
					Logger.outWrite(sig +" retTar returns tainteds " + tarHash +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}
			}
  			}else if (!apiBuilder.toString().equals("")){
  				taintItems.put(tarHash, api);
  				Logger.outWrite(sig +" retTar returns tainteds " + tarHash +" returns "+  tarHash+ " tainted source is  "+ api, dumpFile);
  			}
	}
	public static void tarDTSBody(JoinPoint jp, Object toTaint, Object tar, WeakHashMap<String, String> taintItems, ArrayList<String>tainteds, File dumpFile){
		String sig = jp.getSignature().getDeclaringTypeName().toString()+(".")+jp.getSignature().getName();
		String tarHash = Integer.toString(System.identityHashCode(tar));
		String retHash = Integer.toString(System.identityHashCode(toTaint));
		String api = taintItems.get(tarHash);
		Object[] params = jp.getArgs();
		StringBuilder apiBuilder = new StringBuilder();
		int chk=0;
		if (params!=null){
			for (int i=0; i<params.length; i++){
				if (params[i]!=null && Logger.chkTaint(params[i], tainteds)){
					if (!api.contains(taintItems.get(params[i].toString()))){
						chk = 1;
						apiBuilder.append(taintItems.get(params[i].toString()));
					}
				}
			}
		}
		if (chk==1){
			api+= apiBuilder.toString();
		}
		MethodSignature meth = (MethodSignature)jp.getSignature();
		String type = meth.getReturnType().getName();
		if (api!=null){
			if(toTaint!=null && !Logger.getRet(toTaint)){
				if (type.endsWith("String") || type.endsWith("int") || type.endsWith("byte")
  					||type.endsWith("String[]") || type.endsWith("int[]") || type.endsWith("byte[]")){
					String ret= toTaint.toString();
					tainteds.add(ret);
					taintItems.put(ret, api);
					Logger.outWrite(sig +" tarDTS new primitive tainted= "+ ret +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}else if (!type.equals("void") && !Logger.chkTaint(retHash, tainteds)){
					tainteds.add(retHash);
					taintItems.put(retHash, api);
					Logger.outWrite(sig +" tarDTS new Object tainted= "+ retHash +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}else if (!apiBuilder.toString().equals("")){						
					taintItems.put(tarHash, api);
					Logger.outWrite(sig +" tarDTS returns tainteds " + tarHash +" returns "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}else{
					Logger.outWrite(sig +" tarDTS returns tainteds " + tarHash +" oldtaint "+  tarHash+ " tainted source is  "+ api, dumpFile);
				}
			}else if (!apiBuilder.toString().equals("")){
				taintItems.put(tarHash, api);
				Logger.outWrite(sig +" tarDTS returns tainteds " + tarHash +" returns "+  tarHash+ " tainted source is  "+ api, dumpFile);
			}
		}
  	
	}
	public static Object[] getParams(JoinPoint jp){
		Object[] params;	
			try{
				params = jp.getArgs();
			}catch(NullPointerException e){
				Log.e("Null Params",e.getMessage());
				params=null;
			}
			return params;
	}
	public static int taintChk(JoinPoint jp, WeakHashMap<String, String> taintItems, WeakHashMap<String, String> timeStamp, ArrayList<String>tainteds, int chk, StringBuilder myDat, String myTime){
		String methSig = jp.getSignature().getDeclaringTypeName().toString()+"."+jp.getSignature().getName();
		try{
		Object [] params = getParams(jp);
			//String targ = thisJoinPoint.getTarget().toString();
			
			String buf;
			//outWrite(timestamp.format(new Date()).toString() +" : "+ sig2 + "("+ buildParam(params).toString()+")"+ targ, dumpFile);
			if (params!=null){
				for (int i = 0; i < params.length; i++) {
					if (params[i] != null && Logger.chkTaint(params[i], tainteds)){
						chk=1;
						buf = taintItems.get(params[i].toString());
						if (!myDat.toString().contains(buf)){
							myDat.append(buf);
						}
						myTime=timeStamp.get(myDat);
						//outWrite(myDat+sig2, dumpFile);
						//params[i] = new String(padString(params[i].toString()));
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace();
			chk=0;
		}
			return chk;
	}
	public static void writeSink(JoinPoint jp, ArrayList<String> smsSink, StringBuilder myDat, String myTime, Object[] params, int chk, File traceFile){
		String sig = jp.getSignature().getName();
		String methSig = jp.getSignature().getDeclaringTypeName().toString()+"."+jp.getSignature().getName();
		if (chk==1){
			if (!Logger.chkTaint(sig, smsSink)){
				Logger.outWrite("<Data Exfiltration>"+myDat.toString() +" is Exfiltrated @ " +Logger.timestamp.format(new Date()).toString()+ " as "+Logger.buildParam(params).toString() + " in "+methSig, traceFile);
			}else{
				Logger.outWrite("<Data Exfiltration>"+myDat+ " : Data Exfiltration via SMS @" +Logger.timestamp.format(new Date()).toString() +" as "+Logger.buildParam(params).toString()+ " in "+ methSig, traceFile);
			}
			chk=0;
		}else {
			Logger.outWrite("<Sink Activites> {"+ methSig+"}("+Logger.buildParam(params).toString()+")",  traceFile);
		}
	}
}
