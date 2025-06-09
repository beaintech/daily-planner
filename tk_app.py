
import tkinter as tk
from tkinter import messagebox, ttk
import requests

# 创建主窗口
root = tk.Tk()
root.title("Daily Task Planner")
root.geometry("600x600")

tasks = []

def add_task():
    task_frame = tk.Frame(task_container, pady=5)
    task_frame.pack(fill="x", pady=3)

    task_name_var = tk.StringVar()
    time_mode_var = tk.StringVar(value='2')
    hours_var = tk.StringVar()
    minutes_var = tk.StringVar()
    start_var = tk.StringVar()
    end_var = tk.StringVar()

    def update_fields(*args):
        if time_mode_var.get() == '1':
            hour_entry.config(state='disabled')
            minute_entry.config(state='disabled')
            start_entry.config(state='normal')
            end_entry.config(state='normal')
        else:
            hour_entry.config(state='normal')
            minute_entry.config(state='normal')
            start_entry.config(state='disabled')
            end_entry.config(state='disabled')

    # 行：任务名
    tk.Label(task_frame, text="Task Name:").grid(row=0, column=0, sticky='e')
    tk.Entry(task_frame, textvariable=task_name_var, width=20).grid(row=0, column=1)

    # 行：时间模式
    tk.Label(task_frame, text="Time Mode:").grid(row=1, column=0, sticky='e')
    mode_menu = ttk.Combobox(task_frame, textvariable=time_mode_var, values=["2", "1"], width=17)
    mode_menu.grid(row=1, column=1)
    time_mode_var.trace_add("write", update_fields)

    # 行：小时/分钟 or 起止时间
    hour_entry = tk.Entry(task_frame, textvariable=hours_var, width=10)
    minute_entry = tk.Entry(task_frame, textvariable=minutes_var, width=10)
    start_entry = tk.Entry(task_frame, textvariable=start_var, width=10)
    end_entry = tk.Entry(task_frame, textvariable=end_var, width=10)

    tk.Label(task_frame, text="Hours:").grid(row=2, column=0, sticky='e')
    hour_entry.grid(row=2, column=1, sticky='w')

    tk.Label(task_frame, text="Minutes:").grid(row=3, column=0, sticky='e')
    minute_entry.grid(row=3, column=1, sticky='w')

    tk.Label(task_frame, text="Start (HH:MM):").grid(row=4, column=0, sticky='e')
    start_entry.grid(row=4, column=1, sticky='w')

    tk.Label(task_frame, text="End (HH:MM):").grid(row=5, column=0, sticky='e')
    end_entry.grid(row=5, column=1, sticky='w')

    # 行：移除按钮
    def remove_task():
        task_frame.destroy()
        tasks.remove(data)

    tk.Button(task_frame, text="Remove Task", command=remove_task, fg="red").grid(row=0, column=2, rowspan=2, padx=10)

    data = {
        "task_name_var": task_name_var,
        "time_mode_var": time_mode_var,
        "hours_var": hours_var,
        "minutes_var": minutes_var,
        "start_var": start_var,
        "end_var": end_var,
        "frame": task_frame
    }

    tasks.append(data)
    update_fields()

def submit_tasks():
    payload = []

    for t in tasks:
        mode = t["time_mode_var"].get()
        task = {
            "task_name": t["task_name_var"].get(),
            "time_mode": mode
        }

        if mode == '1':
            task["start"] = t["start_var"].get()
            task["end"] = t["end_var"].get()
        else:
            try:
                task["hours"] = float(t["hours_var"].get() or 0)
                task["minutes"] = float(t["minutes_var"].get() or 0)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for hours and minutes.")
                return

        payload.append(task)

    try:
        response = requests.post("http://127.0.0.1:8000/process-tasks", json=payload)
        response.raise_for_status()
        result = response.json()

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Total Hours: {result['total_hours']}\n\n")
        for task in result["tasks"]:
            result_text.insert(tk.END, f"{task['task_name']}: {task['duration_hours']} hours\n")
    except Exception as e:
        messagebox.showerror("Network Error", f"Error sending data: {e}")

# 布局
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="Add Task", command=add_task, bg="lightblue").pack(side="left", padx=5)
tk.Button(top_frame, text="Submit", command=submit_tasks, bg="lightgreen").pack(side="left", padx=5)

task_container = tk.Frame(root)
task_container.pack(fill="both", expand=True)

result_text = tk.Text(root, height=10, wrap="word")
result_text.pack(padx=10, pady=10, fill="both", expand=True)

# 初始任务
add_task()

# 运行主循环
root.mainloop()

        # response = requests.post(
        #     # "https://daily-planner-1.onrender.com/process-tasks",
        #     "http://127.0.0.1:8000/process-tasks",
        #     headers={"Content-Type": "application/json"},
        #     data=json.dumps([task])
        # )

