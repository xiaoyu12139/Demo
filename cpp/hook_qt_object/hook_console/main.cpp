#include <QtCore/QCoreApplication>
#include <QtCore/QObject>
#include <QtCore/QMetaObject>
#include <QtCore/QMetaMethod>
#include <QtCore/QDebug>
#include <QtCore/QString>

#include "qt_hook.h"

class TestSender : public QObject {
    Q_OBJECT
public:
    explicit TestSender(QObject* p=nullptr):QObject(p){ setObjectName("TestSender"); }
signals:
    void ping(int v);
};

class TestReceiver : public QObject {
    Q_OBJECT
public:
    explicit TestReceiver(QObject* p=nullptr):QObject(p){ setObjectName("TestReceiver"); }
public slots:
    void onPing(int v){ qInfo() << "[hook_console] onPing:" << v; }
};

static QObject* objectFromAddressString(const QString& addrStr) {
    QString s = addrStr.trimmed();
    if (s.startsWith("0x") || s.startsWith("0X")) s = s.mid(2);
    bool ok=false; quint64 addr = s.toULongLong(&ok, 16); if(!ok) return nullptr;
    return reinterpret_cast<QObject*>(addr);
}

int main(int argc, char** argv){
    QCoreApplication app(argc, argv);

    QObject* target = nullptr;
    if (app.arguments().size() > 1) {
        target = objectFromAddressString(app.arguments().at(1));
        qInfo() << "[hook_console] target addr:" << app.arguments().at(1) << ", ptr:" << target;
    }

    initQtHooks(target);

    // 自测：如果没有目标对象地址，创建一对对象并连接，验证 hook 输出
    TestSender sender; TestReceiver recv;
    QObject::connect(&sender, SIGNAL(ping(int)), &recv, SLOT(onPing(int)));
    emit sender.ping(42);

    return 0;
}

#include "main.moc"