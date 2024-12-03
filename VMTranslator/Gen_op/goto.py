

class Goto :

    def __init__(self, classname='Bob'):
        self.classname = classname

    def _commandlabel(self, command):
        """No comment"""
        return f"""\t//{command['type']} {command['label']}
    ({command['label']})\n"""

    def _commandgoto(self, command):
        """No comment"""
        return f"""\t//{command['type']} {command['label']}
        @{command['label']}
        0;JMP
        """

    def _commandifgoto(self, command):
        """No comment"""
        return f"""\t//{command['type']} {command['label']}
    @SP
    M=M-1
    A=M+1
    D=M
    @{command['label']}
    D;JNE
    """