import sys
from rply import LexerGenerator, ParserGenerator

# ReadTheDocs tutorial:
# https://buildmedia.readthedocs.org/media/pdf/rply/latest/rply.pdf

lg = LexerGenerator()

# Building tokenization rules
lg.add('INTEGER', '\d')
lg.add('PLUS', '[+]')
lg.add('MINUS', '[-]')
lg.add('DIV', '[/]')
lg.add('MUL', '[*]')
lg.add('ASSIG', 'is ')
lg.add('INT', 'int ')
lg.add('BOOL', 'bool ')
lg.add('PRINT', 'print ')
lg.add('GREATER', 'greater')
lg.add('LESS', 'less')
lg.add('EQUALS', 'equals')
lg.add('IDENT', '([a-zA-Z])*')




# Ignore whitespaces
lg.ignore('\s+')

lexer = lg.build()

with open(sys.argv[1], 'r') as file:
    lines = file.read()
tokens = list(lexer.lex(lines))
print(tokens)





pg = ParserGenerator(
    # List of all tokens
    ['INTEGER', 'PRINT', 'ASSIG',
    'PLUS', 'MINUS', 'MUL', 'DIV'],
    # List of rules
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)


@pg.production('expression : INTEGER')
def expression_number(p):
    return int(p[0].getstr())
# @pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
# def expression_parens(p):
#     return p[1]
@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return left + right
    elif p[1].gettokentype() == 'MINUS':
        return left - right
    elif p[1].gettokentype() == 'MUL':
        return left * right
    elif p[1].gettokentype() == 'DIV':
        return left / right
    else:
        raise AssertionError('Oops, this should not be possible!')
parser = pg.build()


print(parser.parse(lexer.lex('1 + 1 + 1 * 3')))