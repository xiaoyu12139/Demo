#include "readthread.h"
#include "readclient.h"
#include<QTcpSocket>
ReadThread::ReadThread()
{

}

void ReadThread::run(){
//    Client * client = Client::getTcpSocketClient();
//    QTcpSocket * tcpSocket = client->getTcpClient();
    ReadClient * readClient = ReadClient::getTcpSocketClient();
    QTcpSocket * tcpSocket = readClient->getTcpClient();
    // 把 socket 迁到这个线程，让它的信号在这里触发
    tcpSocket->moveToThread(this);

    // readyRead 发生时，自动调用 readData()
    connect(tcpSocket, &QTcpSocket::readyRead,
            readClient,  &ReadClient::readData);

    // 允许外面用 quit()/requestInterruption() 退出
    exec();
}
