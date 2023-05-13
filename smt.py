#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here

class Term():
    def __eq__(self, rhs):
        return Eq(self, rhs)

    def __add__(self, rhs):
        return Function("bvadd", [self, rhs])

    def __and__(self, rhs):
        return Function("bvand", [self, rhs])

    def __invert__(self):
        return Function("bvneg", [self])

    def __mul__(self, rhs):
        return Function("bvmul", [self, rhs])

    def __sub__(self, rhs):
        return Function("bvsub", [self, rhs])

    def __sub__(self, rhs):
        return Function("bvsub", [self, rhs])

class Var(Term):
    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

    def __str__(self):
        return self.name

class Comment(Term):
	def __init__(self, comment, val):
		self.comment = comment
		self.val = val
	def __str__(self):
		return ";%s\n%s" % (self.comment, str(self.val))

def Vars(xs, sort):
    return [Var(x,sort) for x in xs.split()]


# class Sort(Enum):
#    NUMBER = auto()
#    SYMBOL = auto()
#    TERM = auto()
class Sort():
	def __init__(self, name):
		self.name =name


def BitVec(n):
	return Sort("(_ BitVec %d)" % n)


def bvconst(val, size):
    e = "(_ bv%d %d)" % (abs(val), size)
    if val < 0:
        e = "(bvneg %s)" % e
    return e


class Function(Term):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        args = " ".join([str(arg) for arg in self.args])
        return "(%s %s)" % (self.name, args)

def binop(name):
	return lambda x,y: Function(name, [x, y])

bvule = binop("bvule")
bvugt = binop("bvugt")
bvult = binop("bvult")
bvuge = binop("bvuge")

bvsle = binop("bvsle")
bvsgt = binop("bvsgt")
bvslt = binop("bvslt")
bvsge = binop("bvsge")
def select(mem, *args):
	return Function("select", [mem] + list(args))

def store(mem, *args):
	return Function("store", [mem] + list(args))

class Formula():
    def __and__(self, rhs):
        return And([self, rhs])

    def __le__(self, rhs):
        return Impl(rhs, self)

    def __gt__(self, rhs):
        return Impl(self, rhs)

    def __or__(self, rhs):
        return Or([self, rhs])

    def __invert__(self):
        return Not(self)


class Atom(Formula):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        if len(self.args) > 0:
            args = ",".join(map(str, self.args))
            return "%s(%s)" % (self.name, args)
        else:
            return self.name


def Const(name):
    return Atom(name, [])


def Consts(names):
    return [Const(name) for name in names.split()]


class Eq(Formula):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "(%s = %s)" % (str(self.lhs), str(self.rhs))


class And(Formula):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        t = " & ".join([str(val) for val in self.val])
        return "(%s)" % t


class Or(Formula):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        t = " | ".join([str(val) for val in self.val])
        return "(%s)" % t


class Impl(Formula):
    def __init__(self, hyp, conc):
        self.hyp = hyp
        self.conc = conc

    def __str__(self):
        return "(%s => %s)" % (str(self.hyp), str(self.conc))

class Quantifier(Formula):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

class Let(Quantifier):
    def __str__(self):
        vars = " ".join(["(%s %s)" % (str(var), str(b)) for (var, b) in self.vars])
        return "(let (%s)\n%s)" % (vars, str(self.body))

class ForAll(Formula):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def __str__(self):
        vars = ",".join([str(var) for var in self.vars])
        return "(! [%s] : %s)" % (vars, str(self.body))


class Exists(Formula):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def __str__(self):
        vars = ",".join([str(var) for var in self.vars])
        return "(? [%s] : %s)" % (vars, str(self.body))


class Not(Formula):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "(~ %s)" % str(self.val)