# https://www.dabeaz.com/ply/example.html
# http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html

import lex
import yacc

tokens = (
    'INT',
    'PLUS',
    'MINUS',
    'DIV',
    'MUL',
    'ASSIG',
    'INT',
    'BOOL',
    'PRINT',
    'GREATER',
    'LESS',
    'EQUALS',
    'OPENPAR',
    'CLOSEPAR',
    'IDENT'
)


t_INT = '\d+'
t_PLUS = '[+]'
t_MINUS = '[-]'
t_DIV = '[/]'
t_MUL = '[*]'
t_ASSIG = 'is '
t_INT = 'int '
t_BOOL = 'bool '
t_PRINT = 'print '
t_GREATER = 'greater'
t_LESS = 'less'
t_EQUALS = 'equals'
t_OPENPAR = r'\('
t_CLOSEPAR = r'\)'
t_IDENT = '([a-zA-Z])*'

t_ignore = '\s+'

lex.lex()



