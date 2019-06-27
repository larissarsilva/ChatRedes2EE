from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def aceitar_cliente():

    while True:

        client, client_address = SERVER.accept() #Cria um novo socket TCP/IP com o endereço da maquina do cliente
        print("%s:%s Se conectouu." % client_address)
        client.send(bytes("Digite seu nome:", "utf8"))
        addresses[client] = client_address
        #print(addresses)
        Thread(target=tratamento_conexao, args=(client,)).start()


def tratamento_conexao(client):
    """Trata individualmente as conexões."""

    name = client.recv(1024).decode("utf8") #Decodifica os bytes recebidos
    saudacao = 'Bem vindo %s! Para desconectar digite: {quit}' % name
    client.send(bytes(saudacao, "utf8"))
    msg = "%s Se conectou no chat!" % name
    broadcast(bytes(msg, "utf8")) #Se um novo cliente se conectar vai aparecer uma mensagem para todos os outros clientes já conectados
    clients[client] = name



    while True:
        msg = client.recv(1024) #Decodifica os bytes recebidos em forma de msg
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s Saiu do chat" % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = '192.168.25.14'
PORT = 33000
#BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando Conexão")
    ACCEPT_THREAD = Thread(target=aceitar_cliente)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()