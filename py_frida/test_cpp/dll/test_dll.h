#pragma once

#ifdef TEST_DLL_EXPORTS
#define TEST_DLL_API __declspec(dllexport)
#else
#define TEST_DLL_API __declspec(dllimport)
#endif

// Test class
class TestClass {
public:
    TestClass(int val) : value(val) {}
    int getValue() const { return value; }
    void setValue(int val) { value = val; }
    
private:
    int value;
};

// Test structure with class pointer and data pointer
struct TestData {
    int id;
    char name[64];
    TestClass* classPtr;
    void* dataPtr;
    int* intPtr;
    double value;
    void (*funcPtr)(); // 添加函数指针
};

// Exported functions
extern "C" {
    TEST_DLL_API int PublicFunction1(TestData* data);
    TEST_DLL_API void PublicFunction2(TestData* data);
    TEST_DLL_API double PublicFunction3(TestData* data);
}

// Internal functions (not exported)
int InternalFunction1(TestData* data);
void InternalFunction2(TestData* data);
char* InternalFunction3(TestData* data);