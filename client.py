from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receber():
    #Tratamento das mensagens recebidas
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibilita que o cliente saia do chat
            break


def enviar(event=None):  #Envento criado quando o botão da interface é pressionado

    msg = my_msg.get() #my_msg interface gráfica
    my_msg.set("")  # Clears input field.
    client_socket.enviar(bytes(msg, "utf8"))
    if msg == ".sair": #se for igual a .sair fecha o socket
        client_socket.close()
        top.quit()


def fechado(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set(".sair")
    enviar()

top = tkinter.Tk()
top.title("Projeto Redes")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set(" ") #aqui tava o type msg
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, background='gray')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Enviar", command=send, background='lightgreen')
send_button.pack()

top.protocol("WM_DELETE_WINDOW", fechado)



ADDR = ('192.168.25.14', 33000)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receber_thread = Thread(target=receber)
receber_thread.start()
tkinter.mainloop()  # Starts GUI execution.