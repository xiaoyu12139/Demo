#include <windows.h>
#include <tlhelp32.h>
#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <EasyHook.h>

static DWORD FindProcessIdByName(const std::wstring& name) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) return 0;
    PROCESSENTRY32W pe{}; pe.dwSize = sizeof(pe);
    if (Process32FirstW(snapshot, &pe)) {
        do {
            if (_wcsicmp(pe.szExeFile, name.c_str()) == 0) {
                CloseHandle(snapshot);
                return pe.th32ProcessID;
            }
        } while (Process32NextW(snapshot, &pe));
    }
    CloseHandle(snapshot);
    return 0;
}

static bool IsNumber(const std::wstring& s) {
    for (wchar_t c : s) { if (c < L'0' || c > L'9') return false; }
    return !s.empty();
}

int wmain(int argc, wchar_t** argv) {
    std::wcout << L"[Injector] 用法: Injector.exe <PID|进程名> [可选参数]" << std::endl;

    if (argc < 2) {
        std::wcout << L"示例: Injector.exe TargetApp.exe" << std::endl;
        std::wcout << L"或    Injector.exe 12345" << std::endl;
        return 1;
    }

    DWORD pid = 0;
    std::wstring targetArg = argv[1];
    if (IsNumber(targetArg)) {
        pid = static_cast<DWORD>(_wtol(targetArg.c_str()));
    } else {
        pid = FindProcessIdByName(targetArg);
    }

    if (pid == 0) {
        std::wcerr << L"[Injector] 未找到目标进程: " << targetArg << std::endl;
        return 2;
    }

    wchar_t exePath[MAX_PATH];
    GetModuleFileNameW(nullptr, exePath, MAX_PATH);
    std::filesystem::path exeDir = std::filesystem::path(exePath).parent_path();
    std::filesystem::path dllPath = exeDir / L"HookDll.dll"; // 约定 DLL 与注入器位于同一输出目录

    if (!std::filesystem::exists(dllPath)) {
        std::wcerr << L"[Injector] 未找到 HookDll.dll: " << dllPath.wstring() << std::endl;
        return 3;
    }

    std::wcout << L"[Injector] 准备注入 PID=" << pid << L", DLL=" << dllPath.wstring() << std::endl;

    // 可选：传递参数到 DLL（NativeInjectionEntryPoint 可读取）
    std::vector<std::wstring> args;
    for (int i = 2; i < argc; ++i) args.emplace_back(argv[i]);

    // 将参数转换为 wchar_t* 数组（以空终止）
    std::vector<const wchar_t*> argPtrs;
    for (auto& a : args) argPtrs.push_back(a.c_str());

    NTSTATUS status = RhInjectLibrary(
        pid,
        0, // 线程 ID（0 表示新起远程线程）
        0, // 选项
        dllPath.c_str(), // 32位 DLL 路径（统一用一个路径，EasyHook会处理位数差异）
        dllPath.c_str(), // 64位 DLL 路径
        argPtrs.empty() ? nullptr : (const wchar_t**)&argPtrs[0], // 参数数组
        (DWORD)argPtrs.size()
    );

    if (FAILED(status)) {
        std::wcerr << L"[Injector] 注入失败, NTSTATUS=0x" << std::hex << status << std::endl;
        return 4;
    }

    std::wcout << L"[Injector] 注入成功！" << std::endl;
    return 0;
}