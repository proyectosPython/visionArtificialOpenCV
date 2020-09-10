import sys
from agentes import Servidor
from agentes import Cliente

class Main():
    def __init__(self):
        self.servidor = Servidor.Servidor()
        self.cli1 = Cliente.Cliente(1)
        self.cli2 = Cliente.Cliente(2)

        self.servidor.daemon = True
        self.cli1.daemon = True
        self.cli2.daemon = True


        self.servidor.start()
        self.cli1.start()
        self.cli2.start()

        while True:
            msg = input('>>')
            if msg == 'salir':
                sys.exit()
            else:
                pass

main = Main()