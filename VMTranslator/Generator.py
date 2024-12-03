"""No comment"""

import sys
import Parser
from Gen_op import arith, function, pushpop, goto


class Generator:
    """No comment"""

    def __init__(self, file='Bob.vm'):
        """No comment"""
        self.classname=file[0:-3]
        self.calc= arith.Arith()
        self.pushpop= pushpop.Pushpop(self.classname)
        self.func = function.func(self.classname)
        self.branching=goto.Goto()
        if file is not None:
            self.parser = Parser.Parser(file)

    def __iter__(self):
        return self

    def __next__(self):
        if self.parser is not None and self.parser.hasNext():
            return self._next()
        else:
            raise StopIteration

    def _next(self):
        # No comment
        command = self.parser.next()
        if command is None:
            return None
        else:
            type = command['type']
            # type = push|pop|
            #        add|sub|neg|eq|gt|lt|and|or|not) |
            #        label|goto|if-goto|
            #        Function|Call|return

            match type:
                # Faire une fonction par type de commande
                case 'push':
                    return self.pushpop._commandpush(command)
                case 'pop' :
                    return self.pushpop._commandpop(command)
                case 'call':
                    return self.func._commandcall(command)
                case 'add':
                    return self.calc._commandadd(command)
                case 'sub':
                    return self.calc._commandadd(command)
                case 'neg':
                    return self.calc._commandneg(command)
                case 'eq':
                    return self.calc._commandcomp(command)
                case 'gt':
                    return self.calc._commandcomp(command)
                case 'lt':
                    return self.calc._commandcomp(command)
                case 'and':
                    return self.calc._commandadd(command)
                case 'or':
                    return self.calc._commandadd(command)
                case 'not':
                    return self.calc._commandneg(command)
                case 'label':
                    return self.branching._commandlabel(command)
                case 'goto':
                    return self.branching._commandgoto(command)
                case 'if-goto':
                    return self.branching._commandifgoto(command)
                case 'function':
                    return self.func._commandFunction(command)
                case 'return':
                    return self.func._commandReturn(command)
                case _:
                    print(f'SyntaxError : {command}')
                    exit()

    def _commandcall(self, command):
        return self.func._commandcall(command)

if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print("""
    @FIN
    (FIN)
    0;JMP
    -----fin""")
