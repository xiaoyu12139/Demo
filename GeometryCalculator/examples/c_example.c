/**
 * @file c_example.c
 * @brief c接口使用示例
 */
#include "geometry_c_api.h"
#include <stdio.h>
#include <stdlib.h>

/**
 * @brief C 回调函数
 */
void myCLog(CLogLevel aLevel, const char*aMessage, void* aUserdata)
{
    printf("%s\n", aMessage);
    //可以用level或着userdata进行一些其他自定义操作
}

/**
 * @brief 测试不开启日志测试计算面积
 */
void printAreaWithoutLog()
{
    ErrorCode errorCode;
    //计算圆形面积
    double r = 2.0;
    double cArea = circle_area(r, &errorCode);
    printf("Circle with radius: %f has an area of: %f\n", r, cArea);
    //计算矩形面积
    double rwidth = 2.0;
    double rheight = 2.0;
    double rArea = rectangle_area(rwidth, rheight, &errorCode);
    printf("Rectangle with width: %f and height: %f has an area of: %f\n", rwidth, rheight, rArea);
    //计算三角形面积
    double tbase = 2.0;
    double theight = 2.0;
    double tArea = triangle_area(tbase, theight, &errorCode);
    printf("Triangle with base: %f and height: %f has an area of: %f\n", tbase, theight, tArea);
    //计算一组圆的面积
    double radii[] = { 1.0, 2.5, 3.0 };
    size_t count = sizeof(radii) / sizeof(radii[0]);
    double areas[count];
    calculate_areas(radii, count, areas, &errorCode);
    printf("Batch circle areas:\n");
    for (size_t i = 0; i < count; ++i) {
        printf("  radius=%f -> area=%f\n",radii[i],areas[i]);
    }
}

/**
 * @brief 测试开启日志测试计算面积
 */
void printAreaWithLog()
{
    ErrorCode errorCode;
    //计算圆形面积
    double r = 2.0;
    double cArea = circle_area(r, &errorCode);
    //计算矩形面积
    double rwidth = 2.0;
    double rheight = 2.0;
    double rArea = rectangle_area(rwidth, rheight, &errorCode);
    //计算三角形面积
    double tbase = 2.0;
    double theight = 2.0;
    double tArea = triangle_area(tbase, theight, &errorCode);
    //计算一组圆的面积
    double radii[] = { 1.0, 2.5, 3.0 };
    size_t count = sizeof(radii) / sizeof(radii[0]);
    double areas[count];
    calculate_areas(radii, count, areas, &errorCode);
}

int main()
{
    //测试计算面积
    printAreaWithoutLog();
    printf("\nRegister log callback\n\n");
    //设置回调函数
    g_set_log_callback(myCLog, NULL);
    //测试计算面积
    printAreaWithLog();
    system("pause");
}