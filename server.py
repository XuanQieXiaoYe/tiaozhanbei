from socket import *
HOST=''
PORT=21567
BUFSIZ=1024
ADDR=(HOST,PORT)
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
def server():
    while True:
        print('waitting for connection......')
        tcpCliSock,addr=tcpSerSock.accept()
        print('......connected from:',addr)
        while True:
            data=tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            # tcpCliSock.send(data)
            print(str(data,'utf-8'))
        tcpCliSock.close()
    tcpSerSock.close()


if __name__ == '__main__':
    server()
