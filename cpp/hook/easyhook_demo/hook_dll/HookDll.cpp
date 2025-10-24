#include "HookDll.h"
#include <string>
#include <sstream>

// Hook 目标：MessageBoxW
using MessageBoxW_t = int (WINAPI*)(HWND, LPCWSTR, LPCWSTR, UINT);
static MessageBoxW_t TrueMessageBoxW = nullptr;
static HOOK_TRACE_INFO g_HookInfo = {0};

static std::wstring NowPrefix() {
    SYSTEMTIME st{};
    GetLocalTime(&st);
    wchar_t buf[64];
    swprintf(buf, 64, L"%02d:%02d:%02d.%03d ", st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);
    return buf;
}

int WINAPI HookMessageBoxW(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType) {
    std::wstringstream ss;
    ss << L"[EasyHook] 拦截 MessageBoxW - " << NowPrefix()
       << L"Caption='" << (lpCaption ? lpCaption : L"<null>") << L"'"
       << L", Text='" << (lpText ? lpText : L"<null>") << L"'";
    OutputDebugStringW(ss.str().c_str());

    std::wstring newCaption = std::wstring(L"[HOOKED] ") + (lpCaption ? lpCaption : L"");
    return TrueMessageBoxW(hWnd, lpText, newCaption.c_str(), uType);
}

extern "C" __declspec(dllexport) DWORD WINAPI NativeInjectionEntryPoint(REMOTE_ENTRY_INFO* inRemoteInfo) {
    OutputDebugStringW(L"[EasyHook] Hook DLL 已注入，开始安装钩子...");

    HMODULE hUser32 = GetModuleHandleW(L"user32.dll");
    if (!hUser32) {
        OutputDebugStringW(L"[EasyHook] 获取 user32.dll 失败");
        return (DWORD)ERROR_MOD_NOT_FOUND;
    }
    FARPROC addr = GetProcAddress(hUser32, "MessageBoxW");
    if (!addr) {
        OutputDebugStringW(L"[EasyHook] 获取 MessageBoxW 地址失败");
        return (DWORD)ERROR_PROC_NOT_FOUND;
    }

    TrueMessageBoxW = reinterpret_cast<MessageBoxW_t>(addr);

    NTSTATUS status = LhInstallHook(addr, HookMessageBoxW, nullptr, &g_HookInfo);
    if (FAILED(status)) {
        wchar_t msg[256];
        swprintf(msg, 256, L"[EasyHook] LhInstallHook 失败, NTSTATUS=0x%08X", status);
        OutputDebugStringW(msg);
        return (DWORD)status;
    }

    // 线程 ACL：0 表示对所有线程启用钩子（典型用法）
    ULONG ACLEntries[1] = {0};
    LhSetExclusiveACL(ACLEntries, 1, &g_HookInfo);

    OutputDebugStringW(L"[EasyHook] 钩子安装成功，返回以继续进程执行。");
    return 0;
}