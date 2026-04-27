下载cef `cef_binary_146.0.12+g6214c8e+chromium-146.0.7680.179_windows64.tar`

直接用cmake编译这个解压的项目，在cmakelists.txt中的find_package后面添加add_compile_options(/utf-8)

如果需要在mfc中使用需要在cef_variables.cmake中的 set(CEF_RUNTIME_LIBRARY_FLAG "/MD" CACHE STRING "Optional flag specifying which runtime to use")这里的RUNTIME_LIBRARY类型改成与mfc程序一样的。如果修改这里不生校可以直接去cmakecache.txt中进行修改。