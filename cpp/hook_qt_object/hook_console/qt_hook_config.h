#pragma once

// 在你的 Qt5Core.dll 中查找导出的装饰名（MSVC 示例）。
// 使用 dumpbin/Dependency Walker/PE-bear 查得后替换下方字符串。
#ifndef QMETAOBJECT_CONNECT_SYMBOL
#define QMETAOBJECT_CONNECT_SYMBOL  "?connect@QMetaObject@@..."  // TODO: 替换为实际导出名
#endif
#ifndef QMETAOBJECT_ACTIVATE_SYMBOL
#define QMETAOBJECT_ACTIVATE_SYMBOL "?activate@QMetaObject@@..." // TODO: 替换为实际导出名
#endif