from llvmlite import ir

var = {}

class Number():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        if '.' in self.value:
            i = ir.Constant(ir.DoubleType(), float(self.value))
        else:
            i = ir.Constant(ir.IntType(32), int(self.value))
        return i

class Ident():
    def __init__(self, builder, module, ident):
        self.ident = ident
        self.builder = builder
        self.module = module

    def eval(self):
        r = self.builder.load(var[self.ident])
        return r

class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

class Plus(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return(i)

class Minus(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return(i)

class Multiply(BinaryOp):
    def eval(self):
        i = self.builder.mul(self.left.eval(), self.right.eval())
        return(i)

class Divide(BinaryOp):
    def eval(self):
        i = self.builder.sdiv(self.left.eval(), self.right.eval())
        return(i)

class Bolee(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('>', self.left.eval(), self.right.eval())
        return i

class Menee(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('<', self.left.eval(), self.right.eval())
        return i

class NoAssign(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('!=', self.left.eval(), self.right.eval())
        return i

class And(BinaryOp):
    def eval(self):
        i = self.builder.and_(self.left.eval(), self.right.eval())
        return i

class Or(BinaryOp):
    def eval(self):
        i = self.builder.or_(self.left.eval(), self.right.eval())
        return i

class Mod(BinaryOp):
    def eval(self):
        i = self.builder.srem(self.left.eval(), self.right.eval())
        return i

class While:
    def __init__(self, builder, module, condition, body):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.body = body

    def eval(self):
        condit_block = self.builder.append_basic_block("condit_block") #condition
        body_block = self.builder.append_basic_block("body_block") #condition
        after_block = self.builder.append_basic_block("after_block") #after while

        self.builder.branch(condit_block)
        self.builder.position_at_start(condit_block)
        condit_value = self.condition.eval()
        self.builder.cbranch(condit_value, body_block, after_block)

        self.builder.position_at_start(body_block)
        for statement in self.body:
            statement.eval()
        condit_value = self.condition.eval()
        self.builder.cbranch(condit_value, body_block, after_block)

        self.builder.position_at_start(after_block)

class If:
    def __init__(self, builder, module, condition, body):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.body = body

    def eval(self):
        condition_value = self.condition.eval()
        body_block = self.builder.append_basic_block("if_block")
        after_block = self.builder.append_basic_block("after_block")
        self.builder.cbranch(condition_value, body_block, after_block)

        self.builder.position_at_start(body_block)
        for statement in self.body:
            statement.eval()
        self.builder.branch(after_block)
        self.builder.position_at_start(after_block)


class PereAssign():
    def __init__(self, builder, module, ident, value):
        self.builder = builder
        self.module = module
        self.ident = ident
        self.value = value

    def eval(self):
        if isinstance(self.value, str):
            self.builder.store(ir.Constant(ir.IntType(32), self.value), var[self.ident])
        else:
            value = self.value.eval()
            self.builder.store(value, var[self.ident])
class Assign():
    def __init__(self, builder, module, ident, value):
        self.builder = builder
        self.module = module
        self.ident = ident
        self.value = value

    def eval(self):
        if isinstance(self.value, str):
            if "." not in self.value:
                i = self.builder.alloca(ir.IntType(32), name=self.ident)
                var[self.ident] = i
                self.builder.store(ir.Constant(ir.IntType(32), self.value), i)

            elif "." in self.value:
                i = self.builder.alloca(ir.DoubleType(), name=self.ident)
                var[self.ident] = i
                self.builder.store(ir.Constant(ir.DoubleType(), self.value), i)
        else:
            i = self.builder.alloca(ir.IntType(32), name=self.ident)
            var[self.ident] = i
            value = self.value.eval()
            self.builder.store(value, i)



class Write:
    def __init__(self, builder, module, printf, value, idfstr):
        self.value = value
        self.builder = builder
        self.module = module
        self.printf = printf
        self.idfstr = idfstr

    def eval(self):
        value = self.value.eval()

        # Объявление списка аргументов
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        namefstr = f"fstr{self.idfstr}"
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=namefstr)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Вызов ф-ии Print
        self.builder.call(self.printf, [fmt_arg, value])
