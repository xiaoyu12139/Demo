#include "test_dll.h"
#include <iostream>
#include <cstring>
#include <cstdlib>

// Exported function implementations
extern "C" {
    TEST_DLL_API int PublicFunction1(TestData* data) {
        if (!data) return -1;
        
        std::cout << "[PublicFunction1] Called with data:" << std::endl;
        std::cout << "  ID: " << data->id << std::endl;
        std::cout << "  Name: " << data->name << std::endl;
        std::cout << "  Value: " << data->value << std::endl;
        
        if (data->classPtr) {
            std::cout << "  ClassPtr value: " << data->classPtr->getValue() << std::endl;
        }
        
        if (data->intPtr) {
            std::cout << "  IntPtr value: " << *data->intPtr << std::endl;
        }
        
        // Call internal function
        InternalFunction1(data);
        
        return data->id * 2;
    }
    
    TEST_DLL_API void PublicFunction2(TestData* data) {
        if (!data) return;
        
        std::cout << "[PublicFunction2] Processing data..." << std::endl;
        data->value += 10.5;
        
        if (data->classPtr) {
            data->classPtr->setValue(data->classPtr->getValue() + 100);
        }
        
        // Call internal function
        InternalFunction2(data);
    }
    
    TEST_DLL_API double PublicFunction3(TestData* data) {
        if (!data) return 0.0;
        
        std::cout << "[PublicFunction3] Calculating result..." << std::endl;
        
        char* result = InternalFunction3(data);
        if (result) {
            std::cout << "  Internal result: " << result << std::endl;
            free(result);
        }
        
        return data->value * 1.5;
    }
}

// Internal function implementations (not exported)
int InternalFunction1(TestData* data) {
    if (!data) return -1;
    
    std::cout << "[InternalFunction1] Internal processing..." << std::endl;
    std::cout << "  Processing ID: " << data->id << std::endl;
    
    if (data->dataPtr) {
        std::cout << "  DataPtr is not null" << std::endl;
    }
    
    return data->id + 1000;
}

void InternalFunction2(TestData* data) {
    if (!data) return;
    
    std::cout << "[InternalFunction2] Modifying internal data..." << std::endl;
    
    // Modify some internal data
    if (strlen(data->name) > 0) {
        strcat_s(data->name, sizeof(data->name), "_modified");
    }
    
    if (data->intPtr) {
        *data->intPtr += 500;
    }
}

char* InternalFunction3(TestData* data) {
    if (!data) return nullptr;
    
    std::cout << "[InternalFunction3] Creating result string..." << std::endl;
    
    char* result = (char*)malloc(256);
    if (result) {
        sprintf_s(result, 256, "Processed: ID=%d, Name=%s, Value=%.2f", 
                 data->id, data->name, data->value);
    }
    
    return result;
}