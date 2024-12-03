"""No comment"""

import os
import sys


class Reader:
    """Initialisation de la lecture et ouverture
    du fichier en mode lecture"""

    def __init__(self, file):
        self.char = None
        self._line = 1
        self._col = 1
        if os.path.exists(file):
            self.file = open(file, "r")
            self.char = self.file.read(1)

    def look(self):
        """getter de position dans le fichier texte.
        Quelle ligne, colonne et quel est le caractère"""
        return {'line': self._line, 'col': self._col, 'char': self.char}

    def next(self):
        """On avance dans le texte en mettant toujours a jour notre position dans celui-ci,
        et on renvoie notre position et le caractère lu."""
        res = {'line': self._line, 'col': self._col, 'char': self.char}
        if self.hasNext():
            if self.char == '\n':
                self._line += 1
                self._col = 1
            else:
                self._col += 1
            self.char = self.file.read(1)
            if not self.hasNext():
                self.file.close()
        return res

    def hasNext(self):
        """Vérifie que l'on est toujours sur un caractère du texte et que l'on
        est pas a la fin"""
        if self.char:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    lecteur = Reader(file)
    for c in lecteur:
        print(c)
    print('-----fin')
