#ifndef CONIO_LINUX_H
#define CONIO_LINUX_H
#include <iostream>
#ifdef __linux__
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

// 1. Linux版getch()
inline int getch() {
    struct termios oldt, newt;
    int ch;
    tcgetattr(STDIN_FILENO, &oldt);           // 获取旧的终端设置
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);          // 取消缓冲+不回显
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);   // 应用新设置
    // system("stty -echo");
    ch = getchar();                            // 读一个字符
    // system("stty echo");
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);   // 恢复旧设置
    return ch;
}

// 2. Linux版kbhit()
inline int kbhit() {
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF) {
        ungetc(ch, stdin); // 把读取到的字符放回输入流
        return 1;
    }

    return 0;
}
#endif
#endif // CONIO_LINUX_H
