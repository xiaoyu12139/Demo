#include "widget.h"
#include "loginform.h"
#include <QApplication>
#include <QNetworkProxy>

int main(int argc, char *argv[])
{
    QNetworkProxyFactory::setUseSystemConfiguration(false);
    QApplication a(argc, argv);
    LoginForm loginForm;
    loginForm.show();
    return a.exec();
}
