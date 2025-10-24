#include <QtCore/QObject>
#include <QtCore/QMetaObject>
#include <QtCore/QMetaMethod>
#include <QtCore/QDebug>
#include <QtCore/QByteArray>
#include <windows.h>

#include "qt_hook_config.h"

static void* g_targetSender = nullptr;

// MinHook 可选：
#ifdef USE_MINHOOK
#include <MinHook.h>
#endif

static FARPROC findQtSymbol(const char* decorated) {
    HMODULE h = GetModuleHandleA("Qt5Core.dll");
    if (!h) h = LoadLibraryA("Qt5Core.dll");
    if (!h) return nullptr;
    return GetProcAddress(h, decorated);
}

// 保存原始函数指针
static void* orig_connect = nullptr;
static void* orig_activate = nullptr;

// QMetaObject::connect 原型（简化，未强制匹配签名，仅用于拦截日志）
typedef bool (*FnConnect)(const QMetaObject* senderMeta, int signalIndex, const void* receiver, void** slotPtr, int type, int* types); // 占位，真实签名依构建而定

// QMetaObject::activate 原型（占位）
typedef void (*FnActivate)(QObject* sender, int signalIndex, void** argv);

static bool Hook_connect(const QMetaObject* senderMeta, int signalIndex, const void* receiver, void** slotPtr, int type, int* types) {
    // 打印基本信息（无法完全恢复签名，仅打印索引）
    if (g_targetSender == nullptr || (senderMeta && ((QObject*)senderMeta->cast(g_targetSender) == g_targetSender))) {
        qInfo() << "[hook-connect] signalIndex:" << signalIndex << "receiver:" << receiver << "type:" << type;
    }
    FnConnect fn = (FnConnect)orig_connect;
    if (fn) return fn(senderMeta, signalIndex, receiver, slotPtr, type, types);
    return false;
}

static void Hook_activate(QObject* sender, int signalIndex, void** argv) {
    if (!g_targetSender || sender == g_targetSender) {
        qInfo() << "[hook-activate] sender:" << sender << "signalIndex:" << signalIndex;
    }
    FnActivate fn = (FnActivate)orig_activate;
    if (fn) fn(sender, signalIndex, argv);
}

bool initQtHooks(void* targetSender) {
    g_targetSender = targetSender;
#ifdef USE_MINHOOK
    if (MH_Initialize() != MH_OK) {
        qWarning() << "[hook] MH_Initialize failed";
        return false;
    }
    FARPROC pConnect = findQtSymbol(QMETAOBJECT_CONNECT_SYMBOL);
    FARPROC pActivate = findQtSymbol(QMETAOBJECT_ACTIVATE_SYMBOL);
    if (!pConnect || !pActivate) {
        qWarning() << "[hook] find symbol failed";
        return false;
    }
    orig_connect = (void*)pConnect;
    orig_activate = (void*)pActivate;
    if (MH_CreateHook(pConnect, (LPVOID)&Hook_connect, (LPVOID*)&orig_connect) != MH_OK) {
        qWarning() << "[hook] CreateHook connect failed";
        return false;
    }
    if (MH_CreateHook(pActivate, (LPVOID)&Hook_activate, (LPVOID*)&orig_activate) != MH_OK) {
        qWarning() << "[hook] CreateHook activate failed";
        return false;
    }
    if (MH_EnableHook(MH_ALL_HOOKS) != MH_OK) {
        qWarning() << "[hook] EnableHook failed";
        return false;
    }
    qInfo() << "[hook] Hooks installed";
    return true;
#else
    Q_UNUSED(targetSender);
    qInfo() << "[hook] USE_MINHOOK not defined, hook disabled";
    return false;
#endif
}