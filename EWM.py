import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import tkinter.font as tkFont
from datetime import datetime
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


mean_entries = []
entry_air_entries = []
entry_gas_entries = []
entry_gas_names = []
final_indexes=[]
selected_file_path = ''

ROI_file_path=''

def show_custom_info_dialog(title, message, font):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.minsize(300, 200)
    label = ttk.Label(dialog, text=message, font=font)
    ok_button = ttk.Button(dialog, text="OK", command=dialog.destroy, style='Large.TButton')
    label.grid(row=0, column=0, pady=50, padx=10)
    ok_button.grid(row=1, column=0)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)



def display_dataframe_as_table(dataframe, title):
    root = tk.Tk()
    root.title(title)
    style = ttk.Style(root)
    style.configure("Treeview", font=("Arial", 14))
    style.configure("Treeview.Heading", font=("Arial", 14))
    tree = ttk.Treeview(root, style="Treeview")
    tree["columns"] = list(dataframe.columns)
    tree.heading("#0", text="Index")
    tree.column("#0", width=80)
    for column in dataframe.columns:
        tree.heading(column, text=column)
        tree.column(column, stretch=True, width=110)
    rounded_dataframe = dataframe.round(6)
    for index, row in rounded_dataframe.iterrows():
        if isinstance(index, (int, float)):
            index_label = index + 1
        else:
            index_label = index
        tree.insert("", "end", text=index_label, values=row.tolist())
    tree.pack(expand=True, fill="both")
    root.mainloop()

def display_ndm():
    display_dataframe_as_table(ndm, "Normalization")

def display_pr():
    display_dataframe_as_table(pr, "Probability")

def display_en():
    display_dataframe_as_table(en_df, "Entropy")

def display_div():
    display_dataframe_as_table(div_df, "Divergence")

def display_ew():
    display_dataframe_as_table(ew_df, "Weights")

def plot_graph():
    custom_font = tkFont.Font(family="Arial", size=14)
    global column_name
    if selected_file_path=='':
        show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
        return
    column_name_value = 'Time'
    start_time_value = start_time_entry.get()
    end_time_value = end_time_entry.get()
    if not column_name_value or not start_time_value or not end_time_value:
        show_custom_info_dialog("Error!", "Please fill in the field with the start and end timestamp.", custom_font)
        return
    else:
        try:
            column_name = column_name_value
            start_time = float(start_time_value)
            end_time = float(end_time_value)
        except ValueError:
            show_custom_info_dialog("Error!", "Please enter a numeric value for the timestamps.", custom_font)
            return
    column_name = 'Time'
    start_time = float(start_time_entry.get())
    end_time = float(end_time_entry.get())
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    selected_data = df.loc[(df[column_name] >= start_time) & (df[column_name] <= end_time)]
    columns_to_drop = ["Indexes","Humidity","Temperature"]
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    if columns_to_drop_existing:
        selected_data = selected_data.drop(columns=[column_name]+columns_to_drop_existing)
        max_values = selected_data.max()
        global ndm, pr, en_df, div_df, ew_df
        ndm = selected_data.div(max_values)
        ndm_sums = ndm.sum()
        pr = ndm.div(ndm_sums, axis=1)
        n = selected_data.shape[0]
        y=1.0/(np.log(n))
        pr_log = y*(-1.0)*np.log(pr) * pr
        pr_log_sums = pr_log.sum()
        en=pr_log_sums
        en_df = pd.DataFrame(en, columns=['Entropy'])
        div=np.abs(1-en)
        div_sums=div.sum()
        div_df = pd.DataFrame(div, columns=['Divergence'])
        ew=div.div(div_sums)*100
        ew_df = pd.DataFrame(ew, columns=['Weights'])
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
        selected_file = f"Entropy_method_{file_name}_{current_datetime}"
        ndm.to_csv(selected_file+"_Normalization.csv", sep=';', decimal='.')
        pr.to_csv(selected_file+"_Probability.csv", sep=';', decimal='.')
        en_df.to_csv(selected_file+"_Entropy.csv", sep=';', decimal='.')
        div_df.to_csv(selected_file+"_Divergence.csv", sep=';', decimal='.')
        ew_df.to_csv(selected_file+"_Weights.csv", sep=';', decimal='.')
        threads = []
        for display_func in [display_ndm, display_pr, display_en, display_div, display_ew]:
            thread = threading.Thread(target=display_func)
            threads.append(thread)
            thread.start()
        plt.figure('Entropy Weights Distribution',figsize=(10, 5))
        plt.bar(ew_df.index, ew_df['Weights'], color='blue')
        plt.xlabel('Indexes')
        plt.ylabel('Entropy Weights')
        plt.title('Entropy Weights Distribution')
        plt.grid(True)
        plt.show()
        for thread in threads:
            thread.join()
        recreate_main_menu()

