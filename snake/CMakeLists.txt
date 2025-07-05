# CMakeList.txt: test05 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)
project ("snake")
set(CMAKE_CXX_STANDARD 20)

set(CMAKE_BUILD_TYPE Debug)

if(WIN32)
	message("windows")
	# 如果支持，请为 MSVC 编译器启用热重载。
	if (POLICY CMP0141)
	  cmake_policy(SET CMP0141 NEW)
	  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
	endif()
elseif (LINUX)
	message("linux")
endif()

message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")

include_directories(${PROJECT_SOURCE_DIR}/src/include)
file(GLOB SOURCES src/*.cpp)

# 将源代码添加到此项目的可执行文件。
add_executable (snake_app ${SOURCES})

if(WIN32)
	if (CMAKE_VERSION VERSION_GREATER 3.12)
	  set_property(TARGET snake_app PROPERTY CXX_STANDARD 20)
	endif()
elseif(LINUX)
endif()

