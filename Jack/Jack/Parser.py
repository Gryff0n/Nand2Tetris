import sys

from Cython import returns
from click import argument
from fontTools.ttLib.tables.ttProgram import instructions
from libfuturize.fixes.fix_execfile import expression

import Lexer
import todot


class Parser:
    """No comment"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)

    def jackclass(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        token=self.lexer.look()
        vardec=[]
        subroutine=[]
        self.process('class')
        Name=self.className()
        self.process('{')
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['static', 'field']:
            vardec+=self.classVarDec()
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['constructor', 'function', 'method']:
            subroutine.append(self.subroutineDec())
        self.process('}')

        return {'line':token['line'],'col':token['col'],'type':'class','name':Name,'vardec':vardec,'subroutine':subroutine}

    def classVarDec(self):
        """
        classVarDec: ('static'| 'field') type varName (',' varName)* ';'
        """
        token=self.lexer.look()
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['static', 'field']:
            kind=self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        type=self.type()
        Name = []
        Name.append(self.varName())
        while self.lexer.hasNext() and self.lexer.look()['token'] ==',':
            self.process(',')
            Name.append(self.varName())
        self.process(';')
        ans=[]
        for name in Name :
            ans.append({'line':token['line'],'col':token['col'],'type':type,'name':name,'kind':kind})
        return ans

    def type(self):
        """
        type: 'int'|'char'|'boolean'|className
        """
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['int', 'char', 'boolean']:
             return self.lexer.next()['token']
        else:
            return self.className()


    def subroutineDec(self):
        """
        subroutineDec: ('constructor'| 'function'|'method') ('void'|type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        token = self.lexer.look()
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['constructor', 'function','method']:
            type=self.lexer.next()['token']
        else:
            self.error(self.lexer.look()['token'])
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['void']:
            typereturn =self.process(self.lexer.look()['token'])
        else :
            typereturn =self.type()
        name=self.className()
        self.process('(')
        argument=self.parameterList()
        self.process(')')
        local,instructions=self.subroutineBody()

        return {'line': token['line'], 'col': token['col'], 'type': type, 'return': typereturn, 'name': name, 'argument' : argument, 'local':local, 'instructions': instructions}

    def parameterList(self):
        """
        parameterList: ((type varName) (',' type varName)*)?
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        res=[]
        if self.lexer.hasNext() and self.lexer.look()['token'] != ')':
            type=self.type()
            varName=self.varName()
            res=[{'line': line, 'col': col, 'name': varName, 'kind': 'argument', 'type': type}]
            while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
                self.process(',')
                type=self.type()
                varname=self.varName()
                res.append({'line': line, 'col': col, 'name': varName, 'kind': 'argument', 'type': type})
        return res

    def subroutineBody(self):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.process('{')
        variables=[]
        while self.lexer.hasNext() and self.lexer.look()['token'] == 'var':
            variables+=self.varDec()
        statements=self.statements()
        self.process('}')
        return variables,statements

    def varDec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        """
        variables=[]
        self.process('var')
        varType=self.type()
        name=self.varName()
        variables.append({'type': varType, 'name': name})
        while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
            self.process(',')
            name=self.varName()
            variables.append({'type': varType, 'name': name})
        self.process(';')
        return variables

    def className(self):
        """
        className: identifier
        """
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            return self.lexer.next()['token']
        else:
            self.error(self.lexer.look()['token'])

    def subroutineName(self):
        """
        subroutineName: identifier
        """
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            return self.lexer.next()['token']
        else:
            self.error(self.lexer.look()['token'])

    def varName(self):
        """
        varName: identifier
        """
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            return self.lexer.next()['token']
        else:
            self.error(self.lexer.look()['token'])


    def statements(self):
        """
        statements : statements*
        """
        statements=[]
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['let', 'if', 'while','do','return']:
            statements.append(self.statement())
        return statements

    def statement(self):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """

        if self.lexer.look()['token'] == 'let':
            st=self.letStatement()
        elif self.lexer.look()['token'] == 'if':
            st=self.ifStatement()
        elif self.lexer.look()['token'] == 'while':
            st=self.whileStatement()
        elif self.lexer.look()['token'] == 'do':
            st=self.doStatement()
        else:
            st=self.returnStatement()
        return st

    def letStatement(self):
        """
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        expression1=None
        self.process('let')
        name=self.varName()
        if self.lexer.hasNext() and self.lexer.look()['token'] == '[':
            self.process('[')
            expression1=self.expression()
            self.process(']')
        self.process('=')
        expression2=self.expression()
        self.process(';')
        if expression1 is None :
            return {'line': line, 'col': col, 'type': 'let', 'variable': name,'valeur': expression2}
        return {'line':line, 'col': col,'type': 'let', 'variable': name, 'indice': expression1, 'valeur':expression2}

    def ifStatement(self):
        """
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        false=None
        self.process('if')
        self.process('(')
        cond=self.expression()
        self.process(')')
        self.process('{')
        true=self.statements()
        self.process('}')
        if self.lexer.hasNext() and self.lexer.look()['token'] == 'else':
            self.process('else')
            self.process('{')
            false=self.statements()
            self.process('}')
        if false is None:
            return {'line': line, 'col': col, 'type': 'if', 'condition': cond, 'true': true}
        return {'line':line, 'col': col,'type': 'if', 'condition': cond, 'true': true, 'false':false}

    def whileStatement(self):
        """
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        self.process('while')
        self.process('(')
        cond=self.expression()
        self.process(')')
        self.process('{')
        instructions=self.statements()
        self.process('}')
        return {'line':line, 'col': col,'type': 'if', 'condition': cond, 'instruction':instructions}

    def doStatement(self):
        """
        doStatement : 'do' subroutineCall ';'
        """
        self.process('do')
        self.subroutineCall()
        self.process(';')

    def returnStatement(self):
        """
        returnStatement : 'return' expression? ';'
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        expression=None
        self.process('return')
        if self.lexer.hasNext() and self.lexer.look()['token'] == ';':
            self.process(';')
        else:
            expression=self.expression()
            self.process(';')
        if expression is None:
            return {'line': line, 'col': col, 'type': 'return'}
        return {'line':line, 'col': col,'type': 'return', 'valeur':expression}

    def expression(self):
        """
        expression : term (op term)*
        """
        exp=[self.term()]
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            exp.append(self.op())
            exp.append(self.term())
        return exp

    def term(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        res={}
        res["line"]=self.lexer.look()['line']
        res["col"]=self.lexer.look()['col']
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['true', 'false', 'null', 'this']:
            res["type"]="constant"
            res["val"]=self.KeywordConstant()
            return res
        elif self.lexer.hasNext() and self.lexer.look()['token'] in ['-', '~']:
            res["type"]=self.lexer.next()['token']
            res["valeur"]=self.term()
            return res
        elif self.lexer.hasNext() and self.lexer.look()['token'] == '(':
            self.process('(')
            res["type"]="expression"
            res["valeur"]=self.expression()
            self.process(')')
            return res
        elif self.lexer.hasNext() and self.lexer.look()['type'] in ['StringConstant', 'IntegerConstant']:
            token=self.lexer.next()
            res["type"]=token['type']
            res["valeur"]=token['token']
            return res
        elif self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            if self.lexer.hasNext() and self.lexer.look2()['token'] == '[':
                res["type"]="tableau"
                res["valeur"]=self.varName()
                self.process('[')
                res["indice"]=self.expression()
                self.process(']')
                return res
            elif self.lexer.hasNext() and self.lexer.look2()['token'] in ['(', '.']:
                res["type"]="subroutineCall"
                res["valeur"]=self.subroutineCall()
                return res
            else:
                res["valeur"]=self.varName()
                res["type"]="variable"
                return res

    def subroutineCall(self):
        """
        subroutineCall : subroutineName '(' expressionList ')'
                | (className|varName) '.' subroutineName '(' expressionList ')'
        Attention : l'analyse syntaxique ne peut pas distingué className et varName.
            Nous utiliserons la balise <classvarName> pour (className|varName)
        """
        line=self.lexer.look()['line']
        col=self.lexer.look()['col']
        if self.lexer.hasNext() and self.lexer.look2()['token'] == '(':
            subName=self.subroutineName()
            self.process('(')
            expression=self.expressionList()
            self.process(')')
        else:
            self.className()
            self.process('.')
            subName=self.subroutineName()
            self.process('(')
            expression=self.expressionList()
            self.process(')')
        return {'line':line, 'col': col,'type': 'do', 'classvar': 'classvarName', 'name':subName, 'argument':expression}

    def expressionList(self):
        """
        expressionList : (expression (',' expression)*)?
        """
        expressions=[]
        if self.lexer.hasNext() and self.lexer.look()['token'] != ')':
            expressions.append(self.expression())
            while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
                self.process(',')
                expressions.append(self.expression())
        return expressions

    def op(self):
        """
        op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        return self.lexer.next()['token']

    def unaryOp(self):
        """
        unaryop : '-'|'~'
        """
        return self.lexer.next()['token']

    def KeywordConstant(self):
        """
        KeyWordConstant : 'true'|'false'|'null'|'this'
        """
        return self.lexer.next()['token']

    def process(self, str):
        token = self.lexer.next()
        if (token is not None and token['token'] == str):
            return token
        else:
            self.error(token)

    def error(self, token):
        if token is None:
            print("Syntax error: end of file")
        else:
            print(f"SyntaxError (line={token['line']}, col={token['col']}): {token['token']}")
        exit()


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = Parser(file)
    arbre = parser.jackclass()
    todot = todot.Todot(file)
    todot.todot(arbre)
    print('-----fin')
