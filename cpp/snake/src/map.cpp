#include "map.h"
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

void Map::PrintInitmap()//绘制初始地图
{
    for (auto& point : initmap)
    {
        point.Print();
        #ifdef _WIN32
            Sleep(10);//调用Sleep函数可营造动画效果
        #else
            usleep(10 * 1000);
        #endif
    }
}
