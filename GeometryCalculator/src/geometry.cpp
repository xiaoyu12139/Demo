/**
 * @file geometry.cpp
 * @brief 实现几何计算的 C++ 函数，包括圆面积与矩形面积。
 */
#include "geometry.h"
#include <cmath>
#include <vector>
#include <cstdio>
#include <string>
#include <cstring>
#include <iostream>
#include <mutex>

namespace geometry 
{
//日志级别
static RLogLevel glogLevel = RLogLevel::DEBUG;
//默认空回调
static LogCallbackLevel logCallback = [](RLogLevel level, const char* message, void* userdata){};
//用户数据
static void*  logUserdata = nullptr;

void setGLogLevel(RLogLevel aLevel)
{
    glogLevel = aLevel;
}

void setLogCallback(LogCallbackLevel aUserCallback, void* aUserdata)
{
    // 把用户数据先保存起来
    logUserdata = aUserdata;
    // 用 lambda 包装一层，把 userCallback 和 userdata 一起捕获
    logCallback = [aUserCallback = std::move(aUserCallback), aUserdata]
                  (RLogLevel level, const char* message, void* userdataInner) 
    {
        // 将枚举转为字符串
        const char* levelCStr = to_string(level);
        // 跳过低于阈值的日志
        if (level < glogLevel) {
            std::cout << levelCStr << " pass" << std::endl;
            return;
        }
        std::string levelStr(levelCStr);
        // ——在这里可以插入额外逻辑，比如加个前缀
        std::string decorated = "[" + levelStr + "] ";
        decorated += message;
        // 再调用真正的用户回调
        aUserCallback(level, decorated.c_str(), userdataInner);
    };
}

double circleArea(double aRadius) 
{
    if (aRadius < 0) throw std::invalid_argument("circleArea: radius cannot be negative");
    double area = PI * aRadius * aRadius;
    char buf[128];
    std::snprintf(buf, sizeof(buf), "[Geometry] circleArea: radius=%.6f, area=%.6f", aRadius, area);
    logCallback(RLogLevel::DEBUG,buf,logUserdata);
    logCallback(RLogLevel::INFO,buf,logUserdata);
    logCallback(RLogLevel::WARN,buf,logUserdata);
    logCallback(RLogLevel::ERROR,buf,logUserdata);
    return area;
}

static int callCount = 0;
static std::mutex countMtx;
double circleAreaThreadMtx(double aRadius) 
{
    if (aRadius < 0) throw std::invalid_argument("circleArea: radius cannot be negative");
    double area = PI * aRadius * aRadius;
    char buf[128];
    std::snprintf(buf, sizeof(buf), "[Geometry] circleArea: radius=%.6f, area=%.6f", aRadius, area);
    logCallback(RLogLevel::DEBUG,buf,logUserdata);
    logCallback(RLogLevel::INFO,buf,logUserdata);
    logCallback(RLogLevel::WARN,buf,logUserdata);
    logCallback(RLogLevel::ERROR,buf,logUserdata);
    {
        std::lock_guard<std::mutex> lk(countMtx);
        ++callCount;
        std::cout << "[Internal Counter] circleAreaThread has been called " << callCount << " times\n";
    }
    return area;
}

static int callCountNoMtx = 0;
double circleAreaThreadNoMtx(double aRadius) 
{
    if (aRadius < 0) throw std::invalid_argument("circleArea: radius cannot be negative");
    double area = PI * aRadius * aRadius;
    char buf[128];
    std::snprintf(buf, sizeof(buf), "[Geometry] circleArea: radius=%.6f, area=%.6f", aRadius, area);
    logCallback(RLogLevel::DEBUG,buf,logUserdata);
    logCallback(RLogLevel::INFO,buf,logUserdata);
    logCallback(RLogLevel::WARN,buf,logUserdata);
    logCallback(RLogLevel::ERROR,buf,logUserdata);
    ++callCountNoMtx;
    std::cout << "[Internal Counter] circleAreaThread has been called " << callCountNoMtx << " times\n";
    return area;
}

double rectangleArea(double aWidth, double aHeight) 
{
    if (aWidth < 0 || aHeight < 0) throw std::invalid_argument("rectangleArea: width/height cannot be negative");
    double area = aWidth * aHeight;
    char buf[128];
    std::snprintf(buf, sizeof(buf), "[Geometry] rectangleArea: width=%.6f, height=%.6f, area=%.6f", aWidth, aHeight, area);
    logCallback(RLogLevel::DEBUG,buf,logUserdata);
    logCallback(RLogLevel::INFO,buf,logUserdata);
    logCallback(RLogLevel::WARN,buf,logUserdata);
    logCallback(RLogLevel::ERROR,buf,logUserdata);
    return area;
}

double triangleArea(double aBase, double aHeight) {
    if (aBase < 0 || aHeight < 0) throw std::invalid_argument("triangleArea: base/height cannot be negative");
    double area = 0.5 * aBase * aHeight;
    char buf[128];
    std::snprintf(buf, sizeof(buf), "[Geometry] rectangleArea: width=%.6f, height=%.6f, area=%.6f", aBase, aHeight, area);
    logCallback(RLogLevel::DEBUG,buf,logUserdata);
    logCallback(RLogLevel::INFO,buf,logUserdata);
    logCallback(RLogLevel::WARN,buf,logUserdata);
    logCallback(RLogLevel::ERROR,buf,logUserdata);
    return area;
}

std::vector<double> calculateAreas(const std::vector<double>& aRadii) {
    std::vector<double> areas;
    areas.reserve(aRadii.size());
    for (double r : aRadii) {
        if (r < 0) throw std::invalid_argument("calculateAreas: negative radius in input");
        areas.push_back(circleArea(r));
    }
    // 日志回调一次性打印所有面积
    if (logCallback) {
        std::string msg = "[Geometry] calculateAreas: areas=[";
        for (size_t i = 0; i < areas.size(); ++i) {
            char buf[32];
            std::snprintf(buf, sizeof(buf), "%.6f", areas[i]);
            msg += buf;
            if (i + 1 < areas.size()) msg += ", ";
        }
        msg += "]";
        logCallback(RLogLevel::DEBUG,msg.c_str(),logUserdata);
        logCallback(RLogLevel::INFO,msg.c_str(),logUserdata);
        logCallback(RLogLevel::WARN,msg.c_str(),logUserdata);
        logCallback(RLogLevel::ERROR,msg.c_str(),logUserdata);
    }
    return areas;
}

void testExport()
{
    std::cout << " ";
}
} // geometry
