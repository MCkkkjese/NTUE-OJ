import tkinter as tk
from tkinter import INSERT, messagebox
from Extension_modules import file_directory as fd
from Extension_modules import resolution_checking_process as rcp
import os
import subprocess
import time
import sys
import ttkbootstrap as ttk
from PIL import Image, ImageTk

# ---------- 常數 ----------
VERSION = "1.0.0"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# ---------- 全域變數 ----------
g_default_screensize = "1920x1080"
date_today = time.strftime("%Y_%m_%d", time.localtime())
g_path_commit_history = fd.path_function(f"/Source_code/Commit_History_{date_today}.dat")

with open(g_path_commit_history, 'w', encoding="utf-8") as f:
    f.write(f"Commit History - {date_today}\n")

# ---------- 主視窗 ----------
g_win = ttk.Window(themename="flatly")
g_win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
g_win.title(f"國立臺北教育大學 eTutor - Version {VERSION}")
ico_path = fd.path_function("Extension_modules/NTUE_LOGO.ico")
g_win.iconbitmap(ico_path)
g_win.withdraw()   # 暫時隱藏視窗
g_username = tk.StringVar(value="請輸入學號")
g_time_now = tk.StringVar()

# ---------- 解析度與縮放檢查 ----------
if rcp.resolution() != (1920, 1080):
    messagebox.showwarning("解析度警告", "解析度非 1920 x 1080 ，內容顯示或將異常")
if rcp.magnification() != 1.0:
    messagebox.showwarning("縮放比例警告", "縮放比例非 100% ，內容顯示或將異常")

# ---------- 啟動畫面 ----------
def show_bootup():
    g_boot_win = tk.Toplevel()
    screen_w = g_win.winfo_screenwidth()
    screen_h = g_win.winfo_screenheight()
    x_pos = int(screen_w/6)
    y_pos = int(screen_h/6)
    g_boot_win.geometry(f"1920x1080+{x_pos}+{y_pos}")
    g_boot_win.overrideredirect(True)
    g_boot_win.title("國北教 eTutor 啟動畫面")

    pic_bg_path = fd.path_function("Extension_modules/open_picture.png")
    pic_bg = Image.open(pic_bg_path)
    # 保留參考，避免圖片消失
    g_boot_win.bg_img = ImageTk.PhotoImage(pic_bg)

    tk.Label(g_boot_win, image=g_boot_win.bg_img).place(x=-2, y=-2)
    tk.Label(g_boot_win, text=f"Version {VERSION}", font=("微軟正黑體", 10)).place(x=1, y=1040)

    def close_bootup():
        g_boot_win.destroy()
        g_win.deiconify()

    g_boot_win.after(1000, close_bootup)

show_bootup()

