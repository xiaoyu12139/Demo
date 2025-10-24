cmake_minimum_required(VERSION 3.5)
project(hook_console LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 5.15 REQUIRED COMPONENTS Core)

add_executable(hook_console
    main.cpp
    qt_hook.cpp
)

target_link_libraries(hook_console PRIVATE Qt5::Core)

target_include_directories(hook_console PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# 如果集成 MinHook 源码：
# add_library(minhook STATIC ../third_party/minhook/src/buffer.c ../third_party/minhook/src/hook.c ../third_party/minhook/src/trampoline.c)
# target_include_directories(minhook PUBLIC ../third_party/minhook/include)
# target_link_libraries(hook_console PRIVATE minhook)
# add_definitions(-DUSE_MINHOOK)

target_compile_definitions(hook_console PRIVATE QT_NO_KEYWORDS)