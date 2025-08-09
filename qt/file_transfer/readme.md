> 2025/5/6 14:05:44

##### 构建时报一些奇怪的错误

比如

*  C2039: "xx": 不是 "xxx" 的成员之类
* C2001: 常量中有换行符

检测编码问题，可能是当前编辑器是utf8但与编译器底层用的编码不一QString::fromUtf8("")，或者尝试使用vc打开对应文件，另存为编码为utf8带bom或不带bom或者项目中的所有文件的编码不统一

我这里统一设置为utf8带bom

##### 直接点击build下的exe运行报错缺少dll

打开Qt 5.15.0 for MSVC2019 32‑bit的命令行，然后cd到exe所在目录执行：windeployqt xx.exe 该命令会将执行该exe缺少的dll都copy过来

> testlib 项目被当作“Console”子系统来链接

##### qDebug() 打印中文乱码

QString::fromLocal8Bit

QString::fromUtf8(u8"连接成功"))

或文件前加#pragma execution_character_set("utf-8")

```
win32-msvc* {
对所有 MSVC Kit（Debug/Release）都生效
    QMAKE_CXXFLAGS += /utf-8
} #修改后执行qmake，然后重新构建
```

在简体中文 Windows 下，系统非 Unicode 程序语言通常使用 GBK/GB18030 编码，而 QtCreator 默认也使用“system”编码（即系统本地代码页）来解码输出。如果 `qDebug()` 实际输出的是 UTF-8 或 UTF-16 等编码，而 Qt Creator 用 GBK 解码，就会造成中文被解析为“???”。

**“文件用 UTF‑8 保存”≠“编译器/工具链当它是 UTF‑8”**，而且 Qt Creator 的“应用程序输出”又**默认把调试信息当成本地 ANSI（GBK）来解码**。MSVC 编译器默认是按照系统 ANSI（GBK）来解析源码

##### 建立连接过程

* 客户端使用QTcpSocket中的connectToHost发起连接，连接成功发出信号connected，连接失败发出errorOccurred

​	发起连接后可用waitForConnected等待，或者使用槽函数来处理信号

​	connectToHost通常要几十秒才会报timeout,所以可以使用waitForConnected或

```
QTimer::singleShot(2000, this, [this]() {
    if (_pCommandSocket->state() != QAbstractSocket::ConnectedState) {
        _pCommandSocket->abort();    // 取消握手
        emit errorState(
            ERROR_CLASSIFY_EM::K_NETWORK_ERROR,
            K_NETWORK_ERROR_EM::K_NETWORK_CONNECT_TIMEOUT
        );
    }
});
```

* 服务端使用QTcpServer中的listen对端口开启监听，在与客户端成功建立连接后会创建一个qtcpsocket, 发出newConnection信号，在槽函数中_pTcpServerControl->nextPendingConnection()获取这个qtcpsocket来接收文件

  服务器端qtcpsocket对象在本地有新数据读取时，会触发readyRead()

* `QTcpSocket` 调 `write()` 把文件数据写到网络。TCP 把数据发送到服务器，操作系统内核收到后放到服务器端对应 socket 的接收缓冲区里。

##### 发送一个文件的流程

* 客户端发送文件头部信息（头##状态码##其他信息）。发送一个发送文件响应头
* 服务端接收头部信息解析，打开本地文件准备写入，应答客户端“头已接收”。发送一个接收文件响应头
* 客户端接收到服务器断的接收文件响应头信息，响应代码正常则发送文件（send_file() 丢到线程池里异步执行）
* 与文件传输端口建立连接，然后分块发送，循环发送每块时检测ui线程中是否取消发送（flag）,这里的flag需要加锁
* 服务端文件传输端口读取到新数据触发readyRead()，然后保存文件（beginSave丢到线程池里异步执行）

##### 多个文件同时发送

* 客户端发送文件头部信息，服务端接收确认后，存储该文件头部
* 客户端启动一个线程发送数据，复端接收完数据后调用对应的文件头部确认文件是否完整

![](https://github.com/xiaoyu12139/file_transfer/blob/master/img/file_transfer_show.gif)
