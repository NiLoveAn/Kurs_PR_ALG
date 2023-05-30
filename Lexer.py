from rply import LexerGenerator

class Lexer():

    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('Begin', r'begin')
        self.lexer.add('End', r'end')

        self.lexer.add('Plus', r'\+')
        self.lexer.add('Minus', r'\-')
        self.lexer.add('Multiply', r'\*')
        self.lexer.add('Divide', r'\/')

        self.lexer.add('Assign', r'=')
        self.lexer.add('Semicolon', r';')
        self.lexer.add('LParen', r'\(')
        self.lexer.add('RParen', r'\)')
        self.lexer.add('Write', r'print')

        self.lexer.add('While', r'while')
        self.lexer.add('If', r'if')

        self.lexer.add('Bolee', r'\>')
        self.lexer.add('Menee', r'\<')
        self.lexer.add('And', r'and')
        self.lexer.add('Or', r'or')
        self.lexer.add('NoAssign', r'\!=')
        self.lexer.add('Mod', r'\%')

        self.lexer.add('DOUBLE', r'double')
        self.lexer.add('INTEGER', r'int')
        self.lexer.add('Ident', r'[a-zA-Z][a-zA-Z0-9_]*')
        self.lexer.add('Double', r'\d+\.\d+')
        self.lexer.add('Int', r'\d+')

        self.lexer.ignore('\s+') #Space
        self.lexer.ignore('//.*') #Comment

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

