cmake_minimum_required(VERSION 3.8)
project(vs_server)

find_package(jsoncpp REQUIRED)

include_directories(${PROJECT_SOURCE_DIR}/src/include)
file(GLOB SOURCES "src/*.cpp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=x86-64")

add_executable(${PROJECT_NAME} ${SOURCES})

# find_path(MYSQL_INCLUDE_DIR
#   NAMES mysql/mysql.h
#   PATHS /usr/include /usr/local/include
# )
# if(NOT MYSQL_INCLUDE_DIR)
#   message(FATAL_ERROR "找不到 mysql/mysql.h，请安装 libmysqlclient-dev")
# endif()

find_library(MYSQLCLIENT_LIB
  NAMES mysqlclient
  PATHS /usr/lib /usr/lib/x86_64-linux-gnu /usr/local/lib
)
if(NOT MYSQLCLIENT_LIB)
  message(FATAL_ERROR "找不到 libmysqlclient.so，请安装 libmysqlclient-dev")
endif()

# 直接链接 JsonCpp 库目标。CMake 会自动把头文件路径和库都加好。
target_link_libraries(vs_server
    PRIVATE
      jsoncpp_lib      # JsonCpp 的主要库目标
      ${MYSQLCLIENT_LIB}
)
# # 3) 添加到 target
# target_include_directories(vs_server
#   PRIVATE
#     ${MYSQL_INCLUDE_DIR}
# )

target_link_libraries(vs_server
  PRIVATE
    
)