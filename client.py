from socket import *
def client(data):
    HOST = '192.168.43.211'
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data='OK'
    tcpCliSock.send(bytes(data,'utf-8'))
    tcpCliSock.close()


if __name__ == '__main__':
    client('OK')
