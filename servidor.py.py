import socket
import threading

HOST = '0.0.0.0'
PORTA = 12345

clientes = []

def broadcast(mensagem, cliente_atual):
    for cliente in clientes:
        if cliente != cliente_atual:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                clientes.remove(cliente)

def lidar_com_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            broadcast(mensagem, cliente)
        except:
            clientes.remove(cliente)
            cliente.close()
            break

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))
servidor.listen()

print(f"Servidor rodando na porta {PORTA}...")

while True:
    cliente, endereco = servidor.accept()
    print(f"Conexão de {endereco}")
    clientes.append(cliente)
    thread = threading.Thread(target=lidar_com_cliente, args=(cliente,))
    thread.start()
