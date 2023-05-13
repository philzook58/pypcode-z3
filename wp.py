#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

'''
should look at ghihorn
also any symbolic executors out there
Countermodels into tyhe emulator
'''

from smt import *

Mem = Var("mem", Sort("(_ Array (_ BitVec 64) (_ BitVec 64) (_ BitVec 8))"))

def set_mem(space,addr,val):
    return store(Mem, space, addr, val)

def get_mem(space,addr):
    return select(Mem, space, addr)



def interp_varnode(varnode):
    size = varnode.getSize()
    space = varnode.getSpace()
    offset = varnode.getOffset()
    # check if in constant map
    # also probably reg map
    space = bvconst(space, 64)
    offset = bvconst(offset, 64)
    return get_mem(space,offset)
    return Var(str(varnode), BitVec(size))

    
# https://spinsel.dev/assets/2020-06-17-ghidra-brainfuck-processor-1/ghidra_docs/language_spec/html/pcodedescription.html
def wp(pcode, post):
    print pcode
    assert pcode.getNumInputs() <= 3
    x = interp_varnode(pcode.getInput(0))
    if pcode.getNumInputs() > 1:
        y = interp_varnode(pcode.getInput(1))
    if pcode.getNumInputs() > 2:
        z = interp_varnode(pcode.getInput(1))
    op = pcode.getOpcode()

    if pcode.isAssignment():
        if op == pcode.BOOL_AND:
            e = x & y
        elif op == pcode.BOOL_NEGATE:
            e = ~x
        elif op == pcode.BOOL_OR:
            e = x | y
        elif op == pcode.BOOL_XOR:
            e = x ^ y
        elif op == pcode.COPY:
            e = x
        elif op == pcode.INT_ADD:
            e = x + y
        elif op == pcode.INT_AND:
            e = x & y
        elif op == pcode.INT_SUB:
            e = x - y
        elif op == pcode.INT_DIV:
            e = x / y
        elif op == pcode.INT_EQUAL:
            e = x == y
        elif op == pcode.INT_LEFT:
            e = x << y
        elif op == pcode.INT_LESS:
            e = bvult(x, y)
        elif op == pcode.INT_MULT:
            e = x * y
        elif op == pcode.INT_NOTEQUAL:
            e = x != y
        elif op == pcode.INT_SBORROW:
            # revisit this one. I'm confused why this is different
            # from SLESS
            e = x > y
        elif op == pcode.INT_SEXT:
            outsize = pcode.getOutput().getSize()
            insize = pcode.getInput(0).getSize()
            e = Function("(_ sign_extend %d)" % (outsize - insize), [x])
        elif op == pcode.INT_SLESS:
            e = bvslt(x, y)
        elif op == pcode.INT_SUB:
            e = x - y
        elif op == pcode.INT_ZEXT:
            outsize = pcode.getOutput().getSize()
            insize = pcode.getInput(0).getSize()
            e = Function("(_ zero_extend %d)" % (outsize - insize), [x]) 
        elif op == pcode.INT_ZEXT:
            outsize = pcode.getOutput().getSize()
            insize = pcode.getInput(0).getSize()
            e = Function("(_ zero_extend %d)" % (outsize - insize), [x]) 
        elif op == pcode.LOAD:
            e = get_mem(x, y)
        elif op == pcode.POPCOUNT:
            e = Function("popcount", [x])
        elif op == pcode.SUBPIECE:
            # I always have a hard time getting extract right
            # in principal this offset might be symbolic? Hmm.
            size = pcode.getInput(1).getOffset() - 1
            e = Function("(extract _ %d 0)" % size ,[x])
        else:
            print "missing opcode"
            print pcode
            assert False
        #out = interp_varnode(pcode.getOutput())
        out = pcode.getOutput()
        space = bvconst(out.getSpace(), 64)
        offset = bvconst(out.getOffset(), 64)
        s = Comment(str(pcode),
        #Let([(out, e)], post))
        Let([(Mem, store(Mem, space, offset, e))], post))
        return s
    elif op == pcode.STORE:
        return Comment(str(pcode), Let([Mem], store(Mem, x, y, z)))
    elif op == pcode.BRANCH:
        print "WARN: branch unimplemented"
        return post
    elif op == pcode.CBRANCH:
        print "WARN: cbranch unimplemented"
        return post
    elif op == pcode.RETURN:
        print "WARN: return unimplemented"
        return post
    else:
        print pcode
        assert False
import tempfile
import subprocess
import pprint
def call_z3(formula):
    prelude = """
    (declare-const mem (Array (_ BitVec 64) (_ BitVec 64) (_ BitVec 64)))
    """
    with tempfile.NamedTemporaryFile(suffix=".smt2") as fp:
            fp.write(prelude)
            fp.write("(assert ")
            fp.write(str(formula))
            fp.write(")")
            fp.flush()
            print(fp.readlines())
            fp.seek(0)
            pprint.pprint(list(enumerate(fp.readlines())))
            res = subprocess.check_output(
                ["z3", fp.name], stderr=subprocess.STDOUT)
            print(str(res))


#TODO Add User Code Here

func = getFunctionContaining(currentAddress)

from ghidra.program.model.block import BasicBlockModel
from ghidra.util.task import TaskMonitor
# https://reverseengineering.stackexchange.com/questions/23469/way-to-get-basic-blocks-of-a-binary-using-ghidra
bbm = BasicBlockModel(currentProgram)
blocks = bbm.getCodeBlocks(TaskMonitor.DUMMY)
block = blocks.next()

while block:
    print "Label: {}".format(block.name)
    print "Min Address: {}".format(block.minAddress)
    print "Max address: {}".format(block.maxAddress)
    print
    block = blocks.next()
    listing = currentProgram.getListing()
    ins_iter = listing.getInstructions(block, True)
    for ins in reversed(list(ins_iter)):
        post = "true"
        #print "{} {}".format(ins.getAddressString(False, True), ins)
        #print ins.getPcode()
        for pcode in reversed(ins.getPcode()):
            post = wp(pcode, post)
    print post
    try:
        call_z3(post)
    except Exception as e:
        print(e.output)
        assert False