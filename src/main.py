from lexer import Lexer
from parser import Parser
# https://blog.usejournal.com/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df
# http://joshsharp.com.au/blog/rpython-rply-interpreter-1.html

pg = Parser()
lexer = Lexer().get_lexer()

with open('hello.le', 'r', encoding='utf-8') as infile:
    lines = infile.read()

tokens = lexer.lex(lines)

pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()