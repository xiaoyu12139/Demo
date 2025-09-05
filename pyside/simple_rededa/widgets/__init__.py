"""Widgets包初始化文件。

本包包含应用程序中使用的各种自定义组件，按功能模块分类：
- text_edit_widgets: 文本编辑模式相关组件
- list_manage_widgets: 列表管理模式相关组件  
- drawing_widgets: 绘图设计模式相关组件
"""

from .demo_text_edit_widgets import TextCanvasWidget, TextOperationWidget
from .demo_list_manage_widgets import ListCanvasWidget, ListOperationWidget
from .demo_drawing_widgets import DrawingCanvasWidget, DrawingOperationWidget, DrawingArea
from .get_widget_data_windows import GetWidgetDataCanvasWidget, GetWidgetDataOperationWidget
