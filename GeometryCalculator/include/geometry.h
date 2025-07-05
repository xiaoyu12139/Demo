/**
 * @file geometry.h
 * @brief 提供几何计算的 C++ 接口声明，包括圆面积与矩形面积。
 */
#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <functional>
#include "export.h"

#define PI 3.14159265358979323846

namespace geometry 
{

/**
 * @brief 日志级别
 */
enum class RLogLevel {
    DEBUG,
    INFO,
    WARN,
    ERROR
};

/**
 * @brief 将 LogLevel 转为小写字符串
 */
inline const char* to_string(RLogLevel aLevel) {
    switch (aLevel) {
        case RLogLevel::DEBUG:  return "debug";
        case RLogLevel::INFO:  return "info";
        case RLogLevel::WARN:  return "warn";
        case RLogLevel::ERROR: return "error";
    }
    return "unknown";
}

/**
 * @brief 设置全局的日志级别
 */
GEOMETRY_API void setGLogLevel(RLogLevel aLevel);

/**
 * @brief 日志回调函数签名：接收格式化后的消息
 */
// using LogCallback = std::function<void(const char* message)>;
using LogCallbackLevel = std::function<void(RLogLevel aLevel, const char* aMessage, void* aUserdata)>;

/**
 * @brief 设置自定义日志回调
 * @param callback 将被调用以输出日志消息
 */
// void setLogCallback(LogCallback callback);
// 注册日志回调，第二个参数为用户数据指针
GEOMETRY_API void setLogCallback(LogCallbackLevel aCallback, void* aUserdata = nullptr);

/**
 * @brief 计算一个圆的面积，给定其半径。
 * @param radius 圆的半径。
 * @return 计算得到的面积。
 */
GEOMETRY_API double circleArea(double aRadius);

/**
 * @brief 计算一个圆的面积，给定其半径。用于测试多线程,加锁解决
 * @param radius 圆的半径。
 * @return 计算得到的面积。
 */
GEOMETRY_API double circleAreaThreadMtx(double aRadius);

/**
 * @brief 计算一个圆的面积，给定其半径。用于测试多线程未加锁解决
 * @param radius 圆的半径。
 * @return 计算得到的面积。
 */
GEOMETRY_API double circleAreaThreadNoMtx(double aRadius);

/**
 * @brief 计算矩形的面积。
 * @param width 矩形的宽度。
 * @param height 矩形的高度。
 * @return 计算得到的面积。
 */
GEOMETRY_API double rectangleArea(double aWidth, double aHeight);

/**
 * @brief 计算三角形的面积
 * @param base   三角形的底边长度
 * @param height 三角形的高度
 * @return       计算得到的三角形面积
 */
GEOMETRY_API double triangleArea(double aBase, double aHeight);

/**
* @brief 计算一组圆的面积
*
* 输入多个半径，返回对应的圆面积列表。
* @param radii  输入半径数组
* @return       对应的面积数组，长度与输入相同
*/
GEOMETRY_API std::vector<double> calculateAreas(const std::vector<double>& aRadii);

/**
 * @brief msys下使用>dumpbin /EXPORTS libGeometryCalculatordll.dll查看dll或.a文件中是否存在这个符号，如果存在则说明设置指定导出失败
 */
 void testExport();
} // geometry
#endif // GEOMETRY_H