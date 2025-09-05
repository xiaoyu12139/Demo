#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows DLL Hook 示例
使用 Frida 来 hook Windows 系统 DLL 函数

本示例演示如何 hook kernel32.dll 中的 CreateFileW 函数
监控文件创建和打开操作
"""

import frida
import sys
import time

# Frida JavaScript 代码，用于 hook CreateFileW 函数
js_code = r'''
console.log("[+] Starting hook script...");

// 列出已加载的模块
console.log("[*] Enumerating loaded modules...");
Process.enumerateModules().forEach(function(module) {
    if (module.name.toLowerCase().includes("kernel32") || module.name.toLowerCase().includes("user32")) {
        console.log("[+] Found module: " + module.name + " at " + module.base);
    }
});

// Hook kernel32.dll CreateFileW function
try {
    var kernel32Module = Process.getModuleByName("KERNEL32.DLL");
    var createFileW = kernel32Module.getExportByName("CreateFileW");
    if (createFileW) {
        console.log("[+] Found CreateFileW function at: " + createFileW);
        
        Interceptor.attach(createFileW, {
            onEnter: function(args) {
            try {
                var fileName = args[0].readUtf16String();
                console.log("\n[*] CreateFileW called:");
                console.log("    File: " + fileName);
                this.fileName = fileName;
            } catch (e) {
                console.log("[!] Error in CreateFileW onEnter: " + e.message);
            }
        },
        
        onLeave: function(retval) {
            try {
                var handle = retval.toInt32();
                if (handle == -1) {
                    console.log("    Result: FAILED");
                } else {
                    console.log("    Result: SUCCESS, Handle = 0x" + handle.toString(16));
                }
                console.log("    File: " + this.fileName);
                console.log("    --------------------");
            } catch (e) {
                console.log("[!] Error in CreateFileW onLeave: " + e.message);
            }
        }
    });
    } else {
        console.log("[-] CreateFileW function not found");
    }
} catch (e) {
    console.log("[-] CreateFileW function error: " + e.message);
}

// Hook MessageBoxW function
try {
    var user32Module = Process.getModuleByName("USER32.dll");
    var messageBoxW = user32Module.getExportByName("MessageBoxW");
    if (messageBoxW) {
        console.log("[+] Found MessageBoxW function at: " + messageBoxW);
        
        Interceptor.attach(messageBoxW, {
        onEnter: function(args) {
            try {
                var text = args[1].readUtf16String();
                var caption = args[2].readUtf16String();
                console.log("\n[*] MessageBoxW called:");
                console.log("    Text: " + text);
                console.log("    Caption: " + caption);
            } catch (e) {
                console.log("[!] Error in MessageBoxW onEnter: " + e.message);
            }
        },
        
        onLeave: function(retval) {
            try {
                console.log("    User choice: " + retval.toInt32());
                console.log("    --------------------");
            } catch (e) {
                console.log("[!] Error in MessageBoxW onLeave: " + e.message);
            }
        }
    });
    } else {
        console.log("[-] MessageBoxW function not found");
    }
} catch (e) {
    console.log("[-] MessageBoxW function error: " + e.message);
}

console.log("[+] Hooks installed, monitoring started...");
'''

def on_message(message, data):
    """处理来自 Frida 脚本的消息"""
    if message['type'] == 'send':
        print(f"[Frida] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[错误] {message['stack']}")

def main():
    """主函数"""
    print("Windows DLL Hook 示例")
    print("=" * 50)
    
    try:
        # 获取目标进程
        if len(sys.argv) > 1:
            # 如果提供了进程名或PID
            target = sys.argv[1]
            try:
                # 尝试作为PID解析
                pid = int(target)
                session = frida.attach(pid)
                print(f"[+] 已附加到进程 PID: {pid}")
            except ValueError:
                # 作为进程名处理
                session = frida.attach(target)
                print(f"[+] 已附加到进程: {target}")
        else:
            # 附加到当前进程（用于测试）
            print("[*] 未指定目标进程，将创建新的进程进行测试")
            print("[*] 你也可以运行: python windows_dll_hook.py <进程名或PID>")
            
            # 启动一个简单的测试进程 (使用完整路径)
            import os
            notepad_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'notepad.exe')
            if not os.path.exists(notepad_path):
                notepad_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'notepad.exe')
            
            if os.path.exists(notepad_path):
                pid = frida.spawn([notepad_path])
                session = frida.attach(pid)
                print(f"[+] 已启动并附加到 notepad.exe (PID: {pid})")
                frida.resume(pid)
            else:
                print("[错误] 无法找到 notepad.exe，请手动指定一个进程")
                print("[*] 使用方法: python windows_dll_hook.py <进程名或PID>")
                return
        
        # 创建脚本
        script = session.create_script(js_code)
        script.on('message', on_message)
        
        # 加载脚本
        script.load()
        print("[+] Frida 脚本已加载")
        print("[*] 开始监控 DLL 函数调用...")
        print("[*] 按 Ctrl+C 停止监控")
        print("=" * 50)
        
        # 保持脚本运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] 用户中断，正在停止...")
        
    except frida.ProcessNotFoundError:
        print(f"[错误] 未找到目标进程: {sys.argv[1] if len(sys.argv) > 1 else 'unknown'}")
        print("[提示] 请确保进程正在运行，或者提供正确的进程名/PID")
    except frida.PermissionDeniedError:
        print("[错误] 权限不足，请以管理员身份运行")
    except Exception as e:
        print(f"[错误] {str(e)}")
    finally:
        try:
            session.detach()
            print("[+] 已从目标进程分离")
        except:
            pass

if __name__ == "__main__":
    main()