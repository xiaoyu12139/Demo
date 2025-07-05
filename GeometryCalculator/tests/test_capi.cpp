/**
 * @file test_capi.cpp
 * @brief c接口测试
 */
#include "geometry_c_api.h"
#include <gtest/gtest.h>

// 使用已知数值测试 circleArea
TEST(Geometry_C_API_Test, CircleArea) {
    double r = 1.0;
    double expected = 3.14159265358979323846; // pi * 1^2
    ErrorCode errorCode;
    EXPECT_DOUBLE_EQ(circle_area(r, &errorCode), expected);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    EXPECT_DOUBLE_EQ(circle_area(-1, &errorCode), -1);
    EXPECT_EQ(errorCode, GEO_ERR_NEGATIVE);

    r = 2.5;
    expected = PI * 2.5 * 2.5;
    EXPECT_NEAR(circle_area(r, &errorCode), expected, 1e-12);
    EXPECT_EQ(errorCode, GEO_SUCCESS);
}

// 使用已知数值测试 rectangleArea
TEST(Geometry_C_API_Test, RectangleArea) {
    double w = 3.0;
    double h = 4.0;
    double expected = 12.0;
    ErrorCode errorCode;
    EXPECT_DOUBLE_EQ(rectangle_area(w, h, &errorCode), expected);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    w = 5.5;
    h = 2.0;
    expected = 11.0;
    EXPECT_NEAR(rectangle_area(w, h, &errorCode), expected, 1e-12);
}

// 使用已知数值测试 rectangleArea
TEST(Geometry_C_API_Test, TriangleArea) {
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    ErrorCode errorCode;
    EXPECT_DOUBLE_EQ(triangle_area(base, h, &errorCode), expected);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    base = 5.5;
    h = 2.0;
    expected = 5.5;
    EXPECT_NEAR(triangle_area(base, h, &errorCode), expected, 1e-12);
}

// 测试空数组不会引发错误，并且不修改 out_areas
TEST(Geometry_C_API_Test, HandlesEmptyArray) {
    double radii[] = {};
    size_t count = 0;
    double out_areas[1] = { 42.0 };  // 预先填一个非零值
    ErrorCode errorCode;
    calculate_areas(radii, count, out_areas, &errorCode);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    // 对于空输入，不应修改 out_areas[0]
    EXPECT_DOUBLE_EQ(out_areas[0], 42.0);
}

// 测试正常数组能正确计算圆面积
TEST(Geometry_C_API_Test, ComputesCorrectAreas) {
    double radii[] = { 1.0, 2.5, 3.0 };
    size_t count = sizeof(radii) / sizeof(radii[0]);
    std::vector<double> expected;
    for (double r : radii) {
        expected.push_back(PI * r * r);
    }

    std::vector<double> out_areas(count, 0.0);
    ErrorCode errorCode;
    calculate_areas(radii, count, out_areas.data(), &errorCode);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    for (size_t i = 0; i < count; ++i) {
        EXPECT_NEAR(out_areas[i], expected[i], 1e-6)
            << "at index " << i << ": radius=" << radii[i];
    }
}

// 测试大规模数组性能/正确性（示例规模 1000）
TEST(Geometry_C_API_Test, HandlesLargeArray) {
    const size_t count = 1000;
    std::vector<double> radii(count, 1.23);
    std::vector<double> out_areas(count, 0.0);

    ErrorCode errorCode;
    calculate_areas(radii.data(), count, out_areas.data(), &errorCode);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    double expected = PI * 1.23 * 1.23;
    for (size_t i = 0; i < count; ++i) {
        EXPECT_NEAR(out_areas[i], expected, 1e-6)
            << "at index " << i;
    }
}

struct CallbackContext {
    CLogLevel lastLevel = CLogLevel::ERROR;  // 初始为最高，确保后续能检测到更低级别
    std::string  lastMessage;
    int          callCount   = 0;                // 记录回调被调用的次数
};

TEST(Geometry_C_API_Test, ReceivesCorrectLevelAndMessage) {
    CallbackContext ctx;

    // 注册回调：把 ctx 的指针作为 userdata 传入
    g_set_log_callback(
        // 捕获方式：拷贝 callback 参数本身，userdata 另行传入
        [](CLogLevel level, const char* message, void* userdata) {
            auto* c = static_cast<CallbackContext*>(userdata);
            c->lastLevel   = level;
            c->lastMessage = message;
            ++c->callCount;
        },
        &ctx
    );

    // 将阈值设为 INFO，防止过滤掉 INFO 及以上的日志
    set_glog_level(CLogLevel::INFO);

    // 调用带日志的接口
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    ErrorCode errorCode;
    EXPECT_DOUBLE_EQ(triangle_area(base, h, &errorCode), expected);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    // 回调应被调用三次，会输出debug,info,warn,error三条日志
    EXPECT_EQ(ctx.callCount, 3);
    // 消息中应包含两个计算结果
    EXPECT_NE(ctx.lastMessage.find(std::to_string(expected)), std::string::npos);
}

TEST(Geometry_C_API_Test, FiltersBelowThreshold) {
    CallbackContext ctx;

    // 阈值设为 WARN，INFO,DEBUG 级别的日志会被过滤
    set_glog_level(CLogLevel::WARN);

    g_set_log_callback(
        [](CLogLevel level, const char* message, void* userdata) {
            auto* c = static_cast<CallbackContext*>(userdata);
            ++c->callCount;
        },
        &ctx
    );

    // 调用带日志的接口
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    ErrorCode errorCode;
    EXPECT_DOUBLE_EQ(triangle_area(base, h, &errorCode), expected);
    EXPECT_EQ(errorCode, GEO_SUCCESS);

    // 只应该有WARN,ERROR日志被打印
    EXPECT_EQ(ctx.callCount, 2);
}