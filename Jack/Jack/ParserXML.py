import sys
import Lexer


class ParserXML:
    """No comment"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.xml = open(file[0:-5] + ".xml", "w")
        self.xml.write('<?xml version="1.0" encoding="UTF-8"?>')

    def jackclass(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.xml.write(f"""<class>\n""")
        self.process('class')
        self.className()
        self.process('{')
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['static','field']:
            self.classVarDec()
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['constructor','function','method']:
            self.subroutineDec()
        self.process('}')
        self.xml.write(f"""</class>\n""")

    def classVarDec(self):
        """
        classVarDec: ('static'| 'field') type varName (',' varName)* ';'
        """
        self.xml.write(f"""<classVarDec>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['static', 'field']:
            self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        self.type()
        self.varName()
        while self.lexer.hasNext() and self.lexer.look()['token'] ==',':
            self.process(',')
            self.varName()
        self.process(';')
        self.xml.write(f"""</classVarDec>\n""")

    def type(self):
        """
        type: 'int'|'char'|'boolean'|className
        """
        self.xml.write(f"""<type>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['int', 'char', 'boolean']:
            self.process(self.lexer.look()['token'])
        else:
            self.className()
        self.xml.write(f"""</type>\n""")

    def subroutineDec(self):
        """
        subroutineDec: ('constructor'| 'function'|'method') ('void'|type)
        subroutineName '(' parameterList ')' subroutineBody
        """
        self.xml.write(f"""<subroutineDec>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['constructor', 'function', 'method']:
            self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        if self.lexer.hasNext() and self.lexer.look()['token'] == 'void':
            self.process(self.lexer.look()['token'])
        else:
            self.type()
        self.subroutineName()
        self.process('(')
        self.parameterList()
        self.process(')')
        self.subroutineBody()
        self.xml.write(f"""</subroutineDec>\n""")

    def parameterList(self):
        """
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.xml.write(f"""<parameterList>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] != ')':
            self.type()
            self.varName()
            while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
                self.process(',')
                self.type()
                self.varName()
        self.xml.write(f"""</parameterList>\n""")

    def subroutineBody(self):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        self.xml.write(f"""<subroutineBody>\n""")
        self.process('{')
        while self.lexer.hasNext() and self.lexer.look()['token'] == 'var':
            self.varDec()
        self.statements()
        self.process('}')
        self.xml.write(f"""</subroutineBody>\n""")

    def varDec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.xml.write(f"""<varDec>\n""")
        self.process('var')
        self.type()
        self.varName()
        while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
            self.process(',')
            self.varName()
        self.process(';')
        self.xml.write(f"""</varDec>\n""")

    def className(self):
        """
        className: identifier
        """
        self.xml.write(f"""<className>""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        self.xml.write(f"""</className>""")

    def subroutineName(self):
        """
        subroutineName: identifier
        """
        self.xml.write(f"""<subroutineName>""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        self.xml.write(f"""</subroutineName>""")

    def varName(self):
        """
        varName: identifier
        """
        self.xml.write(f"""<varName>\n""")
        if self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            self.process(self.lexer.look()['token'])
        else:
            self.error(self.lexer.look()['token'])
        self.xml.write(f"""</varName>\n""")

    def statements(self):
        """
        statements : statements*
        """
        self.xml.write(f"""<statements>\n""")
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['let', 'if', 'while','do','return']:
            self.statement()
        self.xml.write(f"""</statements>\n""")

    def statement(self):
        """
        statement : letStatements|ifStatement|whileStatement|doStatement|returnStatement
        """
        self.xml.write(f"""<statement>\n""")

        if self.lexer.look()['token'] == 'let':
            self.letStatement()
        elif self.lexer.look()['token'] == 'if':
            self.ifStatement()
        elif self.lexer.look()['token'] == 'while':
            self.whileStatement()
        elif self.lexer.look()['token'] == 'do':
            self.doStatement()
        else:
            self.returnStatement()

        self.xml.write(f"""</statement>\n""")

    def letStatement(self):
        """
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.xml.write(f"""<letStatement>\n""")
        self.process('let')
        self.varName()
        if self.lexer.hasNext() and self.lexer.look()['token'] == '[':
            self.process('[')
            self.expression()
            self.process(']')
        self.process('=')
        self.expression()
        self.process(';')
        self.xml.write(f"""</letStatement>\n""")

    def ifStatement(self):
        """
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.xml.write(f"""<ifStatement>\n""")
        self.process('if')
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')
        if self.lexer.hasNext() and self.lexer.look()['token'] == 'else':
            self.process('else')
            self.process('{')
            self.statements()
            self.process('}')
        self.xml.write(f"""</ifStatement>\n""")

    def whileStatement(self):
        """
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        self.xml.write(f"""<whileStatement>\n""")
        self.process('while')
        self.process('(')
        self.expression()
        self.process(')')
        self.process('{')
        self.statements()
        self.process('}')
        self.xml.write(f"""</whileStatement>\n""")

    def doStatement(self):
        """
        doStatement : 'do' subroutineCall ';'
        """
        self.xml.write(f"""<doStatement>\n""")
        self.process('do')
        self.subroutineCall()
        self.process(';')
        self.xml.write(f"""</doStatement>\n""")

    def returnStatement(self):
        """
        returnStatement : 'return' expression? ';'
        """
        self.xml.write(f"""<returnStatement>\n""")
        self.process('return')
        if self.lexer.hasNext() and self.lexer.look()['token'] == ';':
            self.process(';')
        else:
            self.expression()
            self.process(';')
        self.xml.write(f"""</returnStatement>\n""")

    def expression(self):
        """
        expression : term (op term)*
        """
        self.xml.write(f"""<expression>\n""")
        self.term()
        while self.lexer.hasNext() and self.lexer.look()['token'] in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.op()
            self.term()
        self.xml.write(f"""</expression>\n""")

    def term(self):
        """
        term : integerConstant|stringConstant|keywordConstant
                |varName|varName '[' expression ']'|subroutineCall
                | '(' expression ')' | unaryOp term
        """
        self.xml.write(f"""<term>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] in ['true', 'false', 'null', 'this']:
            self.KeywordConstant()
        elif self.lexer.hasNext() and self.lexer.look()['token'] in ['-','~']:
            self.unaryOp()
            self.term()
        elif self.lexer.hasNext() and self.lexer.look()['token'] == '(':
            self.process('(')
            self.expression()
            self.process(')')
        elif self.lexer.hasNext() and self.lexer.look()['type'] in ['StringConstant', 'IntegerConstant']:
            self.process(self.lexer.look()['token'])
        elif self.lexer.hasNext() and self.lexer.look()['type'] == 'identifier':
            if self.lexer.hasNext() and self.lexer.look2()['token'] == '[':
                self.varName()
                self.process('[')
                self.expression()
                self.process(']')
            elif self.lexer.hasNext() and self.lexer.look2()['token'] in ['(','.']:
                self.subroutineCall()
            else:
                self.varName()
        self.xml.write(f"""</term>\n""")

    def subroutineCall(self):
        """
        subroutineCall : subroutineName '(' expressionList ')'
                | (className|varName) '.' subroutineName '(' expressionList ')'
        Attention : l'analyse syntaxique ne peut pas distingué className et varName.
            Nous utiliserons la balise <classvarName> pour (className|varName)
        """
        self.xml.write(f"""<subroutineCall>\n""")
        if self.lexer.hasNext() and self.lexer.look2()['token'] == '(':
            self.subroutineName()
            self.process('(')
            self.expressionList()
            self.process(')')
        else:
            self.className()
            self.process('.')
            self.subroutineName()
            self.process('(')
            self.expressionList()
            self.process(')')
        self.xml.write(f"""</subroutineCall>\n""")

    def expressionList(self):
        """
        expressionList : (expression (',' expression)*)?
        """
        self.xml.write(f"""<expressionList>\n""")
        if self.lexer.hasNext() and self.lexer.look()['token'] != ')':
            self.expression()
            while self.lexer.hasNext() and self.lexer.look()['token'] == ',':
                self.process(',')
                self.expression()
        self.xml.write(f"""</expressionList>\n""")

    def op(self):
        """
        op : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        """
        self.xml.write(f"""<op>\n""")
        self.process(self.lexer.look()['token'])
        self.xml.write(f"""</op>\n""")

    def unaryOp(self):
        """
        unaryop : '-'|'~'
        """
        self.xml.write(f"""<unaryop>\n""")
        self.process(self.lexer.look()['token'])
        self.xml.write(f"""</unaryop>\n""")

    def KeywordConstant(self):
        """

        KeyWordConstant : 'true'|'false'|'null'|'this'
        """
        self.xml.write(f"""<KeyWordConstant>\n""")
        self.process(self.lexer.look()['token'])
        self.xml.write(f"""</KeyWordConstant>\n""")

    def process(self, str):
        token = self.lexer.next()
        if (token is not None and token['token'] == str):
            self.xml.write(f"""<{token['type']}>{token['token']}</{token['type']}>\n""")
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
    parser = ParserXML(file)
    parser.jackclass()
    print('-----fin')
