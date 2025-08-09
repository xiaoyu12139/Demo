#ifndef MYTIME_H
#define MYTIME_H


#include<iostream>
#include<string>
#include<chrono>
using namespace std;
class MyTime
{
public:
    static string getCurrentFormatTimeStr();
    static string getTimeStampStr();
};


#endif // MYTIME_H
