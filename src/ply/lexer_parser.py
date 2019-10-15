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
    'IDENT'
)


t_INT = '\d+'
t_PLUS = '[+]'
t_MINUS = '[-]'
t_DIV = '[/]'
t_MUL = '[*]'
t_ASSIG = '= '
t_VARDEC = 'int | bool '
# t_BOOL = 'bool '
t_PRINT = 'print '
t_GREATER = 'greater'
t_LESS = 'less'
t_EQUALS = 'equals'
t_OPENPAR = r'\('
t_CLOSEPAR = r'\)'
t_IDENT = '[a-zA-Z]+'


t_ignore = ' \s+'
# t_ignore = '\n+'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)


lex.lex()


precedence = (
    ('left','PLUS','MINUS'),
    ('left','MUL','DIV')
)

variables = {}


def p_vardec(t):
    'statement : VARDEC IDENT'
    print(t[1])
    variables[t[2]] = None

def p_assig(t):
    'statement : IDENT ASSIG expr'
    print(t[1])
    variables[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expr'
    print(t[1])


def p_binop(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr DIV expr
            | expr MUL expr'''

    # https://stackoverflow.com/questions/18591778/how-to-pass-an-operator-to-a-python-function
    allowed_operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "//": operator.floordiv,
        "EQUALS": operator.eq,
        "GREATER": operator.gt,
        "LESS": operator.lt,
        "OR": operator.or_,
        "AND": operator.and_
    }

    t[0] = allowed_operators[t[2]](t[1], t[3])

def p_int(t):
    'expr : INT'
    t[0] = t[1]

# def p_expression_name(t):
#     'expr : IDENT'
#     try:
#         t[0] = variables[t[1]]
#     except LookupError:
#         print("Undefined name '%s'" % t[1])
#         t[0] = 0

# def p_error(t):
#     print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

parser.parse(
    '''int x
    s is 2''')

