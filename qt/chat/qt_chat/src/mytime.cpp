#include "mytime.h"
#include <QDateTime>

string MyTime::getCurrentFormatTimeStr() {
    time_t timep;
    time(&timep);
    char tmp[64] = { '\0' };
    strftime(tmp, sizeof(tmp), "%Y-%m-%d %H:%M:%S", localtime(&timep));
    return string(tmp);
}

string MyTime::getTimeStampStr(){
    QDateTime dt = QDateTime::currentDateTime();
    QString tmp = dt.toString("yyyy-MM-dd hh:mm:ss.zzz");
    qint64 s = QDateTime::currentDateTime().toSecsSinceEpoch();
    // return tmp.toStdString();
    return std::to_string(s);
}

