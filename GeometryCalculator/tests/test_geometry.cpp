/**
 * @file test_geometry.cpp
 * @brief 实现几何计算的 C++ 函数测试
 */
#include "geometry.h"
#include <gtest/gtest.h>

// 使用已知数值测试 circleArea
TEST(GeometryTest, CircleArea) {
    double r = 1.0;
    double expected = 3.14159265358979323846; // pi * 1^2
    EXPECT_DOUBLE_EQ(geometry::circleArea(r), expected);

    r = 2.5;
    expected = PI * 2.5 * 2.5;
    EXPECT_NEAR(geometry::circleArea(r), expected, 1e-12);
}

// 使用已知数值测试 rectangleArea
TEST(GeometryTest, RectangleArea) {
    double w = 3.0;
    double h = 4.0;
    double expected = 12.0;
    EXPECT_DOUBLE_EQ(geometry::rectangleArea(w, h), expected);

    w = 5.5;
    h = 2.0;
    expected = 11.0;
    EXPECT_NEAR(geometry::rectangleArea(w, h), expected, 1e-12);
}

// 使用已知数值测试 rectangleArea
TEST(GeometryTest, TriangleArea) {
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    EXPECT_DOUBLE_EQ(geometry::triangleArea(base, h), expected);

    base = 5.5;
    h = 2.0;
    expected = 5.5;
    EXPECT_NEAR(geometry::triangleArea(base, h), expected, 1e-12);
}

// 测试空输入，应该返回空向量
TEST(CalculateAreasCppTest, HandlesEmptyInput) {
    std::vector<double> radii;
    auto areas = geometry::calculateAreas(radii);
    EXPECT_TRUE(areas.empty());
}

// 测试若干不同半径，验证结果
TEST(CalculateAreasCppTest, ComputesCorrectAreas) {
    std::vector<double> radii = { 1.0, 2.5, 3.0 };
    std::vector<double> expected;
    expected.reserve(radii.size());
    for (double r : radii) {
        expected.push_back(PI * r * r);
    }

    auto areas = geometry::calculateAreas(radii);
    ASSERT_EQ(areas.size(), expected.size());
    for (size_t i = 0; i < areas.size(); ++i) {
        EXPECT_NEAR(areas[i], expected[i], 1e-6)
            << "at index " << i << ": radius=" << radii[i];
    }
}

// 测试大规模数组（比如 10000 个元素），验证性能及一致性
TEST(CalculateAreasCppTest, HandlesLargeInput) {
    const size_t N = 10000;
    std::vector<double> radii(N, 1.23);
    auto areas = geometry::calculateAreas(radii);

    ASSERT_EQ(areas.size(), N);
    double expected = PI * 1.23 * 1.23;
    for (size_t i = 0; i < N; ++i) {
        EXPECT_NEAR(areas[i], expected, 1e-6)
            << "at index " << i;
    }
}

struct RCallbackContext {
    geometry::RLogLevel     lastLevel   = geometry::RLogLevel::ERROR;  // 初始为最高，确保后续能检测到更低级别
    std::string  lastMessage;
    int          callCount   = 0;                // 记录回调被调用的次数
};

TEST(LogCallbackWithUserdata, ReceivesCorrectLevelAndMessage) {
    RCallbackContext ctx;

    // 注册回调：把 ctx 的指针作为 userdata 传入
    geometry::setLogCallback(
        // 捕获方式：拷贝 callback 参数本身，userdata 另行传入
        [](geometry::RLogLevel level, const char* message, void* userdata) {
            auto* c = static_cast<RCallbackContext*>(userdata);
            c->lastLevel   = level;
            c->lastMessage = message;
            ++c->callCount;
        },
        &ctx
    );

    // 将阈值设为 INFO，防止过滤掉 INFO 及以上的日志
    geometry::setGLogLevel(geometry::RLogLevel::INFO);

    // 调用带日志的接口
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    EXPECT_DOUBLE_EQ(geometry::triangleArea(base, h), expected);

    // 回调应被调用三次，会输出debug,info,warn,error三条日志
    EXPECT_EQ(ctx.callCount, 3);
    // 消息中应包含两个计算结果
    EXPECT_NE(ctx.lastMessage.find(std::to_string(expected)), std::string::npos);
}

TEST(LogCallbackWithFiltering, FiltersBelowThreshold) {
    RCallbackContext ctx;

    // 阈值设为 WARN，INFO,DEBUG 级别的日志会被过滤
    geometry::setGLogLevel(geometry::RLogLevel::WARN);

    geometry::setLogCallback(
        [](geometry::RLogLevel level, const char* message, void* userdata) {
            auto* c = static_cast<RCallbackContext*>(userdata);
            ++c->callCount;
        },
        &ctx
    );

    // 调用带日志的接口
    double base = 3.0;
    double h = 4.0;
    double expected = 6.0;
    EXPECT_DOUBLE_EQ(geometry::triangleArea(base, h), expected);

    // 只应该有WARN,ERROR日志被打印
    EXPECT_EQ(ctx.callCount, 2);
}

TEST(GeometryException, CircleAreaNegative) {
    EXPECT_THROW(geometry::circleArea(-1.0), std::invalid_argument);
}

TEST(GeometryException, RectangleAreaNegative) {
    EXPECT_THROW(geometry::rectangleArea(-2.0, 5.0), std::invalid_argument);
    EXPECT_THROW(geometry::rectangleArea(2.0, -5.0), std::invalid_argument);
}

TEST(GeometryException, TriangleAreaNegative) {
    EXPECT_THROW(geometry::triangleArea(-1.0, 3.0), std::invalid_argument);
}

TEST(GeometryException, CalculateAreasNegative) {
    std::vector<double> v = {1.0, -2.0, 3.0};
    EXPECT_THROW(geometry::calculateAreas(v), std::invalid_argument);
}