// DLL Hook 工具函数库
// 提供通用的hook功能和辅助函数

function readString(fieldPtr, fieldSize) {
    var nameBytes = new Uint8Array(fieldPtr.readByteArray(fieldSize));
    var value = "";
    for (var i = 0; i < fieldSize; i++) {
        var byte = nameBytes[i];
        if (byte === 0) break;
        if (byte >= 32 && byte <= 126) {
            value += String.fromCharCode(byte);
        }
    }
    return value;
}

// 函数名称解析函数
// 在 getFunctionName 函数中添加
function getFunctionName(funcPtr) {
    if (!funcPtr || funcPtr.isNull()) {
        return "[NULL Function Pointer]";
    }
    
    try {
        // 尝试获取符号信息
        const symbol = DebugSymbol.fromAddress(funcPtr);
        if (symbol && symbol.name) {
            // 如果是修饰名，尝试去修饰
            let name = symbol.name;
            
            // 简单的去修饰处理
            if (name.includes('?') && name.includes('@@')) {
                // MSVC 修饰名格式
                const match = name.match(/\?([^@]+)@@/);
                if (match) {
                    return match[1]; // 返回原始函数名
                }
            }
            
            // 如果包含 ILT，提取实际函数名
            if (name.includes('ILT+')) {
                const match = name.match(/\?([^Y]+)Y/);
                if (match) {
                    return match[1];
                }
            }
            
            return name;
        }
    } catch (e) {
        console.log(`[!] Error getting symbol: ${e.message}`);
    }
    
    return `[Unknown Function at ${funcPtr}]`;
}

// 通过模式扫描尝试找到函数名称
function scanForFunctionName(funcPtr, module, patterns = [
            "SampleFunction",
            "AnotherFunction",
            "TestFunction",
            "Function"
        ]) {
    try {
        // 在函数地址附近搜索可能的函数名字符串
        var searchRange = 0x1000; // 搜索范围
        var startAddr = funcPtr.sub(searchRange);
        if (startAddr.compare(module.base) < 0) {
            startAddr = module.base;
        }
        
        var endAddr = funcPtr.add(searchRange);
        if (endAddr.compare(module.base.add(module.size)) > 0) {
            endAddr = module.base.add(module.size);
        }
        
        for (var i = 0; i < patterns.length; i++) {
            var pattern = patterns[i];
            try {
                Memory.scan(startAddr, endAddr.sub(startAddr).toInt32(), pattern, {
                    onMatch: function(address, size) {
                        // 检查找到的字符串是否在合理的位置
                        var distance = Math.abs(address.sub(funcPtr).toInt32());
                        if (distance < 0x500) { // 500字节范围内
                            return pattern;
                        }
                    }
                });
            } catch (e) {
                // 继续尝试下一个模式
            }
        }
        
        return null;
    } catch (e) {
        return null;
    }
}


// 通用hook函数 - 用于hook导出函数
function hookExportedFunction(module, functionName, onEnterHandler, onLeaveHandler) {
    try {
        var funcAddr = module.getExportByName(functionName);
        if (funcAddr) {
            console.log("[+] Found " + functionName + " at: " + funcAddr);
            
            Interceptor.attach(funcAddr, {
                onEnter: function(args) {
                    onEnterHandler(args, functionName);
                },
                
                onLeave: function(retval) {
                    onLeaveHandler(retval, functionName);
                }
            });
            return true;
        } else {
            console.log("[-] " + functionName + " not found");
            return false;
        }
    } catch (e) {
        console.log("[-] Error hooking " + functionName + ": " + e.message);
        return false;
    }
}

// 通用hook函数 - 用于hook内部函数
function hookInternalFunction(functionAddr, functionName, onEnterHandler, onLeaveHandler) {
    if (!functionAddr) {
        return false;
    }
    
    try {
        Interceptor.attach(functionAddr, {
            onEnter: function(args) {
                onEnterHandler(args, functionName);
            },
            
            onLeave: function(retval) {
                onLeaveHandler(retval, functionName);
            }
        });
        return true;
    } catch (e) {
        console.log("[-] Error hooking " + functionName + ": " + e.message);
        return false;
    }
}

// 查找内部函数地址的通用函数
function findInternalFunctions(module, fun_name = "InternalFunction") {
    var internalFunctions = {};
    
    // 方法1: 尝试通过符号查找
    try {
        var symbols = module.enumerateSymbols();
        symbols.forEach(function(symbol) {
            if (symbol.name.includes(fun_name)) {
                internalFunctions.InternalFunction1 = symbol.address;
                console.log("[+] Found InternalFunction1 at: " + symbol.address);
            } 
        });
    } catch (e) {
        console.log("[*] Symbol enumeration failed, trying pattern scanning...");
    }
    
    // 方法2: 如果符号查找失败，使用模式扫描
    if (Object.keys(internalFunctions).length === 0) {
        console.log("[*] Attempting pattern scanning for internal functions...");
        
        // 扫描包含特定字符串的函数
        var ranges = Process.enumerateRanges('r-x').filter(function(range) {
            return range.file && range.file.path && range.file.path.includes('test_dll');
        });
        
        ranges.forEach(function(range) {
            try {
                // 查找包含"InternalFunction1"字符串的位置
                Memory.scan(range.base, range.size, "49 6e 74 65 72 6e 61 6c 46 75 6e 63 74 69 6f 6e 31", {
                    onMatch: function(address, size) {
                        console.log("[*] Found Function string reference at: " + address);
                    },
                    onComplete: function() {}
                });
            } catch (e) {
                // 忽略扫描错误
            }
        });
    }
    
    return internalFunctions;
}

// 简化版内存扫描查找内部函数
function findInternalFunctionsByScan(module) {
    var internalFunctions = {};
    var foundCount = 0;
    var maxResults = 20;
    
    console.log("[*] Starting simplified memory scan...");
    
    try {
        // 方法1: 扫描函数序言模式
        var patterns = [
            "48 89 4C 24 08",      // push ebp; mov ebp, esp (x86)
            "57",   // mov [rsp+xx], rbx (x64)
            "48 83 EC 50",   // mov [rsp+xx], rbx (x64)
            "48 83 7C 24 60 00",   // mov [rsp+xx], rbx (x64)
            "75 0A",   // mov [rsp+xx], rbx (x64)
        ];
        
        // 将数组拼接成长串字节码
        var combinedPattern = patterns.join(" ");
        console.log(`[*] Combined pattern: ${combinedPattern}`);
        
        // 获取模块的可执行内存范围
        var moduleRange = {
            base: module.base,
            size: module.size
        };
        
        try {
            Memory.scan(moduleRange.base, moduleRange.size, combinedPattern, {
                onMatch: function(address, size) {
                    var funcName = `InternalFunc_1`;
                    internalFunctions[funcName] = address;
                    
                    console.log(`[+] Found function at ${address} (${funcName})`);
                },
                onComplete: function() {}
            });
        } catch (e) {
            console.log(`[!] Pattern scan error: ${e.message}`);
        }
        
    } catch (e) {
        console.log(`[!] Memory scan error: ${e.message}`);
    }
    
    console.log(`[*] Scan completed, found ${foundCount} functions`);
    return internalFunctions;
}
