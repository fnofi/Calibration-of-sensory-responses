import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import tkinter.font as tkFont
from datetime import datetime

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
    dialog.minsize(200, 200)
    label = ttk.Label(dialog, text=message, font=font)
    ok_button = ttk.Button(dialog, text="OK", command=dialog.destroy, style='Large.TButton')
    label.grid(row=0, column=0, pady=50, padx=10)
    ok_button.grid(row=1, column=0)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

def show_choose_dialog(title, message, font):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.minsize(200, 200)
    label = ttk.Label(dialog, text=message, font=font)
    select_button = ttk.Button(dialog, text="Select a file", command=lambda: browse_ROI_file(dialog), style='Large.TButton')
    cancel_button = ttk.Button(dialog, text="Cancel", command=dialog.destroy, style='Large.TButton')
    label.grid(row=0, columnspan=2, pady=50, padx=10)
    select_button.grid(row=1, column=0)
    cancel_button.grid(row=1,column=1)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)

def browse_ROI_file():
    global ROI_file_path
    ROI_file_path = filedialog.askopenfilename(title="Select a file")
    plot_graph()

def plot_graph():
    custom_font = tkFont.Font(family="Arial", size=14)
    global column_name
    global every_second_var
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
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    selected_file = f"ROI_{file_name}_{current_datetime}"
    global ROI_file_path
    if every_second_var.get():
        if ROI_file_path!='':
            selected_file = ROI_file_path
            selected_data.iloc[::2].to_csv(selected_file, mode='a', index=False, sep=';', decimal='.', header=False)
        else:
            selected_file+="_through_a_single_value.csv"
            selected_data.iloc[::2].to_csv(selected_file, index=False, sep=';', decimal='.')
    elif every_third_var.get():
        if ROI_file_path!='':
            selected_file = ROI_file_path
            selected_data.iloc[::3].to_csv(selected_file, mode='a', index=False, sep=';', decimal='.', header=False)
        else:
            selected_file+="_through_two_values.csv"
            selected_data.iloc[::3].to_csv(selected_file, index=False, sep=';', decimal='.')
    else:
        if ROI_file_path!='':
            selected_file = ROI_file_path
            selected_data.to_csv(selected_file, mode='a', index=False, sep=';', decimal='.', header=False)
        else:
            selected_file += '.csv'
            selected_data.to_csv(selected_file, index=False, sep=';', decimal='.')
    ROI_file_path=''
    show_custom_info_dialog("Successfully!", f"The region of interest has been successfully saved in {selected_file}", custom_font)
    every_second_var.set(0)
    every_third_var.set(0)

