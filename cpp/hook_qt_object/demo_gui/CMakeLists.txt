cmake_minimum_required(VERSION 3.5)
project(demo_gui LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 5.15 REQUIRED COMPONENTS Widgets)

add_executable(demo_gui
    main.cpp
)

target_link_libraries(demo_gui PRIVATE Qt5::Widgets)

target_compile_definitions(demo_gui PRIVATE QT_NO_KEYWORDS)