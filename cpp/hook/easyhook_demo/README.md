# EasyHook 示例：对 demo 进程进行 Hook

本示例在 `cpp/hook/easyhook_demo` 下包含三个组件：
- `TargetApp`：一个简单的控制台程序，循环调用 `MessageBoxW`。
- `HookDll`：使用 EasyHook 安装对 `MessageBoxW` 的钩子，修改消息框标题并输出调试日志。
- `Injector`：使用 EasyHook 的 `RhInjectLibrary` 将 `HookDll.dll` 注入到目标进程。

构建要求：
- Windows，VS/MSVC 或其他支持的编译器。
- 已获取并构建 EasyHook（包含 `include/` 与 `lib/`）。
  - 可选方式：
    - GitHub Release 预编译包（包含 32/64 位 lib 与头文件）。
    - 源码自行编译后得到 `EasyHook64.lib`/`EasyHook32.lib` 与 `EasyHook.h`。

## 构建步骤（CMake）

1. 准备 EasyHook 根目录，记为 `EASYHOOK_DIR`，其下应包含：
   - `include/EasyHook.h`
   - `lib/EasyHook64.lib`（64 位）或 `lib/EasyHook32.lib`（32 位）

2. 生成与构建：
   ```powershell
   cd cpp/hook/easyhook_demo
   cmake -S . -B build -DEASYHOOK_DIR="C:/path/to/EasyHook"
   cmake --build build --config Release
   ```

3. 构建输出目录：
   - 可执行文件与 DLL 统一输出到 `build/bin/`，包括：
     - `TargetApp.exe`
     - `Injector.exe`
     - `HookDll.dll`

## 运行与注入

1. 先运行目标程序：
   ```powershell
   .\build\bin\TargetApp.exe
   ```
   程序会弹出 3 次消息框。

2. 在消息框弹出期间（或启动后），运行注入器：
   - 按进程名注入：
     ```powershell
     .\build\bin\Injector.exe TargetApp.exe
     ```
   - 或按 PID 注入（任务管理器获取 PID）：
     ```powershell
     .\build\bin\Injector.exe 12345
     ```

3. 注入成功后：
   - 后续 `MessageBoxW` 的标题会被修改为以 `[HOOKED]` 开头。
   - 通过 DebugView 或调试器可见 `OutputDebugString` 输出：
     - 例如：`[EasyHook] 拦截 MessageBoxW - 12:34:56.789 Caption='Demo MessageBoxW', Text='这是第 2 次调用'`

## 注意事项

- 位数匹配：
  - 64 位目标进程需要 64 位 `HookDll.dll` 与 `EasyHook64.lib`；32 位同理。
- 权限：
  - 注入需要足够权限（管理员/UAC），部分安全软件可能拦截。
- 稳定性：
  - 钩子安装在常调用路径上时请避免重入或高频 I/O；本示例仅做简单演示。
- 路径约定：
  - CMake 已将所有产物输出到同一 `bin` 目录，`Injector` 默认从该目录加载 `HookDll.dll`。
- 扩展：
  - 可将 Hook 目标换为其他 Win32 API（如 `CreateFileW`、`WriteFile`），或在 Qt 目标进程中改为拦截 Qt 内部函数（需在 DLL 中定位函数地址与版本适配）。