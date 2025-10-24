#include <windows.h>
#include <string>
#include <iostream>

int wmain(int argc, wchar_t** argv) {
    std::wcout << L"[TargetApp] 启动，演示调用 MessageBoxW。" << std::endl;

    for (int i = 1; i <= 3; ++i) {
        std::wstring text = L"这是第 " + std::to_wstring(i) + L" 次调用";
        std::wstring caption = L"Demo MessageBoxW";
        MessageBoxW(nullptr, text.c_str(), caption.c_str(), MB_OK | MB_ICONINFORMATION);
        Sleep(500);
    }

    std::wcout << L"[TargetApp] 完成演示，退出。" << std::endl;
    return 0;
}