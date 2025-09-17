# 自定义表格Demo

这是一个基于PySide6实现的自定义表格组件演示程序，提供了完整的数据接口用于设置和管理表格数据。

## 功能特性

### 核心功能
- ✅ **数据接口**: 提供`set_table_data()`接口，可一次性设置全表数据
- ✅ **动态操作**: 支持追加行、更新单元格、清空表格等操作
- ✅ **数据获取**: 提供`get_table_data()`接口获取当前表格所有数据
- ✅ **信号机制**: 支持单元格点击和数据变更信号
- ✅ **可编辑控制**: 可设置表格是否允许编辑

### UI特性
- 🎨 交替行颜色显示
- 🎨 自动调整列宽
- 🎨 隐藏行号显示
- 🎨 单行选择模式
- 🎨 最后一列自动拉伸

## 主要接口说明

### CustomTableWidget类

#### 核心方法

```python
# 设置表格数据（主要接口）
set_table_data(headers: List[str], data: List[List[Any]], editable: bool = True) -> bool

# 追加一行数据
append_row(row_data: List[Any]) -> bool

# 更新指定单元格
update_cell(row: int, column: int, value: Any) -> bool

# 获取所有表格数据
get_table_data() -> Dict[str, Any]

# 清空表格
clear_table()

# 设置列宽和行高
set_column_width(column: int, width: int)
set_row_height(row: int, height: int)
```

#### 信号

```python
# 数据变更信号
data_changed = Signal()

# 单元格点击信号 (行索引, 列索引, 单元格内容)
cell_clicked_signal = Signal(int, int, str)
```

## 使用示例

### 基本使用

```python
from custom_table_demo import CustomTableWidget

# 创建表格
table = CustomTableWidget()

# 设置数据
headers = ["姓名", "年龄", "职业"]
data = [
    ["张三", 25, "工程师"],
    ["李四", 30, "设计师"],
    ["王五", 28, "产品经理"]
]

# 通过接口设置全表数据
success = table.set_table_data(headers, data, editable=True)
if success:
    print("数据设置成功")

# 追加新行
table.append_row(["赵六", 32, "测试工程师"])

# 获取当前所有数据
current_data = table.get_table_data()
print(f"当前数据: {current_data}")
```

### 信号连接

```python
# 连接信号
table.cell_clicked_signal.connect(lambda row, col, text: print(f"点击: {row}, {col}, {text}"))
table.data_changed.connect(lambda: print("数据已变更"))
```

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行演示程序

```bash
python custom_table_demo.py
```

## 演示功能

运行程序后，你可以通过界面按钮体验以下功能：

- **加载示例数据1**: 加载学生信息数据
- **加载示例数据2**: 加载产品信息数据
- **追加行**: 随机追加一行数据
- **清空表格**: 清除所有数据
- **获取数据**: 显示当前表格的所有数据信息

## 数据格式

### 输入数据格式

```python
# headers: 表头列表
headers = ["列1", "列2", "列3"]

# data: 二维列表，每个子列表代表一行数据
data = [
    ["行1列1", "行1列2", "行1列3"],
    ["行2列1", "行2列2", "行2列3"]
]
```

### 输出数据格式

```python
{
    "headers": ["列1", "列2", "列3"],
    "data": [
        ["行1列1", "行1列2", "行1列3"],
        ["行2列1", "行2列2", "行2列3"]
    ],
    "row_count": 2,
    "column_count": 3
}
```

## 扩展说明

这个自定义表格组件可以轻松集成到其他PySide6应用中，只需要：

1. 导入`CustomTableWidget`类
2. 创建实例并添加到布局中
3. 使用提供的接口设置和管理数据
4. 根据需要连接相关信号

组件设计遵循了良好的封装原则，提供了清晰的接口，便于在实际项目中使用和扩展。