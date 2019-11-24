#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import sys

class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class PrePro:
    @staticmethod
    def removeComments(origin):
        flag = False
        procorigin = ''
        for i in origin:
            if (i == "'"):
                flag = not flag
                continue
            if (i == '\n'):
                flag = False
            if (flag):
                continue
            procorigin += i
        return procorigin

class Node:
    def __init__(self, value=None, nodes=[]):
        self.value = value
        self.children = nodes
    def Evaluate(self, st):
        pass

class BinOp (Node):
    def Evaluate(self, st):
        # https://stackoverflow.com/questions/18591778/how-to-pass-an-operator-to-a-python-function
        allowed_operators={
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
        child1 = self.children[0].Evaluate(st)
        child2 = self.children[1].Evaluate(st)
        # print(child1, self.children[1].Evaluate(st))
        child2val = child2[0]
        child2type = child2[1]
        if ((child1[1] == 'INTEGER' or child1[1] == 'INT') and (child2type == 'INTEGER' or child2type == 'INT') and self.value in ['+', '-', '*', '//']):
            return [allowed_operators[self.value](child1[0], child2val), 'INTEGER']
        elif ((child1[1] == 'INTEGER' or child1[1] == 'INT') and (child2type == 'INTEGER' or child2type == 'INT') and self.value in ['EQUALS', 'GREATER', 'LESS']):
            return [allowed_operators[self.value](child1[0], child2val), 'BOOLEAN']
        elif (child1[1] == 'BOOLEAN' and child2type == 'BOOLEAN' and self.value in ['OR', 'AND', '=']):
            return [allowed_operators[self.value](child1[0], child2val), 'BOOLEAN']
        else:
            # print(child1)
            # print(child2)
            raise ValueError('Operands type "%s" and "%s" does not match operation "%s"' %(child1[1], child2[1], self.value))

class UnOp(Node):
    def Evaluate(self, st):
        child = self.children[0].Evaluate(st)
        # print(child)
        if (self.value in ['-', '+']):
            if (child[1] == 'INTEGER'):
                if (self.value == '+'):
                    return [+child[0], 'INTEGER']
                if (self.value == '-'):
                    return [-child[0], 'INTEGER']
            else:
                raise ValueError('Operand type "%s" does not match operation "%s"' %(self.children[0].children[1].Evaluate(st), self.value))
        elif (self.value == 'NOT'):
            if (child[1] == 'BOOLEAN'):
                return [not child[0], 'BOOLEAN']
            else:
                raise ValueError('Operand type "%s" does not match operation "%s"' %(self.children[0].children[1].Evaluate(st), self.value))

class IntVal(Node):
    def Evaluate(self, st):
        return [int(self.children[0]), self.children[1].Evaluate(st)]

class BoolVal(Node):
    def Evaluate(self, st):
        # print('qqqqqqqq', self.value)
        if (self.children[0] == 'TRUE'):
            return [True, self.children[1].Evaluate(st)]
        else:
            return [False, self.children[1].Evaluate(st)]

class Identifier(Node):
    def Evaluate(self, st):
        return st.getter(self.value)

class NoOp(Node):
    pass

class Program(Node):
    def Evaluate(self, st):
        for i in self.children:
            i.Evaluate(st)

class Statements(Node):
    def Evaluate(self, st):
        for i in self.children:
            i.Evaluate(st)

class Assignment(Node):
    def Evaluate(self, st):
        # print('assigment', self.children)
        child1 = self.children[0]
        child2 = self.children[1].Evaluate(st)
        child2val = child2[0]
        child2type = child2[1]
        testchild = self.children[0]
        # print(child1.Evaluate(st), testchild.value)
        # print('st:', st.symtabledict)
        if (child2type == 'BOOLEAN' and child2val in [False, True]):
            st.setter(child1.value, child2val, child2type)
        elif ((child2type == 'INTEGER' or child2type == 'INT') and isinstance(child2val, int)):
            st.setter(child1.value, child2val, child2type)
        else:
            raise ValueError('Operand value "%s" does not match type "%s"' %(child2val, child2type))


class Print(Node):
    def Evaluate(self, st):
        # print('print:', self.children[0])
        print(self.children[0].Evaluate(st)[0])

class While(Node):
    def Evaluate(self, st):
        # print('while: ', self.children[0].Evaluate(st)[0])
        while (self.children[0].Evaluate(st)[0]):
            self.children[1].Evaluate(st)

class If(Node):
    def Evaluate(self, st):
        if (self.children[0].Evaluate(st)[0]):
            self.children[1].Evaluate(st)
        elif (len(self.children) == 3):
            self.children[2].Evaluate(st)

class Input(Node):
    def Evaluate(self, st):
        # print('Input:')
        userinput = input('Input: ')
        print('\n')
        try:
            userinput = int(userinput)
            return [userinput, 'INTEGER']
        except:
            raise ValueError('Expected INT input, got input "%s" of type: "%s"' %(userinput, type(userinput)))

class VarDec(Node):
    def Evaluate(self, st):
        # print('var1name', self.children[0])
        # print('var1:', self.children[1].Evaluate(st))
        st.setter(self.children[0], None, self.children[1].Evaluate(st))

class VarType(Node):
    def Evaluate(self, st):
        return self.value

class FuncDec(Node):
    def Evaluate(self, st):
        # self.children[0].Evaluate()
        st.setter(self.value, self, 'FUNCTION')

class SubDec(Node):
    def Evaluate(self, st):
        # self.children[0].Evaluate()
        # print('sub setter: ', self.value, self)
        st.setter(self.value, self, 'SUB')

class FuncSubCall(Node):
    def Evaluate(self, st):
        # print('aaaaaaaaaaaaaaa')
        funcsubst = st.symtabledict.copy()
        funcsubst = SymbolTable(funcsubst)

        # print('test', funcsubst.getter(self.value))
        # funcsubst.setter(self.value, self, funcsubst.getter(self.value)[1])
        funcsubnode = funcsubst.getter(self.value)[0]
        funcsubnodetype = funcsubst.getter(self.value)[1]
        # print(funcsubst.getter(self.value))
        # print(st.symtabledict)
        # print('children: ', self.children)
        # print('funcsubnode:', funcsubst.getter(self.value))
        # print(funcsubnodetype)
        # print('funcsubargs:', funcsubnode.children[1:-1])
        # print('callargs:', self.children)
        if (len(funcsubnode.children[1:-1]) != len(self.children)):
            raise ValueError('Argument amount does not match Function Declaration argument amount')

        idents = []
        for i in funcsubnode.children[:-1]:
            i.Evaluate(funcsubst)
            idents.append(i.children[0])

        
        for i,j in enumerate(self.children):
            # print(self.children[0].children)
            # print('j:', j.Evaluate(funcsubst))
            value = j.Evaluate(funcsubst)
            # print(funcsubst.symtabledict)
            funcsubst.setter(idents[i+1], value[0], value[1])
        # print(funcsubst.getter('a'))
        # print(funcsubst.symtabledict)
        funcsubnode.children[-1].Evaluate(funcsubst)
        # print('bbbbbbbbbbbbb')
        if (funcsubnodetype == 'FUNCTION'):
            return funcsubst.getter(self.value)


class SymbolTable:
    def __init__(self, ancestor={}):
        self.symtabledict = ancestor
        # self.ancestor = ancestor
    def getter(self, identifier):
        # print(self.symtabledict)
        if (identifier in self.symtabledict):
            return self.symtabledict[identifier]
        # elif (self.ancestor != None):
        #     return self.ancestor.getter(identifier)
        raise ValueError('Variable "%s" not defined' %(identifier))
    def setter(self, identifier, value, vartype):
        self.symtabledict[identifier] = [value, vartype]


class Tokenizer:
    def __init__(self, origin):
        self.origin = PrePro.removeComments(origin)
        self.position = 0
        self.actual = Token('EOF', 'EOF')
        self.reservedwords =    ['PRINT', 'IF', 'WHILE', 'THEN', 'ELSE', 'WEND',
                                'INPUT', 'END', 'SUB', 'MAIN', 'INTEGER', 'BOOLEAN',
                                'DIM', 'AS', 'TRUE', 'FALSE', 'NOT', 'AND', 'OR',
                                'FUNCTION', 'CALL', 'INT', 'BOOL', 'ENDIF', 'ENDLOOP',
                                'FUNC']
        self.selectNext()

    def selectNext(self):
        while (self.position < len(self.origin) and self.origin[self.position] == ' '):
            self.position += 1

        if (self.position >= (len(self.origin))):
            self.actual = Token('EOF', 'EOF')
            return

        token = ''

        if (self.origin[self.position].isdigit()):
            while (self.position < (len(self.origin)) and self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            self.actual = Token('INT', token)

        elif (self.origin[self.position].isalpha()):
            while (self.position < (len(self.origin)) and self.origin[self.position].isalpha() or self.position < (len(self.origin)) and self.origin[self.position] == '_'):
                token += self.origin[self.position]
                self.position += 1
            token = token.upper()

            if (token in self.reservedwords):
                self.actual = Token('COMM', token)
            elif (token == 'IS'):
                self.actual = Token('ASSIG', token)
            elif (token == 'GREATER'):
                self.actual = Token('GREATER', token)
            elif (token == 'LESS'):
                self.actual = Token('LESS', token)
            elif (token == 'EQUALS'):
                self.actual = Token('EQUALS', token)
            else:
                self.actual = Token('IDENT', token)

        else:
            if (not self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            if (token == '+'):
                self.actual = Token('PLUS', token)
            elif (token == '-'):
                self.actual = Token('MINUS', token)
            elif (token == '*'):
                self.actual = Token('MULT', token)
            elif (token == '/'):
                self.actual = Token('DIV', '//')
            elif (token == '//'):
                self.actual = Token('DIV', token)
            elif (token == '('):
                self.actual = Token('PAR', token)
            elif (token == ')'):
                self.actual = Token('PAR', token)
            # elif (token == '='):
            #     self.actual = Token('ASSIG', token)
            elif (token == '\n'):
                self.actual = Token('ENDL', token)
            elif (token == '<'):
                self.actual = Token('LESS', token)
            # elif (token == '>'):
            #     self.actual = Token('GREATER', token)
            elif (token == ','):
                self.actual = Token('COMMA', token)
            else:
                raise ValueError('Unexpected token "%s"' %(token))
        # print(self.actual.tokentype, self.actual.tokenvalue)




class Parser:
    @staticmethod
    def varType():
        vartype = Parser.tokens.actual
        if (Parser.tokens.actual.tokentype == 'COMM'):
            if (Parser.tokens.actual.tokenvalue == 'INT'):
                Parser.tokens.selectNext()
                return VarType('INT')
            elif (Parser.tokens.actual.tokenvalue == 'BOOL'):
                Parser.tokens.selectNext()
                return VarType('BOOL')
            else:
                raise SyntaxError('Unrecognized variable type "%s"' %(Parser.tokens.actual.tokenvalue))
        else:
            raise SyntaxError('Expected command type token, got token of type "%s"' %(Parser.tokens.actual.tokentype))

    @staticmethod
    def factorExpression():
        # print('factor')
        try:
            token1 = Parser.tokens.actual
            # print(token1.tokenvalue, token1.tokentype)
        except:
            raise ValueError('Token not found')
        if (token1.tokentype == 'INT'):
            Parser.tokens.selectNext()
            return IntVal('INT', [token1.tokenvalue, VarType('INTEGER')])

        elif (token1.tokentype == 'PLUS' or token1.tokentype == 'MINUS' or token1.tokenvalue == 'NOT'):
            if (token1.tokentype == 'PLUS'):
                Parser.tokens.selectNext()
                return UnOp('+', [Parser.factorExpression()])
            elif (token1.tokentype == 'MINUS'):
                Parser.tokens.selectNext()
                return UnOp('-', [Parser.factorExpression()])
            elif (token1.tokenvalue == 'NOT'):
                Parser.tokens.selectNext()
                return UnOp('NOT', [Parser.factorExpression()])
            else:
                raise SyntaxError('Unexpected unary operation "%s"' %(token1.tokenvalue))

        elif (token1.tokentype == 'IDENT'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue != '('):
                return Identifier(token1.tokenvalue)

            # print('identttttttttttttttttttt')
            # print('funcsubcall', token1.tokenvalue)
            funcsubcall = FuncSubCall(token1.tokenvalue, [])
            # Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenvalue)
            if (Parser.tokens.actual.tokenvalue == '('):
                Parser.tokens.selectNext()
                while (Parser.tokens.actual.tokenvalue != ')'):
                    # print(Parser.tokens.actual.tokenvalue)
                    funcsubcall.children.append(Parser.relExpression())
                    # print('appended')
                    if (Parser.tokens.actual.tokenvalue == ','):
                        Parser.tokens.selectNext()
                        continue
                    break
                if (Parser.tokens.actual.tokenvalue != ')'):
                    raise SyntaxError('Expected ")" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                Parser.tokens.selectNext()
                # print(funcsubcall.)
                return funcsubcall
            else:
                raise SyntaxError('Expected token "(", got "%s"' %(Parser.tokens.actual.tokenvalue))

        elif (token1.tokenvalue == '('):
            Parser.tokens.selectNext()
            parexpr = Parser.relExpression()
            if (Parser.tokens.actual.tokenvalue == ')'):
                Parser.tokens.selectNext()
                return parexpr
            else:
                raise SyntaxError('Unexpected token "%s", expected ")"' %(Parser.tokens.actual.tokenvalue))
        elif (token1.tokenvalue == 'INPUT'):
            Parser.tokens.selectNext()
            # print('input')
            return Input()
        elif (token1.tokentype == 'COMM'):
            if (token1.tokenvalue in ['TRUE', 'FALSE']):
                Parser.tokens.selectNext()
                return BoolVal('BOOL', [token1.tokenvalue, VarType('BOOLEAN')])
            else:
                raise ValueError('Expected "TRUE" or "FALSE", got "%s"' %(token1.tokenvalue))
        else:
            raise SyntaxError('Invalid token "%s" of type "%s"' %(token1.tokenvalue, token1.tokentype))

    @staticmethod
    def termExpression():
        termop = Parser.factorExpression()
        while (Parser.tokens.actual.tokentype == 'DIV' or Parser.tokens.actual.tokentype == 'MULT' or Parser.tokens.actual.tokenvalue == 'AND'):
            termop = BinOp(Parser.tokens.actual.tokenvalue, [termop])
            Parser.tokens.selectNext()
            factor2 = Parser.factorExpression()
            termop.children.append(factor2)
        return termop

    @staticmethod
    def parserExpression():
        parserop = Parser.termExpression()
        # print(Parser.tokens.actual.tokentype)
        while (Parser.tokens.actual.tokentype == 'PLUS' or Parser.tokens.actual.tokentype == 'MINUS' or Parser.tokens.actual.tokenvalue == 'OR'):
            parserop = BinOp(Parser.tokens.actual.tokenvalue, [parserop])
            Parser.tokens.selectNext()
            parserop.children.append(Parser.termExpression())
        return parserop
    
    @staticmethod
    def functionDeclaration(funcvartype):
        # print('funcdec')
        funcargs = [VarDec('VARDEC', [])]
        funcstmts = Statements('STATEMENTS', [])
        if (Parser.tokens.actual.tokenvalue == 'FUNC'):
            Parser.tokens.selectNext()
            funcident = Parser.tokens.actual.tokenvalue
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue == '('):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.tokenvalue != ')'):
                    while True:
                        argtype = Parser.varType()
                        # print(Parser.tokens.actual.tokenvalue)
                        argident = Parser.tokens.actual.tokenvalue
                        Parser.tokens.selectNext()
                        # print('argident:', argident)
                        # print('argtype:', argtype)
                        funcargs.append(VarDec('VARDEC', [argident, argtype]))
                            # Parser.tokens.selectNext()
                        if (Parser.tokens.actual.tokenvalue == ','):
                            Parser.tokens.selectNext()
                            continue
                        break
                if (Parser.tokens.actual.tokenvalue == ')'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == 'IS'):
                        Parser.tokens.selectNext()
                        # functype = VarDec('VARDEC', [funcident, Parser.varType()])
                        funcargs[0].children.append(funcident)
                        funcargs[0].children.append(funcvartype)
                        # Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        Parser.tokens.selectNext()
                        while (Parser.tokens.actual.tokenvalue != 'ENDFUNC'):
                            funcstmts.children.append(Parser.statement())
                            if (Parser.tokens.actual.tokenvalue != '\n'):
                                raise SyntaxError('Expected ENDLINE token after statement, got "%s"' %(Parser.tokens.actual.tokenvalue))
                            Parser.tokens.selectNext()
                        if (Parser.tokens.actual.tokenvalue == 'ENDFUNC'):
                            Parser.tokens.selectNext()
                            funcargs.append(funcstmts)
                            return FuncDec(funcident, funcargs)
                            # Statements('STATEMENTS', funcstmts)
                        else:
                            raise SyntaxError('Expected "END" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                    else:
                        raise SyntaxError('Expected ENDLINE token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                else:
                    raise SyntaxError('Expected ")" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
            else:
                raise SyntaxError('Expected "(" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
        else:
            raise SyntaxError('Expected "FUNCTION" token, got "%s"' %(Parser.tokens.actual.tokenvalue))


    @staticmethod
    def subDeclaration():
        subargs = [VarDec('VARDEC', [])]
        substmts = Statements('STATEMENTS', [])
        if (Parser.tokens.actual.tokenvalue == 'SUB'):
            Parser.tokens.selectNext()
            subident = Parser.tokens.actual.tokenvalue
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue == '('):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.tokenvalue != ')'):
                    while True:
                        argident = Parser.tokens.actual.tokenvalue
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.tokenvalue == 'AS'):
                            Parser.tokens.selectNext()
                            subargs.append(VarDec('VARDEC', [argident, Parser.varType()]))
                            Parser.tokens.selectNext()
                        else:
                            raise SyntaxError('Expected "AS" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                        if (Parser.tokens.actual.tokenvalue == ','):
                            Parser.tokens.selectNext()
                            continue
                        break
                if (Parser.tokens.actual.tokenvalue == ')'):
                    Parser.tokens.selectNext()
                    subargs[0].children.append(subident)
                    subargs[0].children.append(VarType('SUB'))
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        Parser.tokens.selectNext()
                        while (Parser.tokens.actual.tokenvalue != 'END'):
                            # print(Parser.tokens.actual.tokenvalue)
                            substmts.children.append(Parser.statement())
                            if (Parser.tokens.actual.tokenvalue != '\n'):
                                raise SyntaxError('Expected ENDLINE token after statement, got "%s"' %(Parser.tokens.actual.tokenvalue))
                            Parser.tokens.selectNext()
                        if (Parser.tokens.actual.tokenvalue == 'END'):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.tokenvalue == "SUB"):
                                Parser.tokens.selectNext()
                                subargs.append(substmts)
                                # print('subargs:', subargs)
                                return SubDec(subident, subargs)
                                # Statements('STATEMENTS', funcstmts)
                            else:
                                raise SyntaxError('Expected "SUB" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                        else:
                            raise SyntaxError('Expected "END" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                    else:
                        raise SyntaxError('Expected ENDLINE token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                else:
                    raise SyntaxError('Expected ")" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
            else:
                raise SyntaxError('Expected "(" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
        else:
            raise SyntaxError('Expected "FUNCTION" token, got "%s"' %(Parser.tokens.actual.tokenvalue))



    @staticmethod
    def statement():
        # print('stmt')
        if (Parser.tokens.actual.tokentype == 'COMM'):
            if (Parser.tokens.actual.tokenvalue == 'PRINT'):
                Parser.tokens.selectNext()
                printtree = Print('PRINT', [Parser.relExpression()])
                return printtree
            elif (Parser.tokens.actual.tokenvalue == 'IF'):
                # print()
                Parser.tokens.selectNext()
                iftree = If('IF',[])
                iftree.children.append(Parser.relExpression())
                if (Parser.tokens.actual.tokenvalue == 'THEN'):
                    thentree = Statements('STATEMENTS', [])
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        while (Parser.tokens.actual.tokenvalue == '\n'):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.tokenvalue not in ['ENDIF', 'ELSE']):
                                thentree.children.append(Parser.statement())
                    else:
                        raise SyntaxError('Expected ENDLINE token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                    iftree.children.append(thentree)
                    if (Parser.tokens.actual.tokenvalue == 'ELSE'):
                        elsetree = Statements('STATEMENTS', [])
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.tokenvalue == '\n'):
                            while (Parser.tokens.actual.tokenvalue == '\n'):
                                Parser.tokens.selectNext()
                                if (Parser.tokens.actual.tokenvalue not in ['ENDIF']):
                                    elsetree.children.append(Parser.statement())
                        else:
                            raise SyntaxError('Expected endline token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                        iftree.children.append(elsetree)
                        if (Parser.tokens.actual.tokenvalue == 'ENDIF'):
                            Parser.tokens.selectNext()
                            return iftree
                        else:
                            raise SyntaxError('Expected "ENDIF" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                    elif (Parser.tokens.actual.tokenvalue == 'ENDIF'):
                        Parser.tokens.selectNext()
                        return iftree
                    else:
                        raise SyntaxError('Expected "ENDIF" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                else:
                    raise SyntaxError('Expected "THEN" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
            elif (Parser.tokens.actual.tokenvalue == 'WHILE'):
                Parser.tokens.selectNext()
                whiletree = While('WHILE', [Parser.relExpression()])
                whilestmts = Statements('STATEMENTS', [])
                # whiletree.children.append(Parser.relExpression())
                if (Parser.tokens.actual.tokenvalue == 'DO'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        while (Parser.tokens.actual.tokenvalue == '\n'):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.tokenvalue not in ['ENDLOOP']):
                                whilestmts.children.append(Parser.statement())
                        if (Parser.tokens.actual.tokenvalue == 'ENDLOOP'):
                            Parser.tokens.selectNext()
                            whiletree.children.append(whilestmts)
                            # print('while')
                            return whiletree
                        else:
                            raise SyntaxError('Expected "ENDLOOP" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                    else:
                        raise SyntaxError('Expected endline token, got "%s"' %(Parser.tokens.actual.tokenvalue))
            elif (Parser.tokens.actual.tokenvalue == 'INT' or Parser.tokens.actual.tokenvalue == 'BOOL'):
                funcvartype = Parser.varType()
                if (Parser.tokens.actual.tokentype == 'IDENT'):
                    ident = Parser.tokens.actual.tokenvalue
                    # print(ident)
                    Parser.tokens.selectNext()
                    # print('define', Parser.tokens.actual.tokenvalue)
                    return VarDec('VARDEC', [ident, funcvartype])
                elif (Parser.tokens.actual.tokenvalue == 'FUNC'):
                    return Parser.functionDeclaration(funcvartype)
                else:
                    raise SyntaxError('Expected variable identifier (only alphabetic and "_" characters allowed), got "%s"' %(Parser.tokens.actual.tokenvalue))
            elif (Parser.tokens.actual.tokenvalue == 'CALL'):
                subcall = FuncSubCall()
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.tokentype == 'IDENT'):
                    subcall.value = Parser.tokens.actual
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '('):
                        Parser.tokens.selectNext()
                        while (Parser.tokens.actual.tokenvalue != ')'):
                            subcall.children.append(Parser.relExpression())
                            if (Parser.tokens.actual.tokenvalue == ','):
                                Parser.tokens.selectNext()
                                continue
                            break
                        if (Parser.tokens.actual.tokenvalue != ')'):
                            raise SyntaxError('Expected ")" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
                        return subcall
                    else:
                        raise SyntaxError('Expected token "(", got "%s"' %(Parser.tokens.actual.tokenvalue))
                else:
                    raise SyntaxError('Expected variable identifier, got "%s"' %(Parser.tokens.actual.tokenvalue))
            else:
                raise SyntaxError('Expected command, got "%s"' %(Parser.tokens.actual.tokenvalue))
        elif (Parser.tokens.actual.tokentype == 'IDENT'):
            ident = Parser.tokens.actual
            # print('ident: ', ident.tokenvalue)
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokentype == 'ASSIG'):
                # print('assig')
                Parser.tokens.selectNext()
                # print(Parser.tokens.actual.tokenvalue)
                # print(relvalue.children)
                assigtree = Assignment('ASSIG', [Identifier(ident.tokenvalue), Parser.relExpression()])
                # print('assig:', Parser.tokens.actual.tokenvalue)
                return assigtree
            else:
                raise SyntaxError('Expected assignment token "=", got "%s"' %(Parser.tokens.actual.tokenvalue))
        else:
            return NoOp()



    @staticmethod
    def program():
        program = []
        program.append(Parser.statement())
        # Parser.tokens.selectNext()
        while (Parser.tokens.actual.tokenvalue == '\n'):
            # print('while')
            Parser.tokens.selectNext()
            program.append(Parser.statement())
            # Parser.tokens.selectNext()
        # if (Parser.tokens.actual.tokenvalue == 'SUB' or Parser.tokens.actual.tokenvalue == 'FUNCTION'):
        #     while (Parser.tokens.actual.tokenvalue == 'SUB' or Parser.tokens.actual.tokenvalue == 'FUNCTION'):
        #         if (Parser.tokens.actual.tokenvalue == 'SUB'):
        #             program.append(Parser.subDeclaration())
            # while (Parser.tokens.actual.tokenvalue == '\n'):
                # else:
                #     program.append(Parser.functionDeclaration())
                #     # print('oi')
                #     while (Parser.tokens.actual.tokenvalue == '\n'):
                #         Parser.tokens.selectNext()
        # else:
        #     raise SyntaxError('Expected "Sub" or "Function" token, got "%s"' %(Parser.tokens.actual.tokenvalue))
        # program.append(FuncSubCall('MAIN', []))
        return Program('PROGRAM', program)

    @staticmethod
    def relExpression():
        expr1 = Parser.parserExpression()
        op = Parser.tokens.actual
        if (op.tokenvalue in ['EQUALS', 'LESS', 'GREATER']):
            relop = BinOp(op.tokenvalue, [expr1])
            Parser.tokens.selectNext()
            expr2 = Parser.parserExpression()
            relop.children.append(expr2)
            return relop
        else:
            return expr1

    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.program()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended before EOF')

'''Rotina de Testes'''
file = sys.argv[1]
# file = './test.vbs'
with open(file, 'r', encoding='utf-8') as infile:
    lines = infile.read()

st = SymbolTable()
Parser.run(lines).Evaluate(st)
