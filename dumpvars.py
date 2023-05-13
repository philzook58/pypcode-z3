#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
import json
f = getFunction("transport_handler")
def conv_var(v):
	return {
	"name" : v.name,
	"storage" : ["register", v.getRegister().name]
	}

print(json.dumps([ conv_var(v) for v in  f.localVariables]))