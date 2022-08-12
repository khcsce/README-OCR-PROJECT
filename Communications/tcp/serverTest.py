import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assigns a port for the server that listens to clients connecting to this port.
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
disconnect = False
while True:
        conn, addr = serv.accept()
        from_client = ''
        conn.send('I am SERVER'.encode())
        while True:
                data = conn.recv(4096)
                if not data: break
                from_client = data.decode()
                print(from_client)
                if from_client == 'stop':
                    disconnect = True
                    break
                conn.send('I am SERVER'.encode())
                
        if disconnect:
            conn.close()
            print('connection disconnected')
            break;
        conn.close()
        print('client disconnected')
