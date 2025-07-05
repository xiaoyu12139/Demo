#### 介绍

windows+linux兼容版本的控制台简易贪吃蛇程序

linux环境为：Ubuntu 24.04.2 LTS

windows：Microsoft Windows [版本 10.0.22621.2283]

windows上使用vs2022，linux上使用vscode

> 2025/4/27 14:50:04

##### windows下编译

* 编译时报错C2001 常量中有换行符：file，另存为，保存那里选择编码后保存，选择unicode带bom的格式

* 编译时报错为什么这写不错那个错误	C2666	“Point::operator ==”: 重载函数具有类似的转换	：对于operator==(const)要声明为operator==(const) const

* 错误	C2614	“StartInterface”: 非法的成员初始化:“speed”不是基或成员	：转该文件名为带bom编译通过

##### vs关联到远程仓库

git init初始->创建gitignore文件->git add and git commit，github上手动创建仓库

git remote add origin xxx.git，然后git push -u origin master

之后在vs中视图->git更改就可以操作

或者没在远程创建仓库，直接点击git更改配置创建

##### ubuntu中git clone问题

不设置git的代理会卡很久

git config --global http.proxy xxxx:xxx 设置http与https的代理

同一个局域网中，设置代理为另一个主机，需要开启clash中的allow lan允许局域网连接

##### windows特有库标注

```
#include <conio.h>        // ❗ Windows特有的（MS-DOS时代的库，Linux没有）
#include <windows.h>      // ❗ Windows特有的（提供Windows API接口，Linux没有）
```

在linux中尝试用`unistd.h` + `ncurses.h`代替

> 2025/4/27 19:30:33

##### linux环境适配开发

linux上安装openssh-server,windows环境ssh-keygen，scp将id_ras.pub复制到linux然后重命名为authorized_keys。windows下.ssh中的config文件中配置linux的别名与指定密钥。

vscode远程连接

linux中下载cmake,g++

echo $TERM #查看终端类型xterm-256color

```
ubuntu默认使用的是gnome-terminal，$PS1中的\[\e]0;\u@\h: \w\a\]将标题锁死，需要将这段删除
system直接执行linux命令echo -ne "\033]0;新标题测试\007"依然每正常修改，因为默认使用的dash，要使用bash -c '命令1;命令2'，来显示指定bash能正常修改
```

##### tmux分屏调试程序

ctrl+b命令前缀：%垂直分屏、“水平分屏、x关闭当前屏幕、:kill-session结束当前tmux会话、d关闭tmux后台运行tmux attach-session进行重连接、方向键切换窗口

##### tmux分屏也解决不了调试贪吃蛇屏幕刷新问题

使用kdbg调试，ubuntu20安装kdbg,

git clone -b maint https://github.com/j6t/kdbg.git 进行cmake编译报错找不到ecm

sudo apt install extra-cmake-modules安装cmake额外模块

还是报错找到不Qt5：sudo apt install qt5-qmake qtbase5-dev qtchooser qtbase5-dev-tools 安装qt5相关模块

> qtbase5-dev+qtbase5-dev-tools最主要的

找不到KF5：sudo apt install libkf5i18n-dev libkf5config-dev libkf5iconthemes-dev libkf5xmlgui-dev libkf5windowsystem-dev

编译后sudo make install安装

##### kdbg基于gdb也调不了

安装vscode

```
sudo apt install snapd
sudo snap install --classic code
```

##### vscode启动调试时，怎么都打不开外部终端

下载xterm测试，设置中添加"terminal.external.linuxExec": "/usr/bin/xterm"发现能打开

然后降低gnome-terminal的版本为gnome-terminal/focal-updates,now 3.36.2-1ubuntu1~20.04 amd64 正常打开

##### windows与linux中的键码不一

| 按键    | windows | linux          |
| ------- | ------- | -------------- |
| 上      | 224，72 | 27, 91, 65     |
| 下      | 224，80 | 27, 91, 66     |
| 右      | 224，77 | 27, 91, 67     |
| 左      | 224，75 | 27, 91, 68     |
| enter   | 13      | 10             |
| ESC     | 27      | 27             |
| w,s,a,d |         | 119,115,97,100 |
| W,S,A,D |         | 87,83,65,68    |
|         |         |                |

在linux平台使用wasd代替方向键resource/linux_show.gif

![image](https://github.com/xiaoyu12139/snake/blob/master/resource/linux_show.gif)

![image](https://github.com/xiaoyu12139/snake/blob/master/resource/windows_show.gif)
