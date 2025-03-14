import tkinter as tk
from tkinter import ttk
import json
import os
import time

class InputDialog:
    def __init__(self, parent, title, label_text, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        
        # 保存回调函数
        self.callback = callback
        
        # 设置对话框位置为居中
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.center_dialog(parent)
        
        # 创建输入框
        label = ttk.Label(self.dialog, text=label_text)
        label.pack(pady=10)
        
        self.entry = ttk.Entry(self.dialog, width=30)
        self.entry.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        # 创建确定按钮
        ok_button = ttk.Button(button_frame, text="确定", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # 创建取消按钮
        cancel_button = ttk.Button(button_frame, text="取消", command=self.dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        self.entry.bind('<Return>', lambda e: self.on_ok())
        
        # 设置焦点到输入框
        self.entry.focus()
        
    def center_dialog(self, parent):
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 300
        dialog_height = 150
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
    def on_ok(self):
        if self.entry.get().strip():
            self.callback(self.entry.get().strip())
            self.dialog.destroy()

class ActionDialog:
    def __init__(self, parent, title, callback_delete, callback_add):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("200x100")
        
        # 设置对话框位置为居中
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.center_dialog(parent)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(expand=True)
        
        # 创建删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=lambda: self.on_action(callback_delete))
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # 创建增加按钮
        add_button = ttk.Button(button_frame, text="增加", command=lambda: self.on_action(callback_add))
        add_button.pack(side=tk.LEFT, padx=5)
        
    def center_dialog(self, parent):
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 200
        dialog_height = 100
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
    def on_action(self, callback):
        callback()
        self.dialog.destroy()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("学生背课录入程序")
        
        # 设置主窗口的内边距
        self.root.configure(padx=10, pady=10)
        
        # 创建主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建添加姓名按钮
        add_name_button = ttk.Button(button_frame, text="添加姓名", command=self.add_name)
        add_name_button.pack(side=tk.LEFT, padx=5)
        
        # 创建添加课名按钮
        add_course_button = ttk.Button(button_frame, text="添加课名", command=self.add_course)
        add_course_button.pack(side=tk.LEFT, padx=5)
        
        # 创建表格容器框架
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建固定列框架和可滚动列框架
        fixed_frame = ttk.Frame(table_frame)
        fixed_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        scroll_frame = ttk.Frame(table_frame)
        scroll_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 设置表格样式
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Cell", relief="solid")
        style.configure("Treeview.Heading", font=('TkDefaultFont', 9, 'bold'))
        
        # 创建固定列表格（序号和姓名）
        self.fixed_tree = ttk.Treeview(fixed_frame, columns=["序号", "姓名"], 
                                      show="headings", height=20)
        self.fixed_tree.heading("序号", text="序号")
        self.fixed_tree.heading("姓名", text="姓名")
        self.fixed_tree.column("序号", width=50, anchor="center")
        self.fixed_tree.column("姓名", width=100, anchor="center")
        
        # 创建可滚动课程表格
        self.scroll_tree = ttk.Treeview(scroll_frame, columns=[], 
                                       show="headings", height=20)
        
        # 添加垂直滚动条
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加水平滚动条
        x_scrollbar = ttk.Scrollbar(scroll_frame, orient="horizontal")
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 配置滚动条
        self.fixed_tree.configure(yscrollcommand=y_scrollbar.set)
        self.scroll_tree.configure(yscrollcommand=y_scrollbar.set,
                                 xscrollcommand=x_scrollbar.set)
        y_scrollbar.configure(command=self.yview_both)
        x_scrollbar.configure(command=self.scroll_tree.xview)
        
        # 打包表格
        self.fixed_tree.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 初始化变量
        self.course_columns = []  # 课程列
        self.next_row_id = 1     # 下一个行ID
        self.dragging = False    # 拖动状态
        self.last_selected = None # 最后选中的单元格
        
        # 绑定事件
        self.bind_events()
        
        # 加载保存的数据
        self.load_data()
        
        # 设置窗口大小
        self.root.geometry("1000x600")
        
        # 关闭窗口时保存数据
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def bind_events(self):
        # 双击事件
        self.fixed_tree.bind("<Double-Button-1>", self.on_fixed_double_click)
        self.scroll_tree.bind("<Double-Button-1>", self.on_scroll_double_click)
        
        # 单击事件
        self.fixed_tree.bind("<ButtonPress-1>", self.on_click)
        self.scroll_tree.bind("<ButtonPress-1>", self.on_click)
        
        # 拖动事件
        self.scroll_tree.bind("<B1-Motion>", self.on_drag)
        self.scroll_tree.bind("<ButtonRelease-1>", self.on_release)
        
    def yview_both(self, *args):
        """同步两个表格的垂直滚动"""
        self.fixed_tree.yview(*args)
        self.scroll_tree.yview(*args)
        
    def add_name(self):
        """添加姓名"""
        InputDialog(self.root, "添加姓名", "请输入姓名：", self.process_add_name)
        
    def process_add_name(self, name):
        """处理添加姓名"""
        # 在固定列表格中添加行
        values = [self.next_row_id, name]
        item_id = f"I{self.next_row_id}"
        self.fixed_tree.insert("", "end", iid=item_id, values=values)
        
        # 在课程表格中添加对应的空行
        empty_values = [""] * len(self.course_columns)
        self.scroll_tree.insert("", "end", iid=item_id, values=empty_values)
        
        self.next_row_id += 1
        
    def add_course(self):
        """添加课程"""
        InputDialog(self.root, "添加课程", "请输入课程名：", self.process_add_course)
        
    def process_add_course(self, course):
        """处理添加课程"""
        MAX_VISIBLE_COLUMNS = 8  # 最大可见列数（不包括序号和姓名列）
        
        # 获取当前所有行的值
        current_values = {}
        for item in self.scroll_tree.get_children():
            current_values[item] = list(self.scroll_tree.item(item)["values"])
        
        # 生成新列ID
        new_col_id = f"c{len(self.course_columns) + 1}"
        
        # 如果已达到最大可见列数，将课程列整体左移
        if len(self.course_columns) >= MAX_VISIBLE_COLUMNS:
            # 保存所有列的标题和值
            titles = {}
            for col in self.course_columns:
                titles[col] = self.scroll_tree.heading(col)["text"]
            
            # 更新所有行的值，左移一位
            for item in self.scroll_tree.get_children():
                values = current_values[item]
                # 左移一位并在末尾添加空值
                values = values[1:] + [""]
                current_values[item] = values
            
            # 更新列标题，左移一位
            for i in range(len(self.course_columns) - 1):
                self.scroll_tree.heading(self.course_columns[i], text=titles[self.course_columns[i + 1]])
            
            # 设置最后一列的标题为新课程名
            self.scroll_tree.heading(self.course_columns[-1], text=course)
        else:
            # 添加新列到列表末尾
            self.course_columns.append(new_col_id)
            
            # 更新表格列配置
            self.scroll_tree.configure(columns=self.course_columns)
            
            # 设置新列的属性
            self.scroll_tree.heading(new_col_id, text=course)
            self.scroll_tree.column(new_col_id, width=80, anchor="center")
            
            # 为所有行添加空值
            for item in self.scroll_tree.get_children():
                values = current_values.get(item, [])
                if values is None:
                    values = []
                # 添加新列的空值
                values.append("")
                current_values[item] = values
        
        # 更新所有行的值
        for item in self.scroll_tree.get_children():
            self.scroll_tree.item(item, values=current_values[item])
        
    def update_all_columns_width(self):
        """更新所有列的宽度为统一值"""
        for col in self.course_columns:
            self.scroll_tree.column(col, width=80, anchor="center")
            
    def on_fixed_double_click(self, event):
        """处理固定列双击事件"""
        item = self.fixed_tree.identify_row(event.y)
        if item:
            ActionDialog(self.root,
                        "操作选择",
                        lambda: self.delete_row(item),
                        lambda: self.insert_row(item))
            
    def on_scroll_double_click(self, event):
        """处理课程表格双击事件"""
        region = self.scroll_tree.identify_region(event.x, event.y)
        item = self.scroll_tree.identify_row(event.y)
        column = self.scroll_tree.identify_column(event.x)
        
        if region == "heading":
            # 双击表头
            if column:
                self.current_column = column
                ActionDialog(self.root,
                           "操作选择",
                           self.delete_column,
                           self.insert_column)
        elif region == "cell":
            # 双击单元格
            if item and column:
                self.toggle_cell(item, column)
                
    def delete_row(self, item):
        """删除行"""
        # 删除两个表格中的行
        self.fixed_tree.delete(item)
        self.scroll_tree.delete(item)
        
        # 更新序号
        self.update_row_numbers()
        
    def insert_row(self, item):
        """插入行"""
        InputDialog(self.root, "插入姓名", "请输入姓名：",
                   lambda name: self.process_insert_row(item, name))
        
    def process_insert_row(self, after_item, name):
        """处理插入行"""
        # 获取插入位置的索引
        index = self.fixed_tree.index(after_item) + 1
        
        # 创建新行ID
        new_item = f"I{self.next_row_id}"
        
        # 插入固定列
        self.fixed_tree.insert("", index, iid=new_item,
                             values=[self.next_row_id, name])
        
        # 插入课程列
        empty_values = [""] * len(self.course_columns)
        self.scroll_tree.insert("", index, iid=new_item,
                              values=empty_values)
        
        self.next_row_id += 1
        
        # 更新序号
        self.update_row_numbers()
        
    def update_row_numbers(self):
        """更新序号列"""
        items = self.fixed_tree.get_children()
        for i, item in enumerate(items, 1):
            values = list(self.fixed_tree.item(item)["values"])
            values[0] = i
            self.fixed_tree.item(item, values=values)
            
    def delete_column(self):
        """删除列"""
        if not hasattr(self, 'current_column'):
            return
            
        col_index = int(self.current_column.replace('#', '')) - 1
        if 0 <= col_index < len(self.course_columns):
            # 删除列
            removed_col = self.course_columns.pop(col_index)
            
            # 更新表格列
            self.scroll_tree.configure(columns=self.course_columns)
            
            # 更新所有行的值
            for item in self.scroll_tree.get_children():
                values = list(self.scroll_tree.item(item)["values"])
                values.pop(col_index)
                self.scroll_tree.item(item, values=values)
                
            # 更新所有列的宽度
            self.update_all_columns_width()
            
    def insert_column(self):
        """插入列"""
        if not hasattr(self, 'current_column'):
            return
            
        InputDialog(self.root, "插入课程", "请输入课程名：",
                   self.process_insert_column)
        
    def process_insert_column(self, course):
        """处理插入列"""
        col_index = int(self.current_column.replace('#', '')) - 1
        
        # 生成新列ID
        new_col = f"c{len(self.course_columns) + 1}"
        
        # 插入新列到指定位置
        self.course_columns.insert(col_index + 1, new_col)
        
        # 更新表格列
        self.scroll_tree.configure(columns=self.course_columns)
        
        # 设置新列属性
        self.scroll_tree.heading(new_col, text=course)
        
        # 更新所有列的宽度
        self.update_all_columns_width()
        
        # 更新所有行的值（在指定位置插入空值）
        for item in self.scroll_tree.get_children():
            values = list(self.scroll_tree.item(item)["values"])
            values.insert(col_index + 1, "")  # 在指定位置插入空值
            self.scroll_tree.item(item, values=values)
            
    def toggle_cell(self, item, column):
        """切换单元格状态"""
        values = list(self.scroll_tree.item(item)["values"])
        col_index = int(column.replace('#', '')) - 1
        
        if 0 <= col_index < len(values):
            values[col_index] = "✓" if values[col_index] != "✓" else ""
            self.scroll_tree.item(item, values=values)
            
    def on_click(self, event):
        """处理单击事件"""
        tree = event.widget
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        
        if tree == self.scroll_tree:
            self.last_selected = (item, column)
            
    def on_drag(self, event):
        """处理拖动事件"""
        if not self.last_selected:
            return
            
        item = self.scroll_tree.identify_row(event.y)
        column = self.scroll_tree.identify_column(event.x)
        
        if item and column and (item, column) != self.last_selected:
            # 交换单元格值
            old_item, old_column = self.last_selected
            self.swap_cells(old_item, old_column, item, column)
            self.last_selected = (item, column)
            
    def swap_cells(self, item1, col1, item2, col2):
        """交换两个单元格的值"""
        values1 = list(self.scroll_tree.item(item1)["values"])
        values2 = list(self.scroll_tree.item(item2)["values"])
        
        col_index1 = int(col1.replace('#', '')) - 1
        col_index2 = int(col2.replace('#', '')) - 1
        
        values1[col_index1], values2[col_index2] = values2[col_index2], values1[col_index1]
        
        self.scroll_tree.item(item1, values=values1)
        self.scroll_tree.item(item2, values=values2)
        
    def on_release(self, event):
        """处理释放事件"""
        self.last_selected = None
        
    def save_data(self):
        """保存数据到文件"""
        data = {
            'next_row_id': self.next_row_id,
            'course_columns': self.course_columns,
            'courses': {},
            'names': {},
            'values': {}
        }
        
        # 保存课程名
        for col in self.course_columns:
            data['courses'][col] = self.scroll_tree.heading(col)['text']
            
        # 保存姓名和值
        for item in self.fixed_tree.get_children():
            fixed_values = self.fixed_tree.item(item)['values']
            scroll_values = self.scroll_tree.item(item)['values']
            
            data['names'][item] = fixed_values
            data['values'][item] = scroll_values
            
        # 保存到文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def load_data(self):
        """从文件加载数据"""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.next_row_id = data['next_row_id']
            self.course_columns = data['course_columns']
            
            # 恢复课程列
            if self.course_columns:
                self.scroll_tree.configure(columns=self.course_columns)
                for col in self.course_columns:
                    self.scroll_tree.heading(col, text=data['courses'][col])
                    self.scroll_tree.column(col, width=80, anchor="center")
                    
            # 恢复数据
            for item, name_values in data['names'].items():
                self.fixed_tree.insert("", "end", iid=item, values=name_values)
                self.scroll_tree.insert("", "end", iid=item, values=data['values'][item])
                
        except FileNotFoundError:
            pass
            
    def on_closing(self):
        """关闭窗口时的处理"""
        self.save_data()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main() 