from Lexer import Lexer
from Papser import Parser
from codegen import CodeGen

import warnings

warnings.filterwarnings('ignore')

with open("test.txt") as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()

var = parser.parse(tokens)


def get_last_element(lst):
    if isinstance(lst, list):
        return get_last_element(lst[-1])
    else:
        return lst

for node in var:
    if type(node) == type(list()):
        item = get_last_element(node)
        print('\n',item)
        item.eval()
    else:
        node.eval()


codegen.create_ir()
codegen.save_ir("output.ll")
