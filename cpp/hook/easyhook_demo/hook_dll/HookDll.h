#pragma once
#include <windows.h>
#include <EasyHook.h>

#ifdef __cplusplus
extern "C" {
#endif

__declspec(dllexport) DWORD WINAPI NativeInjectionEntryPoint(REMOTE_ENTRY_INFO* inRemoteInfo);

#ifdef __cplusplus
}
#endif