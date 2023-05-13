#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.app.decompiler import ClangToken

import json
#TODO Add User Code Here

from ghidra.app.decompiler import DecompInterface
decomp = DecompInterface()
decomp.openProgram(currentProgram)
func = getFunctionContaining(currentAddress)
print(currentAddress)
print(func)
res = decomp.decompileFunction(func, 0, None)
ccode = res.getCCodeMarkup()
highvars = set()

def collect(code):
	
	for i in range(code.numChildren()):
		c = code.Child(i)
		if isinstance(c, ClangToken) and c.getHighVariable() != None:
			highvars.add(c.getHighVariable())
		else:
			collect(c)

collect(ccode)
print(highvars)

data = []

def extract_pcode(pcode):
	if pcode != None:
		return {
	"seqnum" : str(pcode.getSeqnum()),
	"address" : str(pcode.getSeqnum().getTarget()),
	"pcode" : str(pcode)
	}
	

def extract_varnode(vnode):
	return {
		"varnode" : str(vnode),
		 "def" : extract_pcode(vnode.getDef()),
		"uses" : [extract_pcode(pcode) for pcode in vnode.getDescendants()]
		}

	

for highvar in highvars:
	varnodes = highvar.getInstances()
	if highvar.getName() != None:
		data.append({
			"name" : highvar.getName(),
			"varnodes" : [extract_varnode(vnode) for vnode in varnodes]
		})
print(json.dumps(data,  sort_keys=True, indent=4))

	


	

