# 两个独立程序：demo_gui 与 hook_console

该目录包含两个互不依赖的程序：
- `demo_gui/`：一个独立的 Qt Widgets 示例程序，创建简单界面并建立若干信号/槽连接。
- `hook_console/`：一个独立的控制台程序，用二进制级拦截（可选 MinHook）观察并打印连接与信号激活。

## demo_gui
- 运行后会显示窗口，并在标签上显示 `MainWindow` 的地址（十六进制）。
- 提供 `valueChanged(int)` 与 `textEmitted(QString)` 两个信号，通过按钮与滑条驱动。

构建：
- qmake：
```powershell
cd c:\Users\user1\Desktop\Code\Demo\cpp\hook_qt_object\demo_gui
qmake
nmake  # 或 mingw32-make
```
- CMake：
```powershell
cd c:\Users\user1\Desktop\Code\Demo\cpp\hook_qt_object\demo_gui
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:\Qt\5.15.9\msvc2019_64"
cmake --build build --config Release
```

## hook_console
- 启动时尝试安装对 `QMetaObject::connect` 与 `QMetaObject::activate` 的 hook（需定义 `USE_MINHOOK` 并正确填写 `qt_hook_config.h` 的导出符号名）。
- 可选传入一个十六进制地址参数，用于只打印该 `QObject*` 作为 sender 的连接与信号发出日志：
```powershell
hook_console.exe 0x000001A2B3C4D5E6
```
- 若未传入地址，程序会自建 `TestSender`/`TestReceiver` 进行自测。

构建：
- qmake：
```powershell
cd c:\Users\user1\Desktop\Code\Demo\cpp\hook_qt_object\hook_console
qmake
nmake  # 或 mingw32-make
```
- CMake：
```powershell
cd c:\Users\user1\Desktop\Code\Demo\cpp\hook_qt_object\hook_console
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:\Qt\5.15.9\msvc2019_64"
cmake --build build --config Release
```

## 重要说明
- `hook_console` 只能拦截并打印其自身进程内的连接与信号。如果你希望在独立的 GUI 进程中观察其对象连接，需使用 **DLL 注入** 或在目标程序中内置 hook 初始化逻辑。
- 查找 `Qt5Core.dll` 的导出装饰名：
```powershell
dumpbin /exports C:\Qt\5.15.9\msvc2019_64\bin\Qt5Core.dll | findstr /i "QMetaObject::connect QMetaObject::activate"
```
将结果填入 `hook_console/qt_hook_config.h`。
- 若少数连接路径不经由 `QMetaObject::connect`，考虑额外拦截 `QObject::connectImpl`（另行查找符号）。