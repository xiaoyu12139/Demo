#include <iostream>
#include <cstring>
#include <windows.h>
#include "../dll/test_dll.h"

// 测试函数，用于赋值给funcPtr
void TestFunction() {
    std::cout << "TestFunction called!" << std::endl;
}

int main() {
    std::cout << "=== DLL Hook Demo Main Program ===" << std::endl;
    std::cout << "Press any key to continue..." << std::endl;
    std::cin.get();
    
    // Create test data
    TestData testData = {0}; // 初始化所有字段为0
    testData.id = 12345;
    strcpy_s(testData.name, sizeof(testData.name), "TestObject");
    testData.value = 99.99;
    
    // Create test class instance
    TestClass* testClass = new TestClass(888);
    testData.classPtr = testClass;
    
    // Create some test data
    int* testInt = new int(777);
    testData.intPtr = testInt;
    
    char* testBuffer = new char[128];
    strcpy_s(testBuffer, 128, "This is test data buffer");
    testData.dataPtr = testBuffer;
    
    // 设置函数指针
    testData.funcPtr = TestFunction;
    
    std::cout << "\n--- Initial Data ---" << std::endl;
    std::cout << "ID: " << testData.id << std::endl;
    std::cout << "Name: " << testData.name << std::endl;
    std::cout << "Value: " << testData.value << std::endl;
    std::cout << "ClassPtr value: " << testData.classPtr->getValue() << std::endl;
    std::cout << "IntPtr value: " << *testData.intPtr << std::endl;
    
    std::cout << "\n--- Calling DLL Functions ---" << std::endl;
    
    // Call exported functions
    std::cout << "\n1. Calling PublicFunction1..." << std::endl;
    int result1 = PublicFunction1(&testData);
    std::cout << "Result: " << result1 << std::endl;
    
    std::cout << "\n2. Calling PublicFunction2..." << std::endl;
    PublicFunction2(&testData);
    
    std::cout << "\n3. Calling PublicFunction3..." << std::endl;
    double result3 = PublicFunction3(&testData);
    std::cout << "Result: " << result3 << std::endl;
    
    std::cout << "\n--- Final Data ---" << std::endl;
    std::cout << "ID: " << testData.id << std::endl;
    std::cout << "Name: " << testData.name << std::endl;
    std::cout << "Value: " << testData.value << std::endl;
    std::cout << "ClassPtr value: " << testData.classPtr->getValue() << std::endl;
    std::cout << "IntPtr value: " << *testData.intPtr << std::endl;
    
    // Clean up resources
    delete testClass;
    delete testInt;
    delete[] testBuffer;
    
    std::cout << "\n=== Program finished. Press any key to exit ===" << std::endl;
    system("pause");
    
    return 0;
}