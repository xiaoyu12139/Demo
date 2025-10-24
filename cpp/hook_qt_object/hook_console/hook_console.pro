QT += core
CONFIG += console c++11
TEMPLATE = app
TARGET = hook_console

SOURCES += \
    main.cpp \
    qt_hook.cpp

HEADERS += \
    qt_hook.h \
    qt_hook_config.h

# 如果使用 MinHook 源码方式集成，设置包含路径与源文件，并定义宏：
# INCLUDEPATH += ../third_party/minhook/include
# SOURCES += ../third_party/minhook/src/buffer.c \
#            ../third_party/minhook/src/hook.c \
#            ../third_party/minhook/src/trampoline.c
# DEFINES += USE_MINHOOK