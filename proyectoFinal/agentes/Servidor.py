import socket
import threading
import pickle

class Servidor(threading.Thread):
    def __init__(self, host="localhost", port=4000):
        threading.Thread.__init__(self)
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)
        self.unidades = 0

        aceptar = threading.Thread(target=self.aceptarConeccion)
        procesar = threading.Thread(target=self.procesarConeccion)

        aceptar.daemon = True
        aceptar.start()
        procesar.daemon = True
        procesar.start()


    def run(self):
        threadName = threading.currentThread().getName()
        #print("Hello, I am the thread %s" % threadName)
        while True:
            '''msg = input('>>')
            if msg == 'salir':
                self.sock.close()
                sys.exit()
            else:
                pass'''
            pass

    def aceptarConeccion(self):
        print("aceptar conneccion ha iniciado",end="\n")
        while True:
            try:
                conn, addr = self.sock.accept()
                aux = "id cliente: "+ str(addr[1])
                print(aux)
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarConeccion(self):
        print("Procesar connecciones ha iniciado",end="\n")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            mensaje = pickle.loads(data)
                            try:
                                unidades = int(mensaje)
                                self.unidades = self.unidades + unidades

                                aux = "** server ** resultado de procesar imagen por id cliente : " + str(c) + " --> " + str(unidades)
                                print(aux)
                            except:
                                self.msg_to_all(mensaje,c)
                    except:
                        pass

    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(pickle.dumps(msg))
            except:
                self.clientes.remove(c)
                #pass