# ---------- 時間更新 ----------
def update_time():
    g_time_now.set("Time : " + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
    g_win.after(1000, update_time)

update_time()

# ---------- 工具函式 ----------
def clear_status():
    g_show_answer.config(state="normal")
    g_show_answer.delete('1.0', 'end')
    g_show_answer.config(state="disabled")

def insert_status(text):
    clear_status()
    g_show_answer.config(state="normal")
    g_show_answer.insert(INSERT, text)
    g_show_answer.config(state="disabled")

def create_python_file():
    return fd.path_function("/Extension_modules/Judge_Program/temp_code.py")

def safe_kill_process(process):
    if process and process.poll() is None:
        process.kill()

# ---------- 判題函式 ----------
def judge_python(question_num, py_path, user):
    value_expected = []
    value_user = []
    run_time = 0

    lang = g_language_combobox.get().lower()
    td_path = fd.path_function(f"Question_Database/{lang}/TD_def_{question_num}.dat")
    code_ans_path = fd.path_function(f"Question_Database/{lang}_Ans/TD_def_{question_num}.py")

    with open(td_path, 'r', encoding="utf-8") as f:
        test_data = [line.strip() for line in f if line.strip()]

    # 執行使用者程式
    for data in test_data:
        start_time = time.time()
        try:
            proc = subprocess.Popen(
                [sys.executable, py_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                universal_newlines=True
            )
            value, err = proc.communicate(data, timeout=1)
            run_time += time.time() - start_time
            if err:
                value_user.append(f"Error: {err.strip()}")
            else:
                value_user.append(value.strip())
        except subprocess.TimeoutExpired:
            safe_kill_process(proc)
            value_user.append("Timeout")
        finally:
            safe_kill_process(proc)

    # 執行正確答案程式
    for data in test_data:
        proc = subprocess.Popen(
            [sys.executable, code_ans_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="ignore",
            universal_newlines=True
        )
        value, _ = proc.communicate(data)
        value_expected.append(value.strip())
        safe_kill_process(proc)

    time_judge = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime())

    if value_user == value_expected:
        insert_status(f"{time_judge} - Accepted\nExecution time = {run_time:.5f} s\n\n")
        with open(g_path_commit_history, 'a', encoding="utf-8") as f:
            f.write(f"{time_judge} - User: {user}, {question_num} AC\nExecution time = {run_time:.5f} s\n\n")
    elif "Timeout" in value_user:
        insert_status(f"{time_judge} - Time Limit Exceeded\n\n")
        messagebox.showerror("TLE", "Time Limit Exceeded")
        with open(g_path_commit_history, 'a', encoding="utf-8") as f:
            f.write(f"{time_judge} - User: {user}, {question_num} TLE\n\n")
    else:
        insert_status(f"{time_judge} - Wrong Answer\n\n")
        messagebox.showerror("WA", "Wrong Answer")
        with open(g_path_commit_history, 'a', encoding="utf-8") as f:
            f.write(f"{time_judge} - User: {user}, {question_num} WA\n\n")

# ---------- 提交程式 ----------
def submit_code():
    code_text = g_input_code.get('1.0', 'end')
    user = g_username.get()
    question_num = g_question_combobox.get().strip()
    lang = g_language_combobox.get().lower() 

    def submit_code():
        code_text = g_input_code.get('1.0', 'end')
        user = g_username.get()
        question_num = g_question_combobox.get().strip()
        lang = g_language_combobox.get().lower()  # 新增：取得語言

    if user in ["請輸入學號", ""]:
        messagebox.showerror("使用者未知", "請輸入學生證號碼")
        return
    if not question_num:
        messagebox.showerror("題號錯誤", "請先選擇題號")
        return

    if lang == "python":
        # 直接寫檔，不需要 C++ 編譯
        py_path = create_python_file()
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(code_text)
        judge_python(question_num, py_path, user)

    elif lang == "c++":
        # 原本的 C++ 流程
        ccf.write_temp_code(code_text)
        compile_success = ccf.write_source_code(code_text, user)
        if compile_success:
            cpp_path = ccf.get_executable_path(user)  # 取得編譯後可執行檔
            # judge_cpp(question_num, cpp_path, user)
        else:
            insert_status(f"{time.strftime('%Y/%m/%d %H:%M:%S')} - Compile Error\n\n")
            messagebox.showerror("CE", "Compile Error")


# ---------- 顯示 Commit History ----------
def show_commit_history():
    clear_status()
    g_show_answer.config(state="normal")
    g_show_answer.insert(INSERT, "Opening Commit History\n\n")
    with open(g_path_commit_history, 'r', encoding="utf-8") as f:
        g_show_answer.insert(INSERT, f.read())
    g_show_answer.config(state="disabled")

# ---------- 題目選擇 Combobox ----------
def language_selected():
    selected_lang = g_language_combobox.get()
    g_question_combobox.set("")
    g_question_combobox.config(values=[])

    folder_map = {"Python": "python", "C++": "cpp"}
    folder = folder_map.get(selected_lang)
    if not folder:
        insert_status(f"Selected language: {selected_lang} (unsupported)\n\n")
        return

    insert_status(f"Selected language: {selected_lang}\n\n")
    path_question_num = fd.path_function(f"Question_Database/{folder}/Question_Number.dat")
    try:
        with open(path_question_num, 'r', encoding="utf-8") as f:
            options = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messagebox.showwarning("找不到題號清單", f"無法找到：{path_question_num}")
        options = []

    g_question_combobox.config(values=options)

def question_selected():
    selected_qn = g_question_combobox.get().strip()
    selected_lang = g_language_combobox.get()
    folder_map = {"Python": "python", "C++": "cpp"}
    folder = folder_map.get(selected_lang)
    if not folder:
        insert_status(f"Selected question: {selected_qn} (語言未知)\n\n")
        return

    insert_status(f"Selected question: {selected_qn}\n\n")
    question_text_path = fd.path_function(f"Question_Database/{folder}/Q{selected_qn}.txt")
    try:
        with open(question_text_path, "r", encoding="utf-8") as f:
            content = f.read()
        g_show_question.config(state="normal")
        g_show_question.delete("1.0", "end")
        g_show_question.insert("end", content)
        g_show_question.config(state="disabled")
    except FileNotFoundError:
        messagebox.showwarning("題目不存在", f"找不到題目檔案：{question_text_path}")
    except Exception as e:
        messagebox.showerror("顯示題目失敗", f"讀取題目時發生錯誤：{e}")




# ---------- GUI 建立 ----------
class GUIInterface:
    def __init__(self):
        global g_show_question, g_input_code, g_show_answer
        global g_language_combobox, g_question_combobox

        # 背景圖片
        pic_bg_path = fd.path_function("Extension_modules/background.png")
        pic_bg = Image.open(pic_bg_path)
        self.bg_img = ImageTk.PhotoImage(pic_bg)
        tk.Label(g_win, image=self.bg_img).place(x=-2, y=-2)

        # 時間與版本
        tk.Label(g_win, textvariable=g_time_now, font=("微軟正黑體", 18)).place(x=1270, y=20)
        ttk.Label(g_win, text=f"Version {VERSION}", font=("微軟正黑體", 10)).place(x=20, y=1040)



        # 語言選擇
        g_language_combobox = ttk.Combobox(
            g_win, 
            font=("微軟正黑體", 16), 
             values=["Python", "C++(正在開發中)"], 
            state="readonly"
        )
        g_language_combobox.place(x=10, y=125, width=250)
        g_language_combobox.set("請選擇語言")  # 預設顯示提示文字
        g_language_combobox.bind("<<ComboboxSelected>>", lambda e: language_selected())

        # 題目選擇
        g_question_combobox = ttk.Combobox(
            g_win, 
            font=("微軟正黑體", 16), 
            values=[], 
            state="readonly"
        )
        g_question_combobox.place(x=280, y=125, width=250)
        g_question_combobox.set("請選擇題目")  # 預設顯示提示文字
        g_question_combobox.bind("<<ComboboxSelected>>", lambda e: question_selected())


        # 學號輸入 (帶 placeholder)
        global g_username  
        g_username_entry = ttk.Entry(
            g_win,
            font=("微軟正黑體", 17),
            textvariable=g_username
        )
        g_username_entry.place(x=550, y=125, width=270, height=68)

        # 預設顯示提示文字
        placeholder_text = "請輸入學號"
        if not g_username.get():
            g_username.set(placeholder_text)
        def on_focus_in(event):
            if g_username.get() == placeholder_text:
                g_username.set("")
        def on_focus_out(event):
            if g_username.get() == "":
                g_username.set(placeholder_text)

        g_username_entry.bind("<FocusIn>", on_focus_in)
        g_username_entry.bind("<FocusOut>", on_focus_out)


        # 預設顯示提示文字
        placeholder_text = "請輸入學號"
        g_username.set(placeholder_text)

        # 當 Entry 獲得焦點時清除 placeholder
        def on_focus_in(event):
            if g_username.get() == placeholder_text:
                g_username.set("")

        # 當 Entry 失去焦點時，如果空白就恢復 placeholder
        def on_focus_out(event):
            if g_username.get() == "":
                g_username.set(placeholder_text)

        g_username_entry.bind("<FocusIn>", on_focus_in)
        g_username_entry.bind("<FocusOut>", on_focus_out)


        # 顯示題目
        g_show_question = tk.Text(g_win, font=("微軟正黑體", 16))
        g_show_question.place(x=10, y=200, width=940, height=810)

        # 程式輸入區
        g_input_code = tk.Text(g_win, font=("微軟正黑體", 14))
        g_input_code.place(x=970, y=125, width=940, height=500)

        # 提交按鈕
        ttk.Button(g_win, text=" Submit ", style="Outline.TButton", command=submit_code)\
            .place(x=970, y=635, width=470, height=70)
        ttk.Button(g_win, text=" Commit History ", style="Outline.TButton", command=show_commit_history)\
            .place(x=1450, y=635, width=460, height=70)

        # 程式狀態顯示區
        g_show_answer = tk.Text(g_win, font=("微軟正黑體", 12))
        g_show_answer.place(x=970, y=716, width=940, height=295)
        g_show_answer.config(state="disabled")





# ---------- 啟動 GUI ----------
app = GUIInterface()
g_win.mainloop()
