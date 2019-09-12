import sys
from rply import LexerGenerator, ParserGenerator

lg = LexerGenerator()

# Building tokenization rules
lg.add('INTEGER', '\d')
lg.add('SUM', '[+]')
lg.add('MINUS', '[-]')
lg.add('DIV', '[/]')
lg.add('MUL', '[*]')
lg.add('ASSIG', 'is')
lg.add('INT', 'int')
lg.add('BOOL', 'bool')
lg.add('PRINT', 'print')
lg.add('GREATER', 'greater')
lg.add('LESS', 'less')
lg.add('EQUALS', 'equals')
lg.add('IDENT', '[a-zA-Z]')




# Ignore whitespaces
lg.ignore('\s')

lexer = lg.build()

with open(sys.argv[1], 'r') as file:
    lines = file.read()
tokens = list(lexer.lex(lines))
print(tokens)