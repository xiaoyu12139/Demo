# DLL项目
add_library(test_dll SHARED
    test_dll.cpp
    test_dll.h
)

# 设置DLL导出宏
target_compile_definitions(test_dll PRIVATE TEST_DLL_EXPORTS)

# 设置输出名称
set_target_properties(test_dll PROPERTIES
    OUTPUT_NAME "test_dll"
    PREFIX ""
)

# 包含头文件目录
target_include_directories(test_dll PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)