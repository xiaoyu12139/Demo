# 设置最小的cmake版本要求
cmake_minimum_required(VERSION 3.10)
# 设置项目信息
project(
    GeometryCalculator
    VERSION 0.1.0
    DESCRIPTION "新人练习"
    LANGUAGES C CXX
)
# 使用 project 版本信息
set(PROJECT_VERSION ${PROJECT_VERSION})
string(REPLACE "." ";" VERSION_LIST ${PROJECT_VERSION})
list(GET VERSION_LIST 0 VERSION_MAJOR)
list(GET VERSION_LIST 1 VERSION_MINOR)
list(GET VERSION_LIST 2 VERSION_PATCH)

message(STATUS "${PROJECT_NAME}" version "${PROJECT_VERSION}")

# 设置 C、C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
# 检测到编译器不支持 C++20 时报错
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 防止不小心用了 GCC 才有的特性
set(CMAKE_CXX_EXTENSIONS OFF)

# 遍历寻找 .h 文件的路径放到 HEADERS 变量
file(GLOB_RECURSE HEADERS ${PROJECT_SOURCE_DIR}/include/*.h)
# 遍历寻找 .cpp 文件的路径放到 SOURCES 变量
file(GLOB_RECURSE SOURCES ${PROJECT_SOURCE_DIR}/src/*.cpp)

# 是否同时生成动态库和静态库
option(BUILD_SHARED_LIBS  "Build shared libraries" ON)

#设置动态库名称
set(DLL_NAME "${PROJECT_NAME}dll")
set(LIB_NAME "${PROJECT_NAME}lib")

# 设置生成动态库的源文件有哪些
add_library(
    ${DLL_NAME} SHARED
    ${SOURCES}
)
set_target_properties(
    ${DLL_NAME} PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    OUTPUT_NAME ${DLL_NAME}
    # WINDOWS_EXPORT_ALL_SYMBOLS OFF
)
target_include_directories(
    ${DLL_NAME} PUBLIC 
    ${PROJECT_SOURCE_DIR}/include
)
target_compile_definitions(${DLL_NAME} PRIVATE BUILDING_GEOMETRY_DLL)

# 生成静态库
# add_library(
#     ${LIB_NAME} STATIC 
#     ${SOURCES}
# )
# target_include_directories(
#     ${LIB_NAME} PUBLIC 
#     ${PROJECT_SOURCE_DIR}/include
# )
# set_target_properties(
#     ${LIB_NAME} PROPERTIES
#     VERSION ${PROJECT_VERSION}
#     SOVERSION ${PROJECT_VERSION_MAJOR}
#     OUTPUT_NAME ${LIB_NAME}
# )

# 设置安装路径
set(OUTPUT_DIR ${PROJECT_SOURCE_DIR}/dev)

# 安装动态库
install(
    TARGETS ${DLL_NAME} #${LIB_NAME}
    ARCHIVE   DESTINATION "${OUTPUT_DIR}"
    LIBRARY   DESTINATION "${OUTPUT_DIR}"
    RUNTIME   DESTINATION "${OUTPUT_DIR}"
    INCLUDES  DESTINATION "${OUTPUT_DIR}"
)

# 导出头文件
install(
    DIRECTORY ${PROJECT_SOURCE_DIR}/include
    DESTINATION ${OUTPUT_DIR}
    FILES_MATCHING
    PATTERN "*.h"
)

# 单元测试
# 添加一个选项，默认开启构建测试程序
option(TESTING "Build test programs" ON)
if (TESTING)
    message(STATUS "Enable unit testing(${PROJECT_NAME})")
    enable_testing()
    set(TESTS_DIR ${PROJECT_SOURCE_DIR}/tests)
    add_subdirectory(tests)
    add_test(NAME test_geometry COMMAND geometry_test)
endif()

# 添加一个选项，默认开启构建示例程序
option(BUILD_EXAMPLES "Build example programs" ON)
if (BUILD_EXAMPLES)
    message(STATUS "Enable example(${PROJECT_NAME})")
    set(EXAMPLE_DIR ${PROJECT_SOURCE_DIR}/examples)
    add_subdirectory(examples)
endif()

