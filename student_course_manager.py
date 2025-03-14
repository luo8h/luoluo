import tkinter as tk
from tkinter import ttk
import json
import os

class InputDialog:
    def __init__(self, parent, title, label_text, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        
        # 设置对话框位置为居中
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 计算居中位置
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 300
        dialog_height = 150
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # 创建输入框
        label = ttk.Label(self.dialog, text=label_text)
        label.pack(pady=10)
        
        self.entry = ttk.Entry(self.dialog, width=30)
        self.entry.pack(pady=10)
        
        # 创建按钮框架
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        # 创建确定和取消按钮
        ok_button = ttk.Button(button_frame, text="确定", command=lambda: self.on_ok(callback))
        ok_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=self.dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        self.entry.bind('<Return>', lambda e: self.on_ok(callback))
        self.entry.focus()
        
    def on_ok(self, callback):
        value = self.entry.get().strip()
        if value:
            callback(value)
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
        
        # 创建按钮
        add_name_button = ttk.Button(button_frame, text="添加姓名", command=self.add_name)
        add_name_button.pack(side=tk.LEFT, padx=5)
        
        add_course_button = ttk.Button(button_frame, text="添加课名", command=self.add_course)
        add_course_button.pack(side=tk.LEFT, padx=5)
        
        # 创建表格容器框架
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 设置表格样式
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Cell", relief="solid")
        style.configure("Treeview.Heading", font=('TkDefaultFont', 9, 'bold'))
        
        # 初始化列
        self.name_column_width = 120  # 姓名列宽度
        self.course_column_width = 80  # 课程列宽度
        self.course_columns = []  # 课程列
        
        # 创建10个初始课程列
        for i in range(1, 11):
            col_id = f"c{i}"
            self.course_columns.append(col_id)
        
        # 创建表格，包含序号、姓名和10个课程列
        all_columns = ["序号", "姓名"] + self.course_columns
        self.tree = ttk.Treeview(table_frame, columns=all_columns, 
                                show="headings", height=20)
        
        # 设置列属性
        self.tree.heading("序号", text="序号")
        self.tree.heading("姓名", text="姓名")
        self.tree.column("序号", width=self.name_column_width//2, anchor="center")
        self.tree.column("姓名", width=self.name_column_width, anchor="center")
        
        # 设置课程列的属性
        for col in self.course_columns:
            self.tree.heading(col, text=f"课程{col[1:]}")
            self.tree.column(col, width=self.course_column_width, anchor="center")
        
        # 添加滚动条
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        
        # 配置表格的滚动
        self.tree.configure(yscrollcommand=y_scrollbar.set,
                          xscrollcommand=x_scrollbar.set)
        
        # 放置表格和滚动条
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # 配置表格框架的网格权重
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # 初始化变量
        self.next_row_id = 1     # 下一个行ID
        
        # 绑定事件
        self.tree.bind("<Double-Button-1>", self.on_cell_double_click)
        
        # 设置窗口大小
        self.root.geometry("1000x600")
        
    def add_name(self):
        """添加姓名"""
        InputDialog(self.root, "添加姓名", "请输入姓名：", self.process_add_name)
        
    def process_add_name(self, name):
        """处理添加姓名"""
        # 添加新行，包含序号、姓名和10个空的课程列
        values = [self.next_row_id, name] + [""] * len(self.course_columns)
        item_id = f"I{self.next_row_id}"
        self.tree.insert("", "end", iid=item_id, values=values)
        self.next_row_id += 1
        
    def add_course(self):
        """添加课程"""
        InputDialog(self.root, "添加课程", "请输入课程名：", self.process_add_course)
        
    def process_add_course(self, course):
        """处理添加课程"""
        # 获取当前所有行的值
        current_values = {}
        for item in self.tree.get_children():
            current_values[item] = list(self.tree.item(item)["values"])
        
        # 保存所有列的标题
        titles = {}
        for col in self.course_columns:
            titles[col] = self.tree.heading(col)["text"]
        
        # 更新所有行的值，左移一位
        for item in self.tree.get_children():
            values = current_values[item]
            # 保持序号和姓名不变，只移动课程部分
            values = values[:2] + values[3:] + [""]
            current_values[item] = values
        
        # 更新列标题，左移一位
        for i in range(len(self.course_columns) - 1):
            self.tree.heading(self.course_columns[i], text=titles[self.course_columns[i + 1]])
        
        # 设置最后一列的标题为新课程名
        self.tree.heading(self.course_columns[-1], text=course)
        
        # 更新所有行的值
        for item in self.tree.get_children():
            self.tree.item(item, values=current_values[item])
            
    def on_cell_double_click(self, event):
        """处理单元格双击事件"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item and column:
            col_index = int(column.replace('#', '')) - 1
            values = list(self.tree.item(item)["values"])
            
            # 只允许修改课程列（第3列开始）
            if col_index >= 2 and col_index < len(values):
                values[col_index] = "✓" if values[col_index] != "✓" else ""
                self.tree.item(item, values=values)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main() 