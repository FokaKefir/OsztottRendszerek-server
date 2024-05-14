import socket
import threading
import queue
import time
import datetime

PORT = 80
IP = socket.gethostname()
DATA_SIZE = 1024  # Byteban

queue = queue.Queue(maxsize=0)
file_flag = False


# Müködés: A beérkező adatokat egy szavaztként kezelem, ezt a fileba egy sorba rakom, külön sorok, külön beküldött
# szavazatok. A file neve a jelenlegi nap dátuma(külön szavazásnak tekintve a külön nap)


def write_to_file():
    global file_flag
    while True:
        if queue.empty():
            time.sleep(1)
            continue

        if not file_flag:
            file_flag = True

            today_date = datetime.date.today()

            file = open(str(today_date) + '.txt', 'a')
            file.write(str(queue.get()) + '\n')
            file.close()

            file_flag = False
        time.sleep(.1)


def listener(client_socket: socket.socket, addr):
    data = client_socket.recv(DATA_SIZE).encode()
    if not data:
        client_socket.close()
        return

    print('Szavazas erkezett be ' + str(addr) + '-tol')
    queue.put(data)
    client_socket.close()
    # Lezarja a socketet, one use socket. Bejelentkezik, elküldi az infot, lecsatlakozik, nem vár válaszra


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)
    print('Server started on IP:'+IP+', Port:'+str(PORT))

    threading.Thread(target=write_to_file).start()

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=listener, args=(client_socket, addr)).start()

