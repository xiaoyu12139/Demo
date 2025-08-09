/**
 * @file geometry_c_api.cpp
 * @brief 实现几何计算的 C 接口，封装对 C++ 函数的调用。
 */
#include "geometry_c_api.h"
#include "geometry.h"
#include <stdexcept>

#ifdef __cplusplus
extern "C" 
{
#endif

void set_glog_level(CLogLevel aLevel)
{
    geometry::RLogLevel cppLevel = static_cast<geometry::RLogLevel>(aLevel);
    geometry::setGLogLevel(cppLevel);
}

void g_set_log_callback(LogCallbackLevel aCallback, void* aUserdata)
{
    // 同步到 C++ 端
    geometry::setLogCallback(
        [=](geometry::RLogLevel lvl, const char* msg, void* ud){
            // 级别转换
            CLogLevel clevel = static_cast<CLogLevel>(lvl);
            if (aCallback) aCallback(clevel, msg, ud);
        },
        aUserdata
    );
}

double circle_area(double aRadius, ErrorCode* aErrcode) 
{
    try
    {
        double area = geometry::circleArea(aRadius);
        if (aErrcode) *aErrcode = GEO_SUCCESS;
        return area;
    }
    catch (const std::invalid_argument& e) 
    {
        if (aErrcode) *aErrcode = GEO_ERR_NEGATIVE;
        return -1;
    }
    catch (...) {
        if (aErrcode) *aErrcode = GEO_ERR_OTHER;
        return -1;
    }
}

double rectangle_area(double aWidth, double aHeight, ErrorCode* aErrcode) 
{
    try
    {
        double area = geometry::rectangleArea(aWidth, aHeight);
        if (aErrcode) *aErrcode = GEO_SUCCESS;
        return area;
    }
    catch (const std::invalid_argument& e) 
    {
        if (aErrcode) *aErrcode = GEO_ERR_NEGATIVE;
        return -1;
    }
    catch (...) {
        if (aErrcode) *aErrcode = GEO_ERR_OTHER;
        return -1;
    }
}

double triangle_area(double aBase, double aHeight, ErrorCode* aErrcode) 
{
    try
    {
        double area = geometry::triangleArea(aBase, aHeight);
        if (aErrcode) *aErrcode = GEO_SUCCESS;
        return area;
    }
    catch (const std::invalid_argument& e) 
    {
        if (aErrcode) *aErrcode = GEO_ERR_NEGATIVE;
        return -1;
    }
    catch (...) {
        if (aErrcode) *aErrcode = GEO_ERR_OTHER;
        return -1;
    }
}

void calculate_areas(const double* aRadii, size_t aCount, double* aOutAreas, ErrorCode* aErrcode) 
{
    try
    {
        // 调用 C++ 接口计算并填充
        std::vector<double> areas = geometry::calculateAreas(
            std::vector<double>(aRadii, aRadii + aCount)
        );
        for (size_t i = 0; i < aCount; ++i) {
            aOutAreas[i] = areas[i];
        }
        if (aErrcode) *aErrcode = GEO_SUCCESS;
    }
    catch (const std::invalid_argument& e) 
    {
        if (aErrcode) *aErrcode = GEO_ERR_NEGATIVE;
    }
    catch (...) {
        if (aErrcode) *aErrcode = GEO_ERR_OTHER;
    }
}

#ifdef __cplusplus
}
#endif
