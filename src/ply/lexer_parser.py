# https://www.dabeaz.com/ply/example.html
# http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html

# import lex
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'INT',
    'PLUS',
    'MINUS',
    'DIV',
    'MUL',
    'ASSIG',
    'VARDEC',
    'PRINT',
    'GREATER',
    'LESS',
    'EQUALS',
    'OPENPAR',
    'CLOSEPAR',
    'IDENT',
    'FUNC',
    'ENDFUNC',
    'BOOLVAL',
    'WHILE',
    'ENDLOOP',
    'DO',
    'OR',
    'AND'
)


t_INT = r'\d+'
t_PLUS = r'[+]'
t_MINUS = r'[-]'
t_DIV = r'[/]'
t_MUL = r'[*]'
t_OPENPAR = r'\('
t_CLOSEPAR = r'\)'
t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_VARDEC(t):
    r'int |bool '
    return t
def t_PRINT(t):
    r'print '
    return t
def t_GREATER(t):
    r'greater '
    return t
def t_LESS(t):
    r'less '
    return t
def t_EQUALS(t):
    r'equals '
    return t
def t_ASSIG(t):
    r'is '
    return t
def t_FUNC(t):
    r'func '
    return t
def t_ENDFUNC(t):
    r'endfunc'
    return t
def t_BOOLVAL(t):
    r'true|false'
    return t
def t_WHILE(t):
    r'while '
    return t
def t_ENDLOOP(t):
    r'endloop'
    return t
def t_DO(t):
    r'do'
    return t
def t_OR(t):
    r'or '
    return t
def t_AMD(t):
    r'and '
    return t



t_ignore = " \t"
# t_ignore = '\n+'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


precedence = (
    ('left','PLUS','MINUS'),
    ('left','MUL','DIV')
)

# variables = {}


# def p_program(t):
#     'program : stmts'
#     t[0] = t[1]

def p_stmts(t):
    '''stmts : stmt
             | stmts stmt'''
    # print('stmts')

def p_vardec(t):
    'stmt : VARDEC IDENT'
    print('vardec', t[1], t[2])
    # variables[t[2]] = None

def p_assig(t):
    'stmt : IDENT ASSIG relexpr'
    print('assig', t[1])
    # variables[t[1]] = t[3]

def p_print(t):
    'stmt : PRINT relexpr'
    print('print')
    # variables[t[1]] = t[3]

def p_funcdec(t):
    'stmt : VARDEC FUNC IDENT OPENPAR CLOSEPAR ASSIG stmts ENDFUNC'
    print('funcdec', t[3])

def p_while(t):
    'stmt : WHILE relexpr DO stmts ENDLOOP'
    print('whileloop')

def p_relexpr(t):
    '''relexpr : expr
               | expr GREATER expr
               | expr LESS expr
               | expr EQUALS expr'''
    print('relexpr')


# def p_binop(t):
#     '''expr : expr PLUS expr
#             | expr MINUS expr
#             | expr DIV expr
#             | expr MUL expr'''

def p_expr(t):
    '''expr : term
            | term PLUS term
            | term MINUS term
            | term OR term'''
    print('expr')

def p_term(t):
    '''term : factor
            | factor MUL factor
            | factor DIV factor
            | factor AND factor'''
    print('term')

def p_factor(t):
    '''factor : INT
              | IDENT
              | BOOLVAL'''


parser = yacc.yacc()

parser.parse(
     '''bool flag
        int x
        
        flag is true
        x is 5

        int func Sum() is
        print x
        endfunc
        
        while x greater 0 do
        print x
        endloop
        
        x is 5''')


# lexer.input('''bool flag
#         int x
        
#         flag is true
#         x is 5

#         int func Sum() is
#         print x
#         endfunc
        
#         while x greater 0 do
#         print x
#         endloop
        
#         x is 5''')

# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)