def view_graph():
    global column_name
    custom_font = tkFont.Font(family="Arial", size=14)
    column_name = 'Time'
    if selected_file_path=='':
        show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
        return
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    # df.to_csv('NH3.csv', index=False, sep=';', decimal='.')
    plt.figure('All charts', figsize=(10, 5))
    for column in df.columns:
        if column=='Humidity':
            continue
        if column=='Temperature':
            continue
        if column=='Indexes':
            continue
        if column != column_name:
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('R, Ohm')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('All charts')
    for column in df.columns:
        if column != column_name and column=='Humidity':
            plt.figure(f'{column}', figsize=(10, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('Humidity, g/m3')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()
        if column != column_name and column=='Temperature':
            plt.figure(f'{column}', figsize=(10, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('Temperature, °C')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()
        if column != column_name  and column!='Humidity' and column!='Temperature':
            plt.figure(f'{column}', figsize=(10, 5))
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Time, sec')
            plt.ylabel('R, Ohm')
            plt.title(f'{column}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()
    plt.show()

def get_user_values(mean_entries):
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    user_values = []
    divide_r_rair = pd.DataFrame()
    log_r_rair = pd.DataFrame()
    r_rair_rair = pd.DataFrame()
    abs_r_rair_rair = pd.DataFrame()
    time_column = df[column_name]
    if 'Indexes' in df.columns:
        indexes_column = df['Indexes']
    columns_to_drop = ["Indexes","Humidity","Temperature"]
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    if columns_to_drop_existing:
        df = df.drop(columns=[column_name]+columns_to_drop_existing)
        for entry in mean_entries:
            value = float(entry.get())
            user_values.append(value)
        for idx, (col, values) in enumerate(df.items()):
            new_col_values = values.astype(float) / user_values[idx]
            divide_r_rair[col] = new_col_values
            log_r_rair[col]=np.log10(new_col_values)
            new_value = (values.astype(float) - user_values[idx])/user_values[idx]
            r_rair_rair[col]=new_value
            abs_r_rair_rair[col]=np.abs(new_value)
        divide_r_rair[column_name] = time_column
        log_r_rair[column_name] = time_column
        r_rair_rair[column_name] = time_column
        abs_r_rair_rair[column_name] = time_column
        if 'Indexes' in df.columns:
            divide_r_rair['Indexes'] = indexes_column
            log_r_rair['Indexes'] = indexes_column
            r_rair_rair['Indexes'] = indexes_column
            abs_r_rair_rair['Indexes'] = indexes_column
        divide_r_rair.to_csv('divide_R_Rair.csv', index=False, sep=';')
        log_r_rair.to_csv('log_R_Rair.csv', index=False, sep=';')
        r_rair_rair.to_csv('r_rair_rair.csv', index=False, sep=';')
        abs_r_rair_rair.to_csv('abs_r_rair_rair.csv', index=False, sep=';')
        custom_font = tkFont.Font(family="Arial", size=14)
        show_custom_info_dialog("Successfully!", "The dataset has been successfully saved in С„Р°Р№Р»С‹: divide_R_Rair.csv; log_R_Rair.csv; r_rair_rair.csv; abs_r_rair_rair.csv.", custom_font)
        recreate_main_menu()

def enter_index():
    for widget in frame.winfo_children():
        widget.destroy()
    global gas_input, air_input, air_label, gas_label, continue_button
    info_label = ttk.Label(frame, text="Specify how many times the experiment is served:", font=("Arial", 14))
    air_label = ttk.Label(frame, text="Air:", font=("Arial", 14))
    gas_label = ttk.Label(frame, text="Verification gas mixture:", font=("Arial", 14))
    gas_input = ttk.Entry(frame, font=("Arial", 14), width=10)
    air_input = ttk.Entry(frame, font=("Arial", 14), width=10)
    continue_button = ttk.Button(frame, text="Continue", command=enter_air_gas, style='Large.TButton')
    info_label.grid(row=0, columnspan=2)
    air_label.grid(row=1, column=0)
    air_input.grid(row=1, column=1)
    gas_label.grid(row=2, column=0)
    gas_input.grid(row=2, column=1)
    continue_button.grid(row=3, columnspan=2, pady=10)
    main_menu_button = ttk.Button(frame, text="Main menu", command=recreate_main_menu, style='Large.TButton')
    main_menu_button.grid(column=3, row=3, pady=10, padx=30)
    font = tkFont.Font(font=main_menu_button['style'])
    text_width = font.measure(main_menu_button)
    root_width = text_width + 300
    root.geometry(f"{root_width}x160")

def enter_air_gas():
    custom_font = tkFont.Font(family="Arial", size=14)
    air_value = air_input.get()
    gas_value = gas_input.get()
    if not air_value or not gas_value:
        show_custom_info_dialog("Error!", "Please fill in all the fields.", custom_font)
        return
    air_count = int(air_input.get())
    gas_count = int(gas_input.get())
    for widget in frame.winfo_children():
        widget.destroy()
    multiply_checkbox_var.set(0)
    info_label = ttk.Label(frame, text="Specify the timestamps:", font=("Arial", 14))
    info_label.grid(row=0, columnspan=4, pady=10)
    for i in range(air_count + gas_count):
        if i % 2 == 0:
            air_index = i // 2 + 1
            air_entry_label = ttk.Label(frame, text=f'Timestamps for air {air_index}', font=("Arial", 14))
            air_entry_label.grid(row=i+1, column=0)
            entry_air = ttk.Entry(frame, font=("Arial", 14), width=10)
            entry_air.grid(row=i+1, column=1)
            entry_air_entries.append(entry_air)
        else:
            gas_index = (i + 1) // 2
            gas_name_label = ttk.Label(frame, text=f'Enter the name and concentration of the gas {gas_index}', font=("Arial", 14))
            gas_name_label.grid(row=i+1, column=0)
            entry_gas_name = ttk.Entry(frame, font=("Arial", 14), width=20)
            entry_gas_name.grid(row=i+1, column=1)
            gas_entry_label = ttk.Label(frame, text=f'Timestamps for gas {gas_index}', font=("Arial", 14))
            gas_entry_label.grid(row=i+1, column=2)
            entry_gas = ttk.Entry(frame, font=("Arial", 14), width=10)
            entry_gas.grid(row=i+1, column=3)
            entry_gas_names.append(entry_gas_name)
            entry_gas_entries.append(entry_gas)
    add_air_gas_button = ttk.Button(frame, text="Continue", command=lambda: add_air_gas(air_count, gas_count), style='Large.TButton')
    add_air_gas_button.grid(row=air_count+gas_count+2, columnspan=2, pady=10)
    main_menu_button = ttk.Button(frame, text="Main menu", command=recreate_main_menu, style='Large.TButton')
    main_menu_button.grid(column=2, row=air_count+gas_count+2, pady=10, padx=30)
    width = 1050
    height = 320
    root.geometry(f"{width}x{height}")
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_air_gas(air_count, gas_count):
    custom_font = tkFont.Font(family="Arial", size=14)
    for i in range(air_count):
        entry_air = entry_air_entries[i].get()
        if not entry_air:
            show_custom_info_dialog("Error!", f"Please fill the field for 'Air {i+1}'.", custom_font)
            return
    for i in range(gas_count):
        entry_gas_name = entry_gas_names[i].get()
        entry_gas = entry_gas_entries[i].get()
        if not entry_gas_name or not entry_gas:
            show_custom_info_dialog("Error!", f"Please fill the field for 'Gas {i+1}'.", custom_font)
            return
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    air_entries = [int(entry_air_entries[i].get()) for i in range(air_count)]
    gas_names = [entry_gas_names[i].get() for i in range(gas_count)]
    gas_entries = [int(entry_gas_entries[i].get()) for i in range(gas_count)]
    total_labels = int(entry_air_entries[-1].get())
    final_indexes = []
    air_step=0
    for i, j in zip(range(0, air_count, 1), range(gas_count)):
        air_label_count = int(air_entries[i] - air_step)
        final_indexes.extend(['Air'] * air_label_count)
        gas_label_count = int(gas_entries[j] - air_entries[i])
        final_indexes.extend([gas_names[j]] * gas_label_count)
        air_step=int(gas_entries[j])
    if air_count>gas_count:
        air_label_count = int(air_entries[-1] - int(gas_entries[-1]))
        final_indexes.extend(['Air'] * air_label_count)
    df['Indexes']=''
    df['Indexes'].iloc[:len(final_indexes)]=final_indexes[:len(final_indexes)]
    df['Indexes'] = df['Indexes'].fillna('')
    df.to_csv('indexes.csv', index=False, sep=';', decimal='.')
    recreate_main_menu()
    show_custom_info_dialog("Successfully!", f"The dataset has been successfully saved in indexes.csv.", custom_font)


# def select_mean():
#     custom_font = tkFont.Font(family="Arial", size=14)
#     if mean_checkbox_var.get():
#         multiply_checkbox_var.set(0)
#         global column_name
#         column_name = column_name_entry.get()      
#         if selected_file_path=='':
#             show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
#             mean_checkbox_var.set(0)
#             return  
#         if not column_name:
#             show_custom_info_dialog("Error!", "РџРѕР¶Р°Р»СѓР№СЃС‚Р° Р·Р°РїРѕР»РЅРёС‚Рµ РїРѕР»Рµ СЃ РЅР°Р·РІР°РЅРёРµРј РїР°СЂР°РјРµС‚СЂР°.", custom_font)
#             mean_checkbox_var.set(0)
#             return
#         for widget in frame.winfo_children():
#             widget.destroy()
#         df = pd.read_csv(selected_file_path, sep=';', decimal='.')
#         if column_name not in df.columns:
#             show_custom_info_dialog("Error!", f"РЎС‚РѕР»Р±РµС† {column_name} РЅРµ РЅР°С…РѕРґРёС‚СЃСЏ РІ С„Р°Р№Р»Рµ.", custom_font)
#             return
#         columns_to_drop = ["Indexes","Humidity","Temperature"]
#         columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
#         if columns_to_drop_existing:
#             df = df.drop(columns=[column_name]+columns_to_drop_existing)
#             i=0
#             for idx, col in enumerate(df.columns):
#                 entry_label = ttk.Label(frame, text=f"Р’РІРµРґРёС‚Рµ R РІРѕР·РґСѓС…Р° РґР»СЏ {col}", font=("Arial", 14))
#                 entry_label.grid(row=idx+1, column=1, pady=10)
#                 entry = ttk.Entry(frame, font=("Arial", 14))
#                 entry.grid(row=idx+1, column=2, pady=10)
#                 mean_entries.append(entry)
#                 i=idx
#                 def continue_button_click():
#                     entry_values = [entry.get() for entry in mean_entries]
#                     if not all(entry_values):
#                         show_custom_info_dialog("Error!", "Please fill in all the fields.", custom_font)
#                     else:
#                         get_user_values(mean_entries)
#             continue_mean_button = ttk.Button(frame, text="Continue", command=continue_button_click, style='Large.TButton')
#             continue_mean_button.grid(row=i+2, column=2, pady=10)
#             main_menu_button = ttk.Button(frame, text="Main menu", command=recreate_main_menu, style='Large.TButton')
#             main_menu_button.grid(column=3, row=i+2, pady=10, padx=30)
#             canvas.update_idletasks()
#             canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def select_multiply():
    custom_font = tkFont.Font(family="Arial", size=14)
    if multiply_checkbox_var.get():
        # mean_checkbox_var.set(0)
        global column_name
        column_name = 'Time' 
        if selected_file_path=='':
            show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
            multiply_checkbox_var.set(0)
            return
        enter_index()

def browse_file():
    global selected_file_path, file_name
    selected_file_path = filedialog.askopenfilename(title="Select a file")
    file_name = os.path.splitext(os.path.basename(selected_file_path))[0]
    path_label.config(text=selected_file_path)
    font = tkFont.Font(font=path_label['font'])
    text_width = font.measure(selected_file_path)
    root_width = text_width + 480
    root.geometry(f"{root_width}x320")
    root.minsize(620,160)

def recreate_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    view_main_menu()

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def view_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    global save_existing_button,selected_file_path,mean_entries,entry_air_entries,entry_gas_entries,entry_gas_names,final_indexes, column_name,browse_button,path_label,start_time_label,start_time_entry,end_time_label,end_time_entry,mean_checkbox,multiply_checkbox,every_second_checkbox,every_third_checkbox,plot_button,view_button,mean_checkbox_var,multiply_checkbox_var,every_second_var, every_third_var, air_label, gas_label, gas_input, air_input,continue_button
    mean_entries = []
    entry_air_entries = []
    entry_gas_entries = []
    entry_gas_names = []
    final_indexes=[]
    selected_file_path = ''
    browse_button = ttk.Button(frame, text="Select a file", command=browse_file, style='Large.TButton')
    path_label = ttk.Label(frame, text="", font=("Arial", 14))
    start_time_label = ttk.Label(frame, text="Enter the initial timestamp:", font=("Arial", 14))
    start_time_entry = ttk.Entry(frame, width=10, font=("Arial", 14))
    end_time_label = ttk.Label(frame, text="Enter the end timestamp:", font=("Arial", 14))
    end_time_entry = ttk.Entry(frame, width=10, font=("Arial", 14))
    # mean_checkbox_var = tk.BooleanVar()
    multiply_checkbox_var = tk.BooleanVar()
    every_second_var = tk.BooleanVar()
    every_third_var = tk.BooleanVar()
    # mean_checkbox = ttk.Checkbutton(frame, text="РџСЂРѕРёР·РІРµСЃС‚Рё РІС‹С‡РёСЃР»РµРЅРёСЏ", variable=mean_checkbox_var, command=select_mean, style='TCheckbutton')
    multiply_checkbox = ttk.Checkbutton(frame, text="Add tags", variable=multiply_checkbox_var, command=select_multiply, style='TCheckbutton')
    every_second_checkbox = ttk.Checkbutton(frame, text="Save the region of interest through a single value", variable=every_second_var, style='TCheckbutton')
    every_third_checkbox = ttk.Checkbutton(frame, text="Save the region of interest through two values", variable=every_third_var, style='TCheckbutton')
    plot_button = ttk.Button(frame, text="Save the region of interest", command=plot_graph, style='Large.TButton')
    save_existing_button = ttk.Button(frame, text="Save the region of interest in an existing file", command=browse_ROI_file, style='Large.TButton')
    view_button = ttk.Button(frame, text="View the chart", command=view_graph, style='Large.TButton')
    browse_button.grid(column=0, row=0, pady=10)
    path_label.grid(column=1, row=0, sticky=tk.W)
    start_time_label.grid(column=0, row=1, sticky=tk.W)
    start_time_entry.grid(column=1, row=1, sticky=tk.W)
    end_time_label.grid(column=0, row=2, sticky=tk.W)
    end_time_entry.grid(column=1, row=2, sticky=tk.W)
    # mean_checkbox.grid(column=0, row=5, sticky=tk.W)
    multiply_checkbox.grid(column=0, row=3, sticky=tk.W, pady=(10, 0))
    every_second_checkbox.grid(column=0, row=4, sticky=tk.W)
    every_third_checkbox.grid(column=0, row=5, sticky=tk.W)
    plot_button.grid(column=0, row=6, pady=10)
    save_existing_button.grid(column=0,row=7)
    view_button.grid(column=1, row=6, pady=10)
    width = 620
    height = 320
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
root.title("Preparing a dataset")
frame = ttk.Frame(frame, padding="20")
frame.pack()
view_main_menu()
root.mainloop()