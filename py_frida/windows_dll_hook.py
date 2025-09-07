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
import os

# 读取外部 JavaScript 文件
def load_js_script(script_name="test_dll_hook.js"):
    """加载外部 JavaScript 脚本文件，自动拼接工具函数库"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    utils_path = os.path.join(script_dir, "dll_hook_utils.js")
    
    try:
        # 读取主脚本文件
        with open(script_path, 'r', encoding='utf-8') as f:
            main_script = f.read()
            
        # 读取工具函数库
        try:
            with open(utils_path, 'r', encoding='utf-8') as f:
                utils_content = f.read()
            # 拼接脚本
            merged_script = f"""// ===== 自动拼接的工具函数库 =====
            {utils_content}
            // ===== 工具函数库结束 =====

            {main_script}"""
            
            print("[+] 工具函数库拼接完成")
            return merged_script
            
        except FileNotFoundError:
            print(f"[警告] 找不到工具函数库: {utils_path}")
            print("[提示] 将使用原始脚本，可能会出现require错误")
            return main_script
        
    except FileNotFoundError:
        print(f"[错误] 找不到脚本文件: {script_path}")
        print("[提示] 请确保脚本文件存在于同一目录下")
        return None
    except Exception as e:
        print(f"[错误] 读取脚本文件失败: {e}")
        return None

def on_message(message, data):
    """处理来自 Frida 脚本的消息"""
    if message['type'] == 'send':
        print(f"[Frida] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[错误] {message['stack']}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python windows_dll_hook.py <进程名或PID>")
        print("示例: python windows_dll_hook.py test_main.exe")
        print("示例: python windows_dll_hook.py 1234")
        return
    
    target = sys.argv[1]
    
    # 加载 JavaScript 脚本
    js_code = load_js_script()
    if js_code is None:
        return
    
    try:
        # 尝试连接到进程
        try:
            # 首先尝试作为进程名
            session = frida.attach(target)
            print(f"[+] 已连接到进程: {target}")
        except frida.ProcessNotFoundError:
            try:
                # 尝试作为 PID
                pid = int(target)
                session = frida.attach(pid)
                print(f"[+] 已连接到进程 PID: {pid}")
            except ValueError:
                print(f"[错误] 找不到进程: {target}")
                return
            except frida.ProcessNotFoundError:
                print(f"[错误] 找不到 PID 为 {pid} 的进程")
                return
        
        # 创建并加载脚本
        script = session.create_script(js_code)
        script.on('message', on_message)
        script.load()
        
        print("[+] Hook 脚本已加载，开始监控...")
        print("[提示] 按 Ctrl+C 停止监控")
        
        # 保持脚本运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] 停止监控")
        
    except frida.ServerNotRunningError:
        print("[错误] Frida 服务器未运行")
    except Exception as e:
        print(f"[错误] {e}")
    finally:
        try:
            session.detach()
        except:
            pass

if __name__ == "__main__":
    main()