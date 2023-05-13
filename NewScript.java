//TODO write a description for this script
//@author 
//@category _NEW_
//@keybinding 
//@menupath 
//@toolbar 

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import ghidra.app.decompiler.ClangTokenGroup;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.util.*;
import ghidra.program.model.reloc.*;
import ghidra.program.model.data.*;
import ghidra.program.model.block.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.lang.*;
import ghidra.program.model.pcode.*;
import ghidra.program.model.address.*;

// hmm.
//import org.json.simple.JSONObject;

public class NewScript extends GhidraScript {
	private static class StreamGobbler implements Runnable {
	    private InputStream inputStream;
	    private Consumer<String> consumer;

	    public StreamGobbler(InputStream inputStream, Consumer<String> consumer) {
	        this.inputStream = inputStream;
	        this.consumer = consumer;
	    }

	    @Override
	    public void run() {
	        new BufferedReader(new InputStreamReader(inputStream)).lines()
	          .forEach(consumer);
	    }
	}
    public void run() throws Exception {
//TODO Add User Code Here
    	println("helloworlld");
    	
    	/*
        JSONObject obj = new JSONObject();

        obj.put("name", "foo");
        obj.put("num", new Integer(100));
        obj.put("balance", new Double(1000.21));
        obj.put("is_vip", new Boolean(true));
                System.out.print(obj);
*/
   /* https://www.tutorialspoint.com/java_xml/java_dom_create_document.htm
    * wE CAN ADD simple dependencies into plugins, so we'll bring in some kind of json thing. Fine.
    	DocumentBuilderFactory dbFactory =
    	         DocumentBuilderFactory.newInstance();
    	         DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
    	         Document doc = dBuilder.newDocument();
    	         
    	         // root element
    	         Element rootElement = doc.createElement("cars");
    	         doc.appendChild(rootElement);
   */
    	// Caling process
    	Listing listing = currentProgram.getListing();
    	Function func = listing.getFunctionContaining(currentAddress);
        if (func == null) {
            println("No Function at address " + currentAddress);
            return;
        }
    	println(func.getLocalVariables().toString());
    	DecompInterface decomplib = new DecompInterface();
        if (decomplib == null) {
            println("No Function at address " + currentAddress);
            return;
        }
        decomplib.toggleSyntaxTree(true);
    	if (!decomplib.openProgram(currentProgram)) {
    		println("Decompile Error: " + decomplib.getLastMessage());
    		return;
    	}
    	
    	//println(Integer.toString(decomplib.getOptions().getDefaultTimeout() ));
    	DecompileResults decompRes = decomplib.decompileFunction(func, 5, monitor);
        HighFunction hfunction = decompRes.getHighFunction();
        
        println(hfunction.buildFunctionXML(func.getID(), func, null, 1000));
        ClangTokenGroup docroot = decompRes.getCCodeMarkup();
    	println(hfunction.toString());
    	println(decompRes.toString());
    	
    	
        ProcessBuilder builder = new ProcessBuilder();
        builder.command("bap", "vibes");
        Process process;
		try {
			process = builder.start();
			StreamGobbler streamGobbler = 
					  new StreamGobbler(process.getInputStream(), System.out::println);
					Executors.newSingleThreadExecutor().submit(streamGobbler);
			int exitcode = process.waitFor();
			System.out.println("exitcode" + exitcode);
			// println("foo");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }

}
