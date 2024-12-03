


class Arith :
    def __init__(self,classname='Bob'):
        self.classname = classname
        self.cpt=0
        self.dict = {'eq': 'JNE', 'gt': 'JLE', 'lt': 'JGE','neg': '-', 'not': '!','add': '+', 'sub': '-', 'or': '|', 'and': '&'}

    def _commandadd(self, command):
        """permet d'ajouter des données à un fichier "existant  """
        return f"""\t//{command['type']}
        @SP
        M=M-1
        M=M-1              
        A=M
        D=M
        @SP
        A=M+1
        D=D{self.dict[command['type']]}M
        @SP
        A=M
        M=D
        @SP
        M=M+1"""


    def _commandneg(self, command):
        """inverser le signe d'une valeure numérique """
        return f"""\n\t//{command['type']}
        @SP
        M=M-1
        A=M
        M={self.dict[command['type']]}M\n"""

    def _commandcomp(self, command):
        """compare deux valeurs , si elles sont égales ça retourne vrai sinon faux"""
        self.cpt+=1
        return f"""\n\t//{command['type']}
        @SP
        A=M-1
        D=M
        A=A-1
        D=D-M
        @{self.classname}$END${self.cpt}
        D;{self.dict[command['type']]}
        @SP
        A=M
        M=-1
        ({self.classname}$END${self.cpt})
        """

