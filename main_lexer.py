from Lexer import Lexer

with open("factor.txt") as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
print("-------------------LEXER---------------------")
for token_print in tokens:
    print(token_print)