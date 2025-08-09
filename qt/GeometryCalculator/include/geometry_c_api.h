/**
 * @file geometry_c_api.h
 * @brief 提供几何计算的 C 接口声明，用于 C/C++ 混合开发。
 */
#ifndef GEOMETRY_C_API_H
#define GEOMETRY_C_API_H

#ifdef __cplusplus
extern "C" 
{
#endif

#include <stddef.h>
#include <stdio.h>
#include "export.h"

#define PI 3.14159265358979323846


/**
 * @brief  错误码枚举
 */
typedef enum {
    GEO_SUCCESS          = 0,   ///< 正常情况
    GEO_ERR_NEGATIVE     = 1,  ///< 传入了负数
    GEO_ERR_OTHER        = 2   ///< 其它内部错误
} ErrorCode;

/**
 * @brief  与 C++ LogLevel 对应
 */
typedef enum {
    DEBUG,
    INFO,
    WARN,
    ERROR
} CLogLevel;

/**
 * @brief 将 LogLevel 转为小写字符串
 */
inline const char* to_string(CLogLevel level) {
    switch (level) {
        case DEBUG:  return "debug";
        case INFO:  return "info";
        case WARN:  return "warn";
        case ERROR: return "error";
    }
    return "unknown";
}

/**
 * @brief  C 回调签名：级别 + 消息 + 用户数据
 */
typedef void (*LogCallbackLevel)(
    CLogLevel aLevel,
    const char*aMessage,
    void* aUserdata);

/**
 * @brief 设置全局的日志级别
 */
GEOMETRY_API void set_glog_level(CLogLevel aLevel);

/**
 * @brief 设置 C 端日志回调（消息为 C 字符串）
 * @param callback 接收日志消息的函数指针
 */
// void setLogCallback(void (*callback)(const char* message));
// 注册日志回调
GEOMETRY_API void g_set_log_callback(
    LogCallbackLevel aCallback,
    void* aUserdata);

/**
 * @brief 计算圆面积的 C 接口。
 * @param radius 圆的半径。
 * @param errcode  错误码输出（可 NULL）
 * @return 计算得到的面积。
 */
GEOMETRY_API double circle_area(double aRadius, ErrorCode* aErrcode);

/**
 * @brief 计算矩形面积的 C 接口。
 * @param width 矩形的宽度。
 * @param height 矩形的高度。
 * @param errcode  错误码输出（可 NULL）
 * @return 计算得到的面积。
 */
GEOMETRY_API double rectangle_area(double aWidth, double aHeight, ErrorCode* aErrcode);

/**
 * @brief 计算三角形的面积
 * @param base   三角形的底边长度
 * @param height 三角形的高度
 * @param errcode  错误码输出（可 NULL）
 * @return       计算得到的三角形面积
 */
GEOMETRY_API double triangle_area(double aBase, double aHeight, ErrorCode* aErrcode);

/**
 * @brief 计算一组圆的面积
 * @param radii 输入半径数组，长度为 count
 * @param count 半径数组的元素数量
 * @param out_areas 输出缓冲区，长度应至少为 count，用于存放计算得到的面积
 * @param errcode  错误码输出（可 NULL）
 */
GEOMETRY_API void calculate_areas(const double* aRadii, size_t aCount, double* aOutAreas, ErrorCode* aErrcode);

#ifdef __cplusplus
}
#endif

#endif // GEOMETRY_C_API_H