def view_graph():
    global column_name
    custom_font = tkFont.Font(family="Arial", size=14)
    column_name = 'Time'
    if selected_file_path=='':
        show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
        return
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    plt.figure('All charts', figsize=(10, 5))
    for column in df.columns:
        if column=='Humidity':
            continue
        if column=='Temperature':
            continue
        if column != column_name:
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('R, Ohm')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('All charts')
    for column in df.columns:
        if column != column_name and column=='Humidity':
            plt.figure(f'{column}', figsize=(13, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('Humidity, g/m3')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        if column != column_name and column=='Temperature':
            plt.figure(f'{column}', figsize=(15, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('Temperature, °C')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        if column != column_name  and column!='Humidity' and column!='Temperature':
            plt.figure(f'{column}', figsize=(10, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('R, Ohm')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

def browse_file():
    global selected_file_path, file_name
    selected_file_path = filedialog.askopenfilename(title="Select a file")
    file_name = os.path.splitext(os.path.basename(selected_file_path))[0]
    path_label.config(text=selected_file_path)
    font = tkFont.Font(font=path_label['font'])
    text_width = font.measure(selected_file_path)
    root_width = text_width + 280
    root.geometry(f"{root_width}x200")
    root.minsize(500,200)

def recreate_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    view_main_menu()

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def view_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    global selected_file_path,mean_entries,entry_air_entries,entry_gas_entries,entry_gas_names,final_indexes, column_name,browse_button,path_label,start_time_label,start_time_entry,end_time_label,end_time_entry,plot_button,view_button,multiply_checkbox_var,every_second_var, every_third_var
    mean_entries = []
    entry_air_entries = []
    entry_gas_entries = []
    entry_gas_names = []
    final_indexes=[]
    selected_file_path = ''
    browse_button = ttk.Button(frame, text="Select a file", command=browse_file, style='Large.TButton')
    path_label = ttk.Label(frame, text="", font=("Arial", 14))
    start_time_label = ttk.Label(frame, text="Enter the initial timestamp:", font=("Arial", 14))
    start_time_entry = ttk.Entry(frame, width=20, font=("Arial", 14))
    end_time_label = ttk.Label(frame, text="Enter the end timestamp:", font=("Arial", 14))
    end_time_entry = ttk.Entry(frame, width=20, font=("Arial", 14))
    multiply_checkbox_var = tk.BooleanVar()
    every_second_var = tk.BooleanVar()
    every_third_var = tk.BooleanVar()
    plot_button = ttk.Button(frame, text="Calculate entropy weights", command=plot_graph, style='Large.TButton')
    view_button = ttk.Button(frame, text="View the chart", command=view_graph, style='Large.TButton')
    browse_button.grid(column=0, row=0, pady=10)
    path_label.grid(column=1, row=0, sticky=tk.W)
    start_time_label.grid(column=0, row=1, sticky=tk.W)
    start_time_entry.grid(column=1, row=1)
    end_time_label.grid(column=0, row=2, sticky=tk.W)
    end_time_entry.grid(column=1, row=2)
    plot_button.grid(column=0, row=6, pady=10)
    view_button.grid(column=1, row=6, pady=10)
    width = 500
    height = 200
    root.geometry(f"{width}x{height}")

root = tk.Tk()
style = ttk.Style()
style.configure('Large.TButton', font=('Arial', 14))
style.configure('TCheckbutton', font=('Arial', 14))
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", on_canvas_configure)
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
root.title("Calculate entropy weights")
frame = ttk.Frame(frame, padding="20")
frame.pack()
view_main_menu()
root.mainloop()