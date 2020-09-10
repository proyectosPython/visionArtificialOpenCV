import socket
import threading
import sys
import pickle

class Servidor(threading.Thread):
    def __init__(self, host="localhost", port=4000):
        threading.Thread.__init__(self)
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)



    def run(self):
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon = True
        aceptar.start()
        procesar.daemon = True
        procesar.start()

        while True:
            msg = input('->')
            if msg == 'salir':
                self.sock.close()
                sys.exit()
            elif msg == 'iniciar':
                print("num clientes: ",len(self.clientes))
                for i in range(2):
                    try:
                        self.clientes[i].send(pickle.dumps(nums[i]))
                    except Exception as e:
                        print("error", e)
                        self.clientes.remove(self.clientes[i])
            else:
                pass


    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)

    def aceptarCon(self):
        print("aceptar conneccion ha iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                print("dir: ", addr)
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarCon(self):
        print("Procesar connecciones ha iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data,c)
                            #rint("fact = ", pickle.loads(data))
                    except:
                        pass


