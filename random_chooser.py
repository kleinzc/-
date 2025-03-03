import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os

class RandomChooser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("随机选择工具")
        self.geometry("800x800")  # 调整默认窗口大小
        self.configure(bg="#f0f0f0")
        self.resizable(True, True)
        self.minsize(600, 700)  # 调整最小窗口尺寸
        
        # 设置图标（如果有的话）
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        # 存储选项的列表
        self.options = []
        
        # 创建界面元素
        self.create_widgets()
        
        # 设置默认保存路径
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_options")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
    
    def create_widgets(self):
        # 标题标签
        title_frame = tk.Frame(self, bg="#f0f0f0")
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="随机选择工具", font=("微软雅黑", 18, "bold"), bg="#f0f0f0")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="告别选择困难症", font=("微软雅黑", 10), bg="#f0f0f0", fg="#666666")
        subtitle_label.pack()
        
        # 添加选项区域
        input_frame = tk.Frame(self, bg="#f0f0f0")
        input_frame.pack(pady=10, fill="x", padx=20)
        
        self.option_entry = tk.Entry(input_frame, font=("微软雅黑", 13), width=40)  # 调整输入框
        self.option_entry.pack(side="left", padx=10)
        self.option_entry.bind("<Return>", lambda event: self.add_option())
        
        add_button = tk.Button(input_frame, text="添加选项", font=("微软雅黑", 11), 
                              command=self.add_option, bg="#4CAF50", fg="white", 
                              activebackground="#45a049", activeforeground="white",
                              width=10, height=1)  # 调整按钮尺寸
        add_button.pack(side="left", padx=5)
        
        # 选项列表区域
        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(pady=15, fill="both", expand=True, padx=30)  # 调整内边距
        
        list_label = tk.Label(list_frame, text="当前选项列表", font=("微软雅黑", 12, "bold"), bg="#f0f0f0", fg="#333333")
        list_label.pack(anchor="w", pady=(0, 10))
        
        list_container = tk.Frame(list_frame, bg="white", bd=0)
        list_container.pack(fill="both", expand=True)
        
        # 创建画布和滚动条
        canvas = tk.Canvas(list_container, bg="white", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        
        # 创建选项容器框架
        self.options_frame = tk.Frame(canvas, bg="white")
        self.options_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # 在画布上创建窗口
        canvas.create_window((0, 0), window=self.options_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局画布和滚动条
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定画布大小变化事件
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))
        
        self.options_listbox = tk.Listbox(list_container, font=("微软雅黑", 12), 
                                        selectbackground="#a6d4fa", 
                                        selectmode=tk.SINGLE, 
                                        yscrollcommand=scrollbar.set)
        self.options_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.options_listbox.yview)
        
        # 操作按钮区域
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack(pady=10, fill="x", padx=20)
        
        delete_button = tk.Button(buttons_frame, text="删除选项", font=("微软雅黑", 10), 
                                command=self.delete_option, bg="#f44336", fg="white", 
                                activebackground="#d32f2f", activeforeground="white")
        delete_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(buttons_frame, text="清空所有", font=("微软雅黑", 10), 
                               command=self.clear_options, bg="#ff9800", fg="white", 
                               activebackground="#fb8c00", activeforeground="white")
        clear_button.pack(side="left", padx=5)
        
        save_button = tk.Button(buttons_frame, text="保存选项", font=("微软雅黑", 10), 
                              command=self.save_options, bg="#2196F3", fg="white", 
                              activebackground="#1976d2", activeforeground="white")
        save_button.pack(side="left", padx=5)
        
        load_button = tk.Button(buttons_frame, text="加载选项", font=("微软雅黑", 10), 
                              command=self.load_options, bg="#9c27b0", fg="white", 
                              activebackground="#7b1fa2", activeforeground="white")
        load_button.pack(side="left", padx=5)
        
        # 随机选择区域
        choose_frame = tk.Frame(self, bg="#f0f0f0")
        choose_frame.pack(pady=20, padx=20)
        
        choose_button = tk.Button(choose_frame, text="随机选择", font=("微软雅黑", 15, "bold"), 
                                command=self.choose_random, bg="#3f51b5", fg="white", 
                                activebackground="#303f9f", activeforeground="white",
                                height=2, width=20)  # 调整随机选择按钮尺寸
        choose_button.pack()
        
        # 结果显示区域
        result_frame = tk.Frame(self, bg="#f0f0f0")
        result_frame.pack(pady=10, padx=20, fill="x")
        
        result_label = tk.Label(result_frame, text="结果", font=("微软雅黑", 12), bg="#f0f0f0")
        result_label.pack()
        
        self.result_var = tk.StringVar()
        self.result_var.set("等待选择...")
        
        self.result_display = tk.Label(result_frame, textvariable=self.result_var, 
                                     font=("微软雅黑", 18, "bold"), bg="#e0e0e0", 
                                     fg="#333333", width=35, height=2, relief="ridge")  # 调整结果显示区域
        self.result_display.pack(pady=10)
        
        # 状态栏
        status_frame = tk.Frame(self, bg="#e0e0e0", height=25)
        status_frame.pack(side="bottom", fill="x")
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 | 选项数量: 0")
        
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               font=("微软雅黑", 9), bg="#e0e0e0", anchor="w")
        status_label.pack(side="left", padx=10)
    
    def add_option(self):
        option = self.option_entry.get().strip()
        if option:
            self.options.append(option)
            
            # 创建选项卡片框架
            option_card = tk.Frame(self.options_frame, bg="white", padx=10, pady=5)
            option_card.pack(fill="x", padx=5, pady=3)
            
            # 添加选项文本
            option_label = tk.Label(option_card, text=option, font=("微软雅黑", 12),  # 调整字体大小
                                  bg="white", fg="#333333", anchor="w", padx=12, pady=10)
            option_label.pack(side="left", fill="x", expand=True)
            
            # 添加删除按钮
            delete_btn = tk.Button(option_card, text="×", font=("微软雅黑", 11),
                                 bg="white", fg="#666666", bd=0,
                                 activebackground="#ff4444", activeforeground="white")
            delete_btn.pack(side="right")
            
            # 设置卡片样式
            option_card.bind("<Enter>", lambda e, card=option_card: self._on_card_enter(card))
            option_card.bind("<Leave>", lambda e, card=option_card: self._on_card_leave(card))
            
            # 绑定删除按钮事件
            delete_btn.configure(command=lambda c=option_card, o=option: self._delete_option_card(c, o))
            
            self.option_entry.delete(0, tk.END)
            self.update_status()
        else:
            messagebox.showwarning("警告", "请输入有效的选项!")
    
    def _on_card_enter(self, card):
        card.configure(bg="#f5f5f5")
        for widget in card.winfo_children():
            widget.configure(bg="#f5f5f5")
    
    def _on_card_leave(self, card):
        card.configure(bg="white")
        for widget in card.winfo_children():
            widget.configure(bg="white")
    
    def _delete_option_card(self, card, option):
        card.destroy()
        self.options.remove(option)
        self.update_status()
    
    def delete_option(self):
        # 此方法不再使用，保留为空以防其他地方调用
        pass
    
    def clear_options(self):
        if messagebox.askyesno("确认", "确定要清空所有选项吗?"):
            # 清空选项列表
            self.options.clear()
            # 清空选项框架
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            # 清空列表框
            self.options_listbox.delete(0, tk.END)
            # 重置结果显示
            self.result_var.set("等待选择...")
            # 更新状态栏
            self.update_status()
    
    def choose_random(self):
        if not self.options:
            messagebox.showinfo("提示", "请先添加一些选项!")
            return
        
        # 添加选择动画效果
        self.choose_animation()
    
    def choose_animation(self, count=10):
        if count > 0:
            random_option = random.choice(self.options)
            self.result_var.set(random_option)
            delay = int(100 * (1 + (10-count)/5))  # 逐渐减慢动画速度
            self.after(delay, lambda: self.choose_animation(count-1))
        else:
            # 最终选择
            final_choice = random.choice(self.options)
            self.result_var.set(final_choice)
            self.status_var.set(f"已选择: {final_choice} | 选项数量: {len(self.options)}")
    
    def save_options(self):
        if not self.options:
            messagebox.showwarning("警告", "没有选项可保存!")
            return
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.save_path,
            title="保存选项列表",
            filetypes=[("JSON文件", "*.json")],
            defaultextension=".json"
        )
        
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"options": self.options}, f, ensure_ascii=False, indent=2)
            
            self.status_var.set(f"已保存 | 选项数量: {len(self.options)}")
    
    def load_options(self):
        filename = filedialog.askopenfilename(
            initialdir=self.save_path,
            title="加载选项列表",
            filetypes=[("JSON文件", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if "options" in data and isinstance(data["options"], list):
                    # 清空当前选项
                    self.options_listbox.delete(0, tk.END)
                    self.options.clear()
                    
                    # 加载新选项
                    for option in data["options"]:
                        self.options.append(option)
                        self.options_listbox.insert(tk.END, option)
                    
                    self.update_status()
                    messagebox.showinfo("成功", f"已加载 {len(self.options)} 个选项")
                else:
                    messagebox.showerror("错误", "文件格式不正确!")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件时出错: {str(e)}")
    
    def update_status(self):
        self.status_var.set(f"就绪 | 选项数量: {len(self.options)}")

if __name__ == "__main__":
    app = RandomChooser()
    app.mainloop()