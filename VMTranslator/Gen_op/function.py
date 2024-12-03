from . import pushpop
from . import goto

class func :

    def __init__(self, classname='Bob'):
        self.classname = classname
        self.cpt=0
        self.pushpop=pushpop.Pushpop(self.classname)
        self.goto = goto.Goto(self.classname)

    def _commandcall(self, command):
        """No comment"""
        return f"""\n\t//{command['type']} {command['function']} {command['parameter']}
        {self.pushpop._commandpushconstant({'type':'push','segment':'constant', 'parameter':'retAddrLabel'})}
        //push LCL
        @LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push ARG
        @ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push THIS
        @THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push THAT
        @THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @SP
        D=M
        @LCL
        M=D
        @5
        D=D-A
        @{command['parameter']}
        D=D-A
        @ARG
        M=D
        {self.goto._commandgoto({'type':'goto','label':command['function']})}
        {self.goto._commandlabel({'type':'label','label':'retAddrLabel'})}\n"""

    def _commandFunction(self, command):
        """No comment"""
        return f"""\n\t//{command['type']} {command['function']} {command['parameter']}
        ({command['function']})
        \n""" + int(command['parameter'])*f"\t{self.pushpop._commandpushconstant({'type':'push','segment':'constant', 'parameter':'0'})}\n"

    def _commandReturn(self, command):
        """No comment"""
        return f"""\t//{command['type']}
    //endFrame=LCL
    @LCL
    D=M
    @R13
    M=D
    //retAddr=*(endFrame-5)
    @R13
    D=M
    @5
    D=D-A
    A=D
    D=M
    @R14
    M=D
    //*ARG=pop()
    @SP
    M=M-1
    A=M
    D=M
    @ARG
    A=M
    M=D
    //SP=ARG+1
    @ARG
    D=M+1
    @SP
    M=D
    //THAT = *(endFrame – 1) 
    @R13
    A=M-1
    D=M
    @THAT
    M=D
    //THIS = *(endFrame – 2)
    @R13
    D=M
    @2
    A=D-A
    D=M
    @THIS
    M=D
    //ARG=*(endFrame-3)
    @R13
    D=M
    @3
    A=D-A
    D=M
    @ARG
    M=D
    //LCL = *(endFrame – 4) 
    @R13
    D=M
    @4
    A=D-A
    D=M
    @LCL
    M=D 
    //goto retAddr 
    @R14
    A=M
    0;JMP
    """
