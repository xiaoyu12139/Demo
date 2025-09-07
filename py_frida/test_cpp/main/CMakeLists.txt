# 主程序项目
add_executable(main_app
    main.cpp
)

# 链接DLL
target_link_libraries(main_app PRIVATE test_dll)

# 包含DLL头文件目录
target_include_directories(main_app PRIVATE
    ${CMAKE_SOURCE_DIR}/dll
)

# 设置输出名称
set_target_properties(main_app PROPERTIES
    OUTPUT_NAME "main_app"
)