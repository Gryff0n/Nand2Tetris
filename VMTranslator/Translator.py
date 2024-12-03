"""No comment"""
import os
import glob
import sys

import Generator


class Translator:
    """conversion et traduction des données d'un format , d'un langage ou d'une representation a un autre """

    def __init__(self, files, asm):
        self.asm = open(asm, "w")
        self.files = files

    def translate(self):
        """remplace des caractéres spécifiques d'une chaine de texte par d'autres selon une table de correspodance définie """
        self.asm.write(self._bootstrap())
        # os.listdir("/home/olivier")
        if os.path.isfile(self.files):
            self._translateonefile(self.files)
        else:
            if os.path.isdir(self.files):
                for file in glob.glob(f'{self.files}/*.vm'):
                    self._translateonefile(file)
        self.asm.write(self._reverseBootstrap())

    def _translateonefile(self, file):
        """"""
        self.asm.write(f"""\n//code de {file}\n""")
        generator = Generator.Generator(file)
        for command in generator:
            self.asm.write(command)

    def _reverseBootstrap(self):
        """restaurer l'état précedant d'un système en inversant le processus d'initialisation """
        return """
// End
    @FIN
    (FIN)
    0;JMP"""

    def _bootstrap(self):
        """mettre en place tout ce qu'il faut pour assurer le démarrage du fichier en chargeant les paramétres """
        init = Generator.Generator()._commandcall({'type': 'Call', 'function': 'Sys.init', 'parameter': '0'})

        return f"""// Bootstrap
    @256
    D=A
    @SP
    M=D
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Translotor.py <vm file| dir> <asm file>")
    else:
        vmfiles=sys.argv[1]
        asmfile=sys.argv[2]
        translator = Translator(vmfiles,asmfile)
        translator.translate()
