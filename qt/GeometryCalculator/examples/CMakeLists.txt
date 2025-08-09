set(EXAMPLE_C_TARGET_NAME geometry_c_example)
set(EXAMPLE_CXX_TARGET_NAME geometry_cxx_example)

message(STATUS "EXAMPLE_C_TARGET_NAME:${EXAMPLE_C_TARGET_NAME}")
message(STATUS "EXAMPLE_DIR:${EXAMPLE_DIR}")
message(STATUS "OUTPUT_DIR:${OUTPUT_DIR}")

# c接口示例程序
add_executable(
    ${EXAMPLE_C_TARGET_NAME}
    ${EXAMPLE_DIR}/c_example.c
)
# 修改c接口示例程序的输出路径
set_target_properties(
    ${EXAMPLE_C_TARGET_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR}
)
# c接口 添加头文件目录
target_include_directories(
    ${EXAMPLE_C_TARGET_NAME} PUBLIC
    ${OUTPUT_DIR}/include
)
# c接口 添加依赖库目录
target_link_directories(
    ${EXAMPLE_C_TARGET_NAME} PUBLIC
    ${OUTPUT_DIR} 
)
# c接口 添加依赖库
target_link_libraries(
    ${EXAMPLE_C_TARGET_NAME} PUBLIC
    ${PROJECT_NAME}dll
)

# cpp 接口示例程序
add_executable(
    ${EXAMPLE_CXX_TARGET_NAME}
    ${EXAMPLE_DIR}/cpp_example.cpp
)
# 修改cpp接口示例程序的输出路径
set_target_properties(
    ${EXAMPLE_CXX_TARGET_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR}
)
# cpp接口 添加头文件目录
target_include_directories(
    ${EXAMPLE_CXX_TARGET_NAME} PUBLIC
    ${OUTPUT_DIR}/include
)
# cpp接口 添加依赖库目录
target_link_directories(
    ${EXAMPLE_CXX_TARGET_NAME} PUBLIC
    ${OUTPUT_DIR} 
)
# cpp接口 添加依赖库
target_link_libraries(
    ${EXAMPLE_CXX_TARGET_NAME} PUBLIC
    ${PROJECT_NAME}dll
)
