from rply import ParserGenerator
from ast import *


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
            'SEMI_COLON', 'SUM', 'SUB', 'IDENTIFIER']
        )

    def parse(self):


        @self.pg.production('program : statements')
        def program(p):
            return p[0]


        @self.pg.production('statements : statement SEMI_COLON')
        def statements(p):
            return Statements(False, [p[0]])
        
        @self.pg.production('statements : statements statement SEMI_COLON')
        def statements(p):
            p[0].add_child(p[1])
            return p[0]


        @self.pg.production('statement : PRINT OPEN_PAREN expression CLOSE_PAREN')
        def statement(p):
            return Print(p[2])
        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()