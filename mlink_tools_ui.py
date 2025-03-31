import os
import shutil
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class DirectoryMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("大目录迁移工具")
        self.root.geometry("500x300")
        self.last_operation = None  # 新增：记录最后一次操作信息
        
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 源目录部分
        ttk.Label(self.main_frame, text="源目录路径：").grid(row=0, column=0, sticky=tk.W)
        self.source_entry = ttk.Entry(self.main_frame, width=40)
        self.source_entry.grid(row=1, column=0, sticky=tk.EW)
        ttk.Button(self.main_frame, text="浏览...", command=self.browse_source).grid(row=1, column=1, padx=5)

        # 目标目录部分
        ttk.Label(self.main_frame, text="目标父目录路径：").grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        self.target_entry = ttk.Entry(self.main_frame, width=40)
        self.target_entry.grid(row=3, column=0, sticky=tk.EW)
        ttk.Button(self.main_frame, text="浏览...", command=self.browse_target).grid(row=3, column=1, padx=5)

        # 操作按钮（新增撤销按钮）
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(self.btn_frame, text="执行迁移", command=self.process).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="撤销", command=self.undo).pack(side=tk.LEFT, padx=5)  # 新增撤销按钮
        ttk.Button(self.btn_frame, text="帮助", command=self.show_help).pack(side=tk.LEFT)

        self.main_frame.columnconfigure(0, weight=1)

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)

    def browse_target(self):
        path = filedialog.askdirectory()
        if path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, path)

    def show_help(self):
        help_text = """
        使用方法：
        本程序用于将原始目录移动到目标父目录下的同名子目录，
        并在原位置创建符号链接。
        
        步骤：
        1. 选择源目录路径
        2. 选择目标父目录路径
        3. 自动在目标路径下创建同名子目录并迁移内容
        
        注意：
        - 请使用绝对路径
        - Windows可能需要管理员权限
        - 自动处理目录创建无需确认
        """
        messagebox.showinfo("帮助信息", help_text)

    def process(self):
        source = self.source_entry.get().strip()
        target_parent = self.target_entry.get().strip()

        if not source or not os.path.exists(source):
            messagebox.showerror("错误", f"源目录不存在: {source}")
            return
        
        source_basename = os.path.basename(source.rstrip(os.sep))
        final_target = os.path.join(target_parent, source_basename)

        if os.path.exists(target_parent) and not os.path.isdir(target_parent):
            messagebox.showerror("错误", "目标路径是一个文件路径")
            return

        try:
            os.makedirs(target_parent, exist_ok=True)
        except Exception as e:
            messagebox.showerror("错误", f"创建目标路径失败: {str(e)}")
            return

        if not messagebox.askyesno("确认", 
            f"即将执行：\n1. 移动目录: {source} ➔ {final_target}\n2. 创建符号链接\n是否继续？"):
            return

        # 移动目录
        try:
            shutil.move(source, final_target)
        except Exception as e:
            messagebox.showerror("错误", f"目录移动失败: {str(e)}")
            return

        # 创建符号链接
        try:
            if platform.system() == "Windows":
                os.symlink(final_target, source, target_is_directory=True)
            else:
                os.symlink(final_target, source)
        except OSError as e:
            messagebox.showerror("错误", f"创建符号链接失败: {str(e)}\nWindows可能需要管理员权限")
            self.rollback_movement(source, final_target)
            return

        # 记录操作以便撤销
        self.last_operation = {
            'source': source,
            'target': final_target,
            'symbolic_link': source
        }

        messagebox.showinfo("成功", "操作完成！")

    def rollback_movement(self, source, target):
        if messagebox.askyesno("回滚", "检测到符号链接失败，是否回滚移动操作？"):
            try:
                shutil.move(target, source)
                messagebox.showinfo("成功", "回滚完成")
            except Exception as e:
                messagebox.showerror("错误", f"回滚失败: {str(e)}\n请手动移动 {target} 回到 {source}")

    def undo(self):
        if not self.last_operation:
            messagebox.showinfo("撤销", "没有可撤销的操作")
            return

        # 获取操作信息
        original_source = self.last_operation['source']
        target = self.last_operation['target']
        symbolic_link = self.last_operation['symbolic_link']

        # 确认操作
        if not messagebox.askyesno("确认撤销", 
            f"即将撤销：\n1. 删除符号链接: {symbolic_link}\n2. 恢复目录: {target} ➔ {original_source}\n是否继续？"):
            return

        # 删除符号链接
        if os.path.exists(symbolic_link) and os.path.islink(symbolic_link):
            os.unlink(symbolic_link)
        else:
            messagebox.showerror("错误", f"符号链接不存在或已被修改: {symbolic_link}")
            return

        # 恢复目录
        try:
            shutil.move(target, original_source)
        except Exception as e:
            messagebox.showerror("错误", f"恢复目录失败: {str(e)}")
            return

        self.last_operation = None
        messagebox.showinfo("成功", "撤销成功！")

def main():
    root = tk.Tk()
    DirectoryMoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
