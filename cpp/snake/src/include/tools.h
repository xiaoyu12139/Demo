#ifndef TOOLS_H
#define TOOLS_H
#include <iostream>

#define KEY_ERROR -1
#define KEY_ESC 0
#define KEY_UP 1
#define KEY_DOWN 2
#define KEY_LEFT 3
#define KEY_RIGHT 4
#define KEY_ENTER 5

void SetWindowSize(int cols, int lines);
void SetCursorPosition(const int x, const int y);
void SetColor(int colorID);
void SetBackColor();
int getKeyCode();
void clearScreen();
void sleep(int t);


inline std::string win_str(std::string s){
    return s;
}

#ifdef __linux__
#include <iconv.h>
inline std::string linux_str(std::string gb2312_str){
    iconv_t cd = iconv_open("UTF-8", "GB2312");
    if (cd == (iconv_t)-1) {
        perror("iconv_open");
        return "";
    }

    size_t in_len = gb2312_str.size();
    size_t out_len = in_len * 2;
    std::string out(out_len, 0);
    char *in_ptr = const_cast<char*>(gb2312_str.c_str());
    char *out_ptr = &out[0];
    size_t out_bytes_left = out_len;

    if (iconv(cd, &in_ptr, &in_len, &out_ptr, &out_bytes_left) == (size_t)-1) {
        perror("iconv");
        iconv_close(cd);
        return "";
    }

    iconv_close(cd);
    out.resize(out_len - out_bytes_left);
    return out;
}
#endif

#ifdef _WIN32
#define STR win_str
#else
#define STR linux_str
#endif

#endif // TOOLS_H
