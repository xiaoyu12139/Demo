# 遍历寻找所有的 .cpp 文件的绝对路径放到 SOURCES 变量
file(GLOB_RECURSE SOURCES ${TESTS_DIR}/*.cpp)
# 设置可执行程序的名称
set(EXE_NAME geometry_test)
# 使用指定的源文件将可执行文件添加到项目中
add_executable(
    ${EXE_NAME}
    ${SOURCES}
)
# 添加头文件目录
target_include_directories(
    ${EXE_NAME} PUBLIC
    ${OUTPUT_DIR}/include
)
# 添加依赖库目录
target_link_directories(
    ${EXE_NAME} PUBLIC
    ${OUTPUT_DIR} 
)
# 添加依赖库
target_link_libraries(
    ${EXE_NAME} PUBLIC
    ${PROJECT_NAME}dll
    gtest
    gtest_main
)
