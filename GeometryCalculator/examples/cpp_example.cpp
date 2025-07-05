/**
 * @file cpp_example.cpp
 * @brief 实现几何计算的 C++ 函数使用示例
 */
#include <iostream>
#include "geometry.h"
#include <thread>
#include <chrono>
using namespace std;

// cpp回调函数
// void myCLog(const char* message) {
//     printf("%s\n", message);
// }

/**
 * @brief cpp回调函数
 */
void myCLog(geometry::RLogLevel level, const char* message, void* userdata)
{
    std::cout << message << std::endl;
    //可以用level或着userdata进行一些其他自定义操作
}

/**
 * @brief 测试不开启日志测试计算面积
 */
void printAreaWithoutLog()
{
    //计算圆形面积
    double r = 2.0;
    double cArea = geometry::circleArea(r);
    printf("Circle with radius: %f has an area of: %f\n", r, cArea);
    //计算矩形面积
    double width = 2.0;
    double height = 2.0;
    double rArea = geometry::rectangleArea(width, height);
    printf("Rectangle with width: %f and height: %f has an area of: %f\n", width, height, rArea);
    //计算三角形面积
    double tbase = 2.0;
    double theight = 2.0;
    double tArea = geometry::triangleArea(tbase, theight);
    printf("Triangle with base: %f and height: %f has an area of: %f\n", tbase, theight, tArea);
    //计算一组圆的面积
    vector<double> radii{1.0, 2.5, 4.0};
    auto areas = geometry::calculateAreas(radii);
    cout << "Batch circle areas:" << endl;
    for (size_t i = 0; i < radii.size(); ++i) {
        cout << "  radius=" << radii[i] << " -> area=" << areas[i] << endl;
    }
}

/**
 * @brief 测试开启日志测试计算面积
 */
void printAreaWithLog()
{
    //计算圆形面积
    double r = 2.0;
    double cArea = geometry::circleArea(r);
    //计算矩形面积
    double width = 2.0;
    double height = 2.0;
    double rArea = geometry::rectangleArea(width, height);
    //计算三角形面积
    double tbase = 2.0;
    double theight = 2.0;
    double tArea = geometry::triangleArea(tbase, theight);
    //计算一组圆的面积
    vector<double> radii{1.0, 2.5, 4.0};
    auto areas = geometry::calculateAreas(radii);
}

/**
 * @brief 一个简单的线程函数：计算若干圆面积并打印，加锁
 */
void threadFuncSafeMtx(int aId, const std::vector<double>& aRadii) {
    for (double r : aRadii) {
        double a = geometry::circleAreaThreadMtx(r);
        // std::cout << "[Thread " << id << "] circleArea(" << r << ") = " << a << "\n";
        // 稍微睡一下，增加交错可能
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

/**
 * @brief 显示加锁的结果
 */
void testThreadMtx(){
    geometry::setLogCallback([](geometry::RLogLevel level, const char* message, void* userdata){});
    std::vector<double> radii = {1.0, 2.0, 3.0, 4.0, 5.0};
    // 并发启动 4 个线程
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(threadFuncSafeMtx, i, std::cref(radii));
    }
    // 等待所有线程结束
    for (auto& t : threads) {
        t.join();
    }
    std::cout << "All threads finished.\n";
}

/**
 * @brief 一个简单的线程函数：计算若干圆面积并打印，不加锁
 */
void threadFuncSafeNoMtx(int aId, const std::vector<double>& aRadii) {
    for (double r : aRadii) {
        double a = geometry::circleAreaThreadNoMtx(r);
        // std::cout << "[Thread " << id << "] circleArea(" << r << ") = " << a << "\n";
        // 稍微睡一下，增加交错可能
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

/**
 * @brief 显示不加锁的结果
 */
void testThreadNoMtx(){
    geometry::setLogCallback([](geometry::RLogLevel level, const char* message, void* userdata){});
    std::vector<double> radii = {1.0, 2.0, 3.0, 4.0, 5.0};
    // 并发启动 4 个线程
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(threadFuncSafeNoMtx, i, std::cref(radii));
    }
    // 等待所有线程结束
    for (auto& t : threads) {
        t.join();
    }
    std::cout << "All threads finished.\n";
}

int main()
{
    // geometry::testExport();
    //测试计算面积
    printAreaWithoutLog();
    cout << endl << "Register log callback" << endl << endl;
    //设置回调函数
    geometry::setLogCallback(myCLog);
    //测试计算面积
    printAreaWithLog();
    //多线程测试
    cout << endl << "Thread test No Mtx" << endl << endl;
    testThreadNoMtx();
    cout << endl << "Thread test Mtx" << endl << endl;
    testThreadMtx();
    system("pause");
}