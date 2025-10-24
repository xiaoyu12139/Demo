cmake_minimum_required(VERSION 3.16)
project(easyhook_demo LANGUAGES CXX)

# 要求：设置 EasyHook 根目录（包含 include 和 lib 子目录）
# 使用时：cmake -S . -B build -DEASYHOOK_DIR="C:/path/to/EasyHook"
if(NOT EASYHOOK_DIR)
    message(FATAL_ERROR "请通过 -DEASYHOOK_DIR 指定 EasyHook 根目录（含 include/ 与 lib/）")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_definitions(-DUNICODE -D_UNICODE)

# 统一输出到 build/bin 目录，便于注入器定位 DLL
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# EasyHook 路径配置（根据位数选择 lib）
set(EASYHOOK_INCLUDE_DIR "${EASYHOOK_DIR}/include")
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(EASYHOOK_LIB "${EASYHOOK_DIR}/lib/EasyHook64.lib")
else()
    set(EASYHOOK_LIB "${EASYHOOK_DIR}/lib/EasyHook32.lib")
endif()

include_directories(${EASYHOOK_INCLUDE_DIR})

# 目标 demo（调用 MessageBoxW）
add_executable(TargetApp target_app/main.cpp)
# 需要链接 user32
if(MSVC)
    target_link_libraries(TargetApp PRIVATE user32)
else()
    target_link_libraries(TargetApp PRIVATE user32)
endif()

# Hook DLL
add_library(HookDll SHARED hook_dll/HookDll.cpp)
# 链接 EasyHook
target_link_libraries(HookDll PRIVATE ${EASYHOOK_LIB})

# 注入器（RhInjectLibrary）
add_executable(Injector injector/Injector.cpp)
# 链接 EasyHook
target_link_libraries(Injector PRIVATE ${EASYHOOK_LIB})