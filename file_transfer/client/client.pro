QT       += core gui network concurrent testlib
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = client
TEMPLATE = app

CONFIG += c++11

win32-msvc* {
    # 对所有 MSVC Kit（Debug/Release）都生效
    QMAKE_CXXFLAGS += /utf-8
}

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS
DEFINES += USE_QTCREATOR
# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0
INCLUDEPATH += $$PWD/../public

HEADERS += \
        mainwindow.h \
        $$PWD/../public/config.h \
        KFileTransferSender.h \
        $$PWD/../public/Singleton.h \
        $$PWD/../public/kfiletransfercachemanage.h

SOURCES += \
        main.cpp \
        mainwindow.cpp \
        KFileTransferSender.cpp \
        $$PWD/../public/kfiletransfercachemanage.cpp

FORMS += \
        mainwindow.ui
