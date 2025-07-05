#ifndef GEOMETRY_EXPORT_H
#define GEOMETRY_EXPORT_H

#if defined(_WIN32)
#ifdef BUILDING_GEOMETRY_DLL
#define GEOMETRY_API __declspec(dllexport)
#else
#define GEOMETRY_API __declspec(dllimport)
#endif
#else//linux/macos下控制可见性
#define GEOMETRY_API __attribute__ ((visibility("default"))) 
#endif

#endif // GEOMETRY_EXPORT_H