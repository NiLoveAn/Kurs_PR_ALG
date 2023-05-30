from rply import ParserGenerator
import Ast
from Ast import Number, Ident, Plus, Minus, Multiply, Divide, Bolee, Menee, NoAssign, While, If, Assign, Write, PereAssign, And, Or, Mod

class Parser:
    def __init__(self, module, builder, printf):
        self.var = {}
        self.pg = ParserGenerator(
            ['Begin', 'End', 'Plus', 'Minus', 'Multiply', 'Divide', 'Assign', 'Semicolon',
             'LParen', 'RParen', 'Write', 'While', 'If', 'Bolee', 'Menee', 'Mod',
             'And', 'Or', 'NoAssign', 'Ident', 'Double', 'Int', 'DOUBLE', 'INTEGER']
        )
        self.module = module
        self.builder = builder
        self.printf = printf
        self.idfstr = 0

    def parse(self):
        @self.pg.production('body : line')
        def body(p):
            return p[0]

        @self.pg.production('line : line colon')
        def line_1(p):
            if p[1] is None:
                return p[0]
            else:
                return p[0] + [p[1]]

        @self.pg.production('line : colon')
        def line(p):
            if p[0] is None:
                return []
            else:
                return [p[0]]

        @self.pg.production('colon : assign Semicolon')
        @self.pg.production('colon : write Semicolon')
        @self.pg.production('colon : while Semicolon')
        @self.pg.production('colon : if Semicolon')
        @self.pg.production('colon : pereAssign Semicolon')
        def colons(p):
            return p[0]
#################################################################################
        @self.pg.production('pereAssign : Ident Assign expr')
        def pereAssign(p):
            if isinstance(p[2], Ast.Number):
                return PereAssign(self.builder, self.module, p[0].value, p[2].value)
            else:
                return PereAssign(self.builder, self.module, p[0].value, p[2])

        @self.pg.production('assign : DOUBLE Ident Assign expr')
        @self.pg.production('assign : INTEGER Ident Assign expr')
        def assign(p):
            if isinstance(p[3], Ast.Number):
                return Assign(self.builder, self.module, p[1].value, p[3].value)
            else:
                return Assign(self.builder, self.module, p[1].value, p[3])

#################################################################################
        @self.pg.production('write : Write LParen expr RParen')
        def write(p):
            self.idfstr += 1
            return Write(self.builder, self.module, self.printf, p[2], self.idfstr)

        @self.pg.production('while : While expr Begin line End')
        def while_b(p):
            return While(self.builder, self.module, p[1], p[3])

        @self.pg.production('if : If expr Begin line End')
        def if_b(p):
            return If(self.builder, self.module, p[1], p[3])


        @self.pg.production('expr : expr Plus expr')
        @self.pg.production('expr : expr Minus expr')
        @self.pg.production('expr : expr Multiply expr')
        @self.pg.production('expr : expr Divide expr')
        @self.pg.production('expr : expr NoAssign expr')
        @self.pg.production('expr : expr Bolee expr')
        @self.pg.production('expr : expr Menee expr')
        @self.pg.production('expr : expr And expr')
        @self.pg.production('expr : expr Or expr')
        @self.pg.production('expr : expr Mod expr')
        def expr(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'Plus':
                return Plus(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Minus':
                return Minus(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Multiply':
                return Multiply(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Divide':
                return Divide(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'NoAssign':
                return NoAssign(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Bolee':
                return Bolee(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Menee':
                return Menee(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'And':
                return And(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Or':
                return Or(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'Mod':
                return Mod(self.builder, self.module, left, right)


        @self.pg.production('expr : LParen expr RParen')
        def parens_expr(p):
            return p[1]

        @self.pg.production('expr : Int')
        @self.pg.production('expr : Double')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('expr : Ident')
        def ident(p):
            return Ident(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()


