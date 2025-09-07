console.log("[+] Starting hook script for test_dll...");

// 列出已加载的模块
console.log("[*] Enumerating loaded modules...");
Process.enumerateModules().forEach(function(module) {
    console.log("[+] Found module: " + module.name + " at " + module.base);
    if (module.name.toLowerCase().includes("test_dll")) {
        console.log("[***] Target DLL found: " + module.name + " at " + module.base);
    }
});

// printTestData 函数 - 从 dll_hook_utils.js 移回到这里
function printTestData(dataPtr, functionName) {
    try {
        if (dataPtr.isNull()) {
            console.log("    [" + functionName + "] Data pointer is NULL");
            return;
        }
        
        console.log("    [" + functionName + "] Data structure:");

        var id = dataPtr.readInt();
        console.log("id: " + id);

        var name = readString(dataPtr.add(4), 64);
        console.log("name: " + name);

        var classPtr = dataPtr.add(72);
        console.log("classPtr: " + classPtr);

        var dataPtrField = dataPtr.add(80);
        console.log("dataPtr: " + dataPtrField);

        var intPtr = dataPtr.add(88);
        console.log("intPtr: " + intPtr);
        console.log("intPtr value: " + intPtr.readPointer().readInt());

        var value = dataPtr.add(96).readDouble();
        console.log("value: " + value);

        var funcPtr = dataPtr.add(104);
        console.log("funcPtr: " + funcPtr);
        var firstDeref = funcPtr.readPointer();
        console.log("first deref: " + firstDeref);
        console.log("funcName (single deref): " + getFunctionName(firstDeref));
        } catch (e) {
            console.log("    [" + functionName + "] Error reading data: " + e.message);
        }
}

// 通用hook函数已移至 dll_hook_utils.js

// Hook test_dll 对外暴露的函数
try {
    var testDllModule = Process.getModuleByName("test_dll.dll");
    
    // Hook PublicFunction1 - 在onEnterHandler中执行printTestData
    hookExportedFunction(testDllModule, "PublicFunction1", function(args) {
        console.log("\n[*] PublicFunction1 called:");
        printTestData(args[0], "PublicFunction1");
    },function(args) {});
    
    // Hook PublicFunction2 - 在onEnterHandler中执行printTestData并添加自定义处理
    hookExportedFunction(testDllModule, "PublicFunction2", function(args) {
        console.log("\n[*] PublicFunction2 called with CUSTOM handler:");
        printTestData(args[0], "PublicFunction2");
    },function(args) {});
    
    // Hook PublicFunction3 - 在onEnterHandler中执行printTestData并添加特殊处理
    hookExportedFunction(testDllModule, "PublicFunction3", function(args) {
        console.log("\n[*] PublicFunction3 called with INLINE custom handler:");
        printTestData(args[0], "PublicFunction3");
    },function(args) {});
    
} catch (e) {
    console.log("[-] test_dll module not found or error: " + e.message);
}

// 查找内部函数地址的通用函数已移至 dll_hook_utils.js

// Hook test_dll 内部函数（不对外暴露）
try {
    var testDllModule = Process.getModuleByName("test_dll.dll");
    
    // 查找所有内部函数
    var internalFunctions = findInternalFunctions(testDllModule);
    
    // Hook InternalFunction1 - 在onEnterHandler中执行printTestData
    hookInternalFunction(internalFunctions.InternalFunction1, "InternalFunction1", function(args) {
        console.log("\n[*] InternalFunction1 called (INTERNAL):");
        printTestData(args[0], "InternalFunction1");
    },function(args) {});
    
    // Hook InternalFunction2 - 在onEnterHandler中执行printTestData并添加自定义处理
    hookInternalFunction(internalFunctions.InternalFunction2, "InternalFunction2", function(args) {
        console.log("\n[*] InternalFunction2 called (INTERNAL) with CUSTOM handler:");
        printTestData(args[0], "InternalFunction2");
    },function(args) {});
    
    // Hook InternalFunction3 - 在onEnterHandler中执行printTestData并添加特殊处理
    hookInternalFunction(internalFunctions.InternalFunction3, "InternalFunction3", function(args) {
        console.log("\n[*] InternalFunction3 called (INTERNAL) with INLINE handler:");
        printTestData(args[0], "InternalFunction3");
    },function(args) {});
    
    if (Object.keys(internalFunctions).length === 0) {
        console.log("[-] No internal functions found. They may be inlined or optimized out.");
        console.log("[*] Try building the DLL with debug information and no optimization.");
    }
    
} catch (e) {
    console.log("[-] Error hooking internal functions: " + e.message);
}

console.log("[+] Hooks installed, monitoring started...");