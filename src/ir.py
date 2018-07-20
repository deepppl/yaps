class IR(object):
    pass


class Program(IR):
    def __init__(self, blocks):
        self.blocks = blocks


# Program Blocks (Section 6)
class ProgramBlock(IR):
    def __init__(self, body=[]):
        self.body = []


class FunctionsBlock(ProgramBlock):
    def __init__(self, fdecls=[]):
        self.fdecls = fdecls


class DataBlock(ProgramBlock):
    def __init__(self, vdecls=[]):
        self.vdecls = vdecls


class TransformedDataBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class ParametersBlock(ProgramBlock):
    def __init__(self, vdecls=[]):
        self.vdecls = vdecls


class TransformedParametersBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class ModelBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class GeneratedQuantities(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts

# stmts (Section 5)


class Statement(IR):
    pass


class AssignStmt(Statement):
    def __init__(self, lval, op, exp):
        self.lval = lval
        self.op = op
        self.exp = exp


class SamplingStmt(Statement):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class ForStmt(Statement):
    def __init__(self, var, iter, body):
        self.var = var
        self.iter = iter
        self.body = body


class ConditionalStmt(Statement):
    def __init__(self, cond, exp, alt):
        self.cond = cond
        self.exp = exp
        self.alt = alt


class WhileStmt(Statement):
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmt = stmt


class Block(Statement):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class CallStmt(Statement):
    def __init__(self, id, args):
        self.id = id
        self.args = args


class BreakStmt(Statement):
    pass


class ContinueStmt(Statement):
    pass


# expessions (Section 4)
class Expression(IR):
    def __init__(self, value):
        self.value = value


class Atom(Expression):
    pass


class Constant(Atom):
    def __init__(self, value):
        self.value = value


class Variable(Atom):
    def __init__(self, id):
        self.id = id


class VectorExpr(Atom):
    pass


class ArrayExpr(Atom):
    pass


class Subscript(Atom):
    def __init__(self, val, slice):
        self.val = val
        self.slice = slice


class Binop(Expression):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs


class Call(Expression):
    def __init__(self, id, args):
        self.id = id
        self.args = args


# Declarations
class VariableDecl(IR):
    def __init__(self, id, ty, exp=None):
        self.id = id
        self.ty = ty
        self.exp = exp


class Type(IR):
    def __init__(self, kind, cstrts=None, dims=None):
        self.kind = kind
        self.cstrts = cstrts
        self.dims = dims