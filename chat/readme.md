##### 介绍

基于qt实现的聊天客户端和在ubuntu上的epoll实现服务端的聊天室，支持同步消息，发送文件，发送图片

##### socket

socket（套接字）是一个抽象概念，用来表示“网络通信的端点”。通俗地说，它就像一根插在系统里的网线插口，程序通过它才能跟网络上的另一端——可能是另一台机器上的程序——交换数据。

操作系统内部用 **文件描述符**统一管理所有可读写的“东西”——文件、管道、设备、网络连接，**socket** 就是让 TCP/IP 网络连接也能被当作“文件”来读写，这样程序就只需调用 `read()/write()`就能完成网络io。

每一个 socket 都对应一个 **文件描述符**，在内核中维护了一套状态机（TCP 的连接状态、发送/接收缓冲区等）。

windows下的叫winsocket操作流程和linux上类似

#### 客户端

> 2025/5/6 21:17:44

qt5实现，文件都设置为utf8带bom。

##### 连接服务端报错UnsupportedSocketOperationError: The proxy type is invalid for this operation

Qt 的底层对 QTcpSocket 会先从 “全局代理工厂” 拿一次代理。如果你的系统（或程序里）启用了 “使用系统代理配置”那它可能返回一个 HTTP 代理之类的类型， `QTcpSocket` 是不支持 HTTP 代理的，就会抛出这个错误。socket.setProxy(NoProxy) 只能覆盖到“应用层面”你显式设置的代理，但不影响系统代理工厂的默认行为。

main函数开始时设置

```
// 不再从系统/环境变量里读取任何代理
QNetworkProxyFactory::setUseSystemConfiguration(false);
// 应用层面也不使用代理
QNetworkProxy::setApplicationProxy(QNetworkProxy::NoProxy);
```

#### 服务端

> 2025/5/6 21:17:44

cmake编译实现，ubuntu上安装vscode,配置tasks.json与launch.json

安装cmake,make,g++

sudo apt install libmysqlclient-dev 然后cmake中手动查找指定lib位置

安装mysql:sudo apt install mysql-server,sudo mysql进入，

```
ALTER USER 'root'@'localhost'
  IDENTIFIED WITH mysql_native_password
  BY '123456';
-- 刷新权限表
FLUSH PRIVILEGES;
```

监听本机：inet_pton(AF_INET, HOST, &serverAddr.sin_addr);

监听所有：serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

使用：epoll_wait等待可读事件，epoll_wait返回值为填充进 `events[0]` 到 `events[nready-1]` 的有效事件个数，通过遍历events处理对应的可读/可写/异常等事件

```
1.创建socket:int lfd = socket(AF_INET, SOCK_STREAM, 0);//AF_INET为IPv4 协议族，SOCK_STREAM为面向连接的 TCP，返回值 lfd 就是「监听套接字」的文件描述符（fd）。
2.设置socket选项：int opt = 1;
setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
3. 绑定地址：bind把套接字和一个本地 IP+端口 绑定起来。
4.进入监听状态：listen告诉内核「我准备接受连接了」，内核会为到来的 connect() 请求维护一个等待队列，队列长度由第二个参数指定。
5. 接收连接（accept）：分为简单阻塞和高性能非阻塞 + epoll。
6.数据收发：read/write
7.连接关闭：close
```

##### accept模式与epoll模式的区别

| 特性     | 阻塞 accept() 模式                             | epoll 模式                                                   |
| -------- | ---------------------------------------------- | ------------------------------------------------------------ |
| 监听方式 | 每次调用 accept() 阻塞直到有新连接             | 一次调用 epoll_wait() 阻塞直到“有事件”                       |
| 连接管理 | 通常：`while(1){ cfd=accept(); handle(cfd); }` | `epoll_ctl()` 注册所有 fd，然后循环 `epoll_wait()` 分发      |
| I/O 调用 | `read()`/`write()` 也一般为阻塞                | `read()`/`write()` 通常设为非阻塞，用 `EPOLLIN`/`EPOLLOUT` 通知 |

阻塞 accept 模式：一个主线程 accept()，每接入一个连接可 `fork()` 子进程或 `std::thread`/`pthread` 一个线程来处理。线程/进程数目随连接数暴涨，切换开销大，资源消耗高。

epoll 模式：一个线程（或少量线程）同时管理成千上万 socket。只有真正有数据可读/可写时才回调，避免大量空读写调用和线程切换。

#### 运行流程

* 客户端：点击登录，连接服务器，QTcpSocket::write把字节写入了底层的 TCP 发送缓冲区，操作系统内核再通过 TCP 协议把它们送到对端。开始等待

* 服务端：启动时，把 **`lfd`** 的EPOLLIN注册到 epoll。当 epoll 告诉你 `lfd` 可读时，你调用 `accept()` 得到 **`cfd`**。然后再把 **`cfd`** 的EPOLLIN注册进 epoll用来读取客户端写来的数据。epoll_ctl 用于注册。

  拿到登录信息后，查询数据库中信息与该信息是否相符。然后返回给客户端一个状态信息。

* 客户端：拿到服务端返回的信息，判断登录状态。登录成功就打开聊天窗口。然后发送一个信息给服务端为了同步聊天室里面的一些信息，同时开启一个工作线程用于即时读取服务端的更新数据
* 服务端：收到读取信息后，将当前聊天室的相关信息发送给所有客户端来同步共同信息
* 客户端：读取工作线程收到readdata信号，将数据刷新到界面

退出与关闭同样发送响应数据到服务端通知服务端更新其他客户端的数据

**注意：** 服务端与客户端的可执行文件目录下，需要有一个image文件夹，否则可能会不显示图片到界面上。如果是在qtcreator中直接run的，那么在工作目录下需要有个image文件夹。

![](https://github.com/xiaoyu12139/chat/blob/master/image/chat_show.gif)





