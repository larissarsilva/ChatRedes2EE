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
    saudacao = 'Bem vindo %s! Para desconectar digite: .sair' % name
    client.send(bytes(saudacao, "utf8"))
    msg = "%s Se conectou no chat!" % name
    dif(bytes(msg, "utf8")) #Se um novo cliente se conectar vai aparecer uma mensagem para todos os outros clientes já conectados
    clients[client] = name #Adiciona o nome no dicionário cliente



    while True:
        msg = client.recv(1024) #Recebe os bytes informado pelo cliente
        if msg != bytes(".sair", "utf8"): #Compara a mensagem enviada com .sair
            dif(msg, name + ": ")
        else:
            client.send(bytes(".sair", "utf8"))
            client.close() #encerra o socket do cliente
            del clients[client] #deleta o socket do dicionário
            dif(bytes("%s SAIU!!!" % name, "utf8")) #Envia, para outros usuários, que um usuário encerrou a conexão
            break


def dif(msg, prefix=""):
    #Difunde a mensagem para todos os clients

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}


ADDR = ('192.168.25.14', 33000)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) #Limite o número de clientes
    #Aceita e trata as threads e o join faz com que o código fique esperando para não encerrar o servidor
    print("Aguardando Conexão")
    ACCEPT_THREAD = Thread(target=aceitar_cliente)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()