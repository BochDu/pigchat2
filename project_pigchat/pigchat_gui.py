import sys
import os
import tkinter as tk
import ctypes

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from core import pigchat
from core import pigtime


try:
    # 任意唯一标识符
    myappid = 'yourcompany.yourproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except AttributeError:
    print("当前系统不支持 SetCurrentProcessExplicitAppUserModelID 方法。")
except Exception as e:
    print(f"设置 AppUserModelID 时出现错误: {e}")


def toggle_encrypt_decrypt():
    timestamp = pigtime.get_pig_timestamp()
    pigchat_class = pigchat.set_pigchat_class('fancy')
    input_text = entry.get("1.0", tk.END).strip()
    action_mode = pigchat.determine_encryption_decryption(input_text, pigchat_class)
    
    if action_mode == 'encrypt':
        output_text = pigchat.utf8_to_emoji(input_text, timestamp, password=password_var.get(), pigchat_class=pigchat_class)
    elif action_mode == 'decrypt':
        output_text = pigchat.emoji_to_utf8(input_text, timestamp, password=password_var.get(), pigchat_class=pigchat_class)
    else:
        output_text = input_text
    
    entry.delete("1.0", tk.END)
    entry.insert("1.0", output_text)


def adjust_password_entry_width():
    # 获取标题的宽度
    title_width = title_label.winfo_reqwidth()
    # 获取 Private Key 标签的宽度
    password_label_width = password_label.winfo_reqwidth()
    # 计算文本框需要的宽度
    entry_width = (title_width - password_label_width) // 10  # 除以 10 是因为 Entry 的宽度单位是字符
    if entry_width > 0:
        password_entry.config(width=entry_width)


# 创建主窗口并隐藏
root = tk.Tk()
root.withdraw()
root.title("PigChat")
# 设置窗口最小尺寸
root.minsize(500, 300)
root.configure(bg="#f0f0f0")

# 设置字体样式
font_style = ("Arial", 12)

# 创建一个新的框架来放置按钮和密码输入框
top_frame = tk.Frame(root, bg="#f0f0f0")
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# 加载野猪图片
try:
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序
        base_path = sys._MEIPASS
    else:
        # 如果是开发环境
        base_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_path, "wild_boar.png")
    img = tk.PhotoImage(file=img_path)
    img_width = img.width()
    img_height = img.height()
    # 根据图片大小调整窗口初始大小
    root.geometry(f"{max(500, img_width + 200)}x{max(300, img_height + 200)}")
except tk.TclError:
    print("未能找到或加载图片，请检查图片文件路径和格式。")
    img = None

# 加密/解密图片按钮
if img:
    button = tk.Button(top_frame, image=img, command=toggle_encrypt_decrypt, borderwidth=0, highlightthickness=0)
    button.image = img  # 避免图片被垃圾回收机制清除
    button.pack(side=tk.LEFT, padx=50)

# 密码输入框框架
password_frame = tk.Frame(top_frame, bg="#f0f0f0")
password_frame.pack(side=tk.RIGHT, padx=0)

# 添加标题标签
title_label = tk.Label(password_frame, text="start a new encrypted chat", font=("Arial", 14, "bold"), bg="#f0f0f0", wraplength=password_frame.winfo_width())
title_label.pack(side=tk.TOP, pady=5, fill=tk.X)

password_label = tk.Label(password_frame, text="Private Key :", font=font_style, bg="#f0f0f0")
password_label.pack(side=tk.LEFT)

password_var = tk.StringVar()
password_entry = tk.Entry(password_frame, show="", textvariable=password_var, width=20, font=font_style, bd=1, relief=tk.SOLID)
password_entry.pack(side=tk.RIGHT, padx=10, pady=0)

# 文本输入框
entry = tk.Text(root, width=50, height=15, wrap=tk.WORD, font=font_style, bd=1, relief=tk.SOLID)
entry.pack(pady=10, padx=20, expand=True, fill='both')

# 定义一个函数，在窗口大小改变时更新标题的换行长度
def on_window_resize(event):
    title_label.config(wraplength=password_frame.winfo_width())


# 绑定窗口大小改变事件
root.bind("<Configure>", on_window_resize)

# 动态调整密码输入框宽度
adjust_password_entry_width()

# 强制 Tkinter 完成布局计算
root.update_idletasks()

# 设置窗口图标
try:
    icon_path = os.path.join(base_path, "wild_boar.ico")
    root.iconbitmap(icon_path)
except tk.TclError:
    print("未能找到或加载图标，请检查图标文件路径和格式。图标文件应为 .ico 格式。")

# 显示窗口
root.deiconify()

root.mainloop()