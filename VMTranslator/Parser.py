"""No comment"""

import sys
import Lexer


class Parser:
    """lit et analyse le texte pour extraire les informations les plus utiles """

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.command = self._read()

    def next(self):
        """permet d'obtenir l'élément suivant """
        res = self.command
        self.command = self._read()
        return res

    def look(self):
        """trouve et affiche les données selon un mot clé"""
        return self.command

    def hasNext(self):
        """permet de vérifier si il y'a un élément suivant à lire."""
        return self.command is not None

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration

    def _read(self):
        """lit le contenu du fichier et le renvoie sous forme d'un texte """
        command = self.lexer.look()
        if command is None:
            return None
        else:
            type = command['type']
            match type:
                case 'pushpop':
                    return self._commandpushpop()
                case 'branching':
                    return self._commandbranching()
                case 'arithmetic':
                    return self._commandarithmetic()
                case 'function':
                    return self._commandfunction()
                case 'return':
                    return self._commandreturn()
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandarithmetic(self):
        """"""
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}

    def _commandpushpop(self):
        """"""
        command = self.lexer.next()
        segment = self.lexer.next()
        parameter = self.lexer.next()
        if segment is None or parameter is None or segment['type'] != 'segment' or parameter['type'] != 'int':
            print(f'SyntaxError (line={command["line"]}, col={command["col"]}): {command["token"]}')
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'segment': segment['token'], 'parameter': parameter['token']}

    def _commandbranching(self):
        """"""
        command = self.lexer.next()
        label = self.lexer.next()
        if label is None or label['type'] != 'string':
            print("t")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'label': label['token']}

    def _commandfunction(self):
        """crée un bloc de code qu'on l'on peut utiliser plusieurs fois dans le programme"""
        command = self.lexer.next()
        name = self.lexer.next()
        parameter = self.lexer.next()
        if name is None or parameter is None or name['type'] != 'string' or parameter['type'] != 'int':
            print("error")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'function': name['token'], 'parameter': parameter['token']}

    def _commandreturn(self):
        """renvoie la valeur de la fonction et termine son exécution """
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = Parser(file)
    for command in parser:
        print(command)
    print('-----fin')
