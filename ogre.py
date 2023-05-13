#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here

func = getFunctionContaining(currentAddress)
addrset = func.getBody()
entry = func.getEntryPoint()
for addr_range in addrset.getAddressRanges():
	print("(symbol-chunk (addr 0x%s) (size %s) (root 0x%s))" % 
		(addr_range.getMinAddress().getAddressableWordOffset(), hex(int(addr_range.getLength())), entry))
