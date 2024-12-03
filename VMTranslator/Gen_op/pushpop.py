


class Pushpop :
    def __init__(self,classname='Bob'):
        self.classname = classname
        self.dict = {'local': 1, 'argument': 2, 'this': 3, 'that': 4}
        self.pointer = {0:'THIS', 1:'THAT'}



    def _commandpush(self, command):
        """No comment"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'constant':
                return self._commandpushconstant(command)
            case 'local'|'this'|'argument'|'that':
                return self._commandpushsegment(command)
            case 'static' :
                return self._commandpushstatic(command)
            case 'temp':
                return self._commandpushtemp(command)
            case 'pointer':
                return self.commandpushpointer(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandpop(self, command):
        """No comment"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'local'|'this'|'argument'|'that':
                return self._commandpopsegment(command)
            case 'static' :
                return self._commandpopstatic(command)
            case 'temp':
                return self._commandpoptemp(command)
            case 'pointer':
                return self.commandpoppointer(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandpushconstant(self, command):
        """No comment"""
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1\n"""

    def _commandpushsegment(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @{self.dict[command['segment']]}
        A=M
        """ + (int(parameter))*"A=A+1"+ f"""
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1\n"""

    def _commandpopsegment(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        A=M
        D=M
        @{self.dict[command['segment']]}
        A=M
        """ + (int(parameter))*"A=A+1"+f"""
        M=D"""

    def _commandpopstatic(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        A=M
        D=M
        @{self.classname}.{parameter}
        M=D"""

    def _commandpushstatic(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @{self.classname}.{parameter}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1\n"""

    def _commandpoptemp(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        A=M
        D=M
        @{str(int(parameter)+5)}
        M=D"""

    def _commandpushtemp(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @{str(int(parameter)+5)}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1\n"""

    def _commandpushpointer(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @{self.pointer[parameter]}
        A=M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1"""

    def commandpoppointer(self, command):
        parameter = command['parameter']
        return f"""\n\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        A=M
        D=M
        @{self.pointer[parameter]}
        A=M
        M=D
        """

