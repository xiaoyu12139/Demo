> 2025/06/17

任务全部完成

单元测试和示例程序通过option控制默认开启还是关闭。如果需要通过修改cmakelists.txt来开启和关闭单元测试和示例程序，需要删除build文件夹重新构建，或者通过`cmake -S . -B build -DBUILD_EXAMPLES=OFF`在命令行强制传OFF。

环境配置：

* vscode：安装插件cmake-tools、cmake，在cmake-tools设置中Use C Make Presets项设置为auto或者always

* msys2：

  ```
  export https_proxy=http://192.168.1.227:9870;export http_proxy=http://192.168.1.227:9870;export all_proxy=socks5://192.168.1.227:9870 #设置公司梯子代理
  pacman -Syuu # 同步软件包数据库并更新核心包
  # 只装 64 位的 MinGW GCC 编译器（包含 g++）
  pacman -S --needed mingw-w64-x86_64-gcc
  # 如果你还需要 CMake（生成项目文件）
  pacman -S --needed mingw-w64-x86_64-cmake
  # 如果需要基础的 MSYS2 运行时库（通常默认已经有了）
  pacman -S --needed mingw-w64-x86_64-runtime
  pacman -S --needed mingw-w64-x86_64-gtest #安装gtest
  # 安装 MinGW64 版本的 Ninja
  pacman -Sy --needed mingw-w64-x86_64-ninja
  ```

  系统环境变量中配置msys2的目录C:\msys64\mingw64\bin

运行：

* vscode中调出**命令面板**（setting->Keyboard Shortcuts->搜索show all commands->查看快捷键），输入cmake:build构建
* 在dev文件夹下运行构建好的example程序
* vscode命令面板输入cmake:run tests执行单元测试
* 确保cmake tools侧边栏确保build构建目标设置为install

> 2025/06/18

1.创建新分支refactor-capi，并从master分支切换到refactor-capi分支

2.refactor-capi分支，修改c接口命名为蛇形小写,修改示例程序与单元测试对应位置的调用

3.在refactor-capi分支，提交代码

4.切换到refactor-capi分支，rebase到master分支

5.让 `master` 跟上新的提交：git checkout master
git merge --ff-only feat

下载vs_buildtools安装，安装时选择C++开发组件，在Visual Studio 2022 Developer Command Prompt中输入dumpbin /EXPORTS libGeometryCalculatordll.dll查看确认是否为指定接口导出

