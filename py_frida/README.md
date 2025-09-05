# Windows DLL Hook 示例

使用 Python + Frida 来 hook Windows 系统 DLL 函数的示例项目。

## 功能特性

- **CreateFileW Hook**: 监控文件创建和打开操作
- **MessageBoxW Hook**: 监控消息框显示
- **实时监控**: 显示函数调用的详细参数和返回值
- **参数解析**: 自动解析访问权限、创建方式等参数

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install frida frida-tools
```

## 使用方法

### 1. 附加到现有进程

```bash
# 通过进程名附加
python windows_dll_hook.py notepad.exe

# 通过进程ID附加
python windows_dll_hook.py 1234
```

### 2. 自动启动测试进程

```bash
# 不指定参数，会自动启动 notepad.exe 进行测试
python windows_dll_hook.py
```

## 监控的函数

### CreateFileW (kernel32.dll)

监控文件操作，显示：
- 文件路径
- 访问权限 (GENERIC_READ, GENERIC_WRITE 等)
- 共享模式
- 创建方式 (CREATE_NEW, OPEN_EXISTING 等)
- 操作结果和文件句柄

### MessageBoxW (user32.dll)

监控消息框显示，显示：
- 消息文本
- 标题
- 消息框类型
- 用户选择结果

## 输出示例

```
[*] CreateFileW 被调用:
    文件名: C:\Users\user\Desktop\test.txt
    访问权限: 0x80000000
    共享模式: 0x1
    创建方式: 0x3
    访问权限解析: GENERIC_READ 
    创建方式解析: OPEN_EXISTING
    结果: 成功，句柄 = 0x1a4
    文件: C:\Users\user\Desktop\test.txt
------------------------------------------------------------
```

## 注意事项

1. **管理员权限**: 某些进程可能需要管理员权限才能附加
2. **防病毒软件**: 可能会被防病毒软件误报，需要添加白名单
3. **目标架构**: 确保 Python 和目标进程的架构匹配（32位/64位）
4. **进程保护**: 某些系统进程可能受到保护，无法附加

## 扩展功能

你可以通过修改 JavaScript 代码来添加更多 hook：

```javascript
// Hook 其他 DLL 函数
var ntdll = Module.findExportByName("ntdll.dll", "NtCreateFile");
var advapi32 = Module.findExportByName("advapi32.dll", "RegOpenKeyExW");
```

## 常见问题

### Q: 提示 "ProcessNotFoundError"
A: 确保目标进程正在运行，或者检查进程名是否正确

### Q: 提示 "PermissionDeniedError"
A: 以管理员身份运行 Python 脚本

### Q: 没有看到任何输出
A: 目标进程可能没有调用被 hook 的函数，尝试在目标程序中执行相关操作

## 技术原理

1. **动态插桩**: Frida 通过动态插桩技术在运行时修改目标进程
2. **函数拦截**: 使用 `Interceptor.attach()` 拦截 DLL 函数调用
3. **参数读取**: 通过 `args` 数组读取函数参数
4. **返回值监控**: 通过 `onLeave` 回调监控函数返回值

## 许可证

本项目仅用于学习和研究目的，请遵守相关法律法规。