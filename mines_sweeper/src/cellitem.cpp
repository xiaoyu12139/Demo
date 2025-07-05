#include "cellitem.h"
//#include <qDebug>
#include <fielddata.h>

int cellItem::_refCount = 0;

QPixmap * cellItem::_initial    =   nullptr;
QPixmap * cellItem::_flag       =   nullptr;
QPixmap * cellItem::_question   =   nullptr;
QPixmap * cellItem::_blank      =   nullptr;
QPixmap * cellItem::_explode    =   nullptr;
QPixmap * cellItem::_digits[9]  =   {nullptr};

cellItem::cellItem(int x, int y,
                   enum cellStatus status, QGraphicsItem *parent)
    :
      QGraphicsPixmapItem(parent) {
    cx = x;
    cy = y;
    _status = status;

    ++_refCount;//创建第一个cellItem时加载所有图片

    if(_refCount == 1) {//引用计数，保证只new一次
        _initial    =   new QPixmap("://resource/images/initial.png");
        _flag       =   new QPixmap("://resource/images/flag.png");
        _question   =   new QPixmap("://resource/images/question.png");
        _blank      =   new QPixmap("://resource/images/blank.png");
        _explode    =   new QPixmap("://resource/images/explode.png");

        QString prefix = "://resource/images/";
        QString num;
        QString suffix = ".png";

        for(int i=1;i<9;++i){
            QString fileName;
            fileName+=prefix;
            fileName+=num.setNum(i);
            fileName+=suffix;
            _digits[i] = new QPixmap(fileName);
        }
    }
    setPixmap(*_initial);
    //qDebug()<<this<<endl;
}

cellItem::~cellItem(){
    //释放所有cellItem后，释放图片
    if(--_refCount == 0){
        delete _initial   ;
        delete _flag      ;
        delete _question  ;
        delete _blank     ;
        delete _explode   ;
        for(int i=0;i<9;++i){
            delete _digits[i];
        }
    }
}

enum cellStatus cellItem::getStatus(){
    return _status;
}

void cellItem::setStatus(enum cellStatus status,int digit){
    _status=status;
    switch(_status){
    case INITIAL:
        setPixmap(*_initial);
        break;
    case FLAG:
        setPixmap(*_flag);
        break;
    case QUESTION:
        setPixmap(*_question);
        break;
    case EXPLODE:
        setPixmap(*_explode);
        break;
    case DIGIT:
        setPixmap(*_digits[digit]);
        break;
    case BLANK:
        setPixmap(*_blank);
        break;
    default:
        break;
    }
}

