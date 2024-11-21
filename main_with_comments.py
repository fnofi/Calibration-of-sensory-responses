import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import math
from itertools import zip_longest

selected_file_path = ""

def plot_graph():
    column_name = column_name_entry.get()
    start_time = float(start_time_entry.get())
    end_time = float(end_time_entry.get())
    df = pd.read_csv(selected_file_path, sep=';', decimal='.', encoding='utf-8-sig')
    # print(df)
    selected_data = df.loc[(df[column_name] >= start_time) & (df[column_name] <= end_time)]
    # print(selected_data)
    # for column in df.columns:
    #     if column != column_name:
    #         plt.figure()
    #         plt.plot(df[column_name], df[column], label=column)
    #         plt.xlabel('Время')
    #         plt.ylabel('Значение')
    #         plt.title(f'График для столбца {column}')
    # plt.legend()
    # for column in selected_data.columns:
    #     if column != column_name:
    #         plt.figure(f'{column}')
    #         plt.plot(selected_data[column_name], selected_data[column], label=column)
    #         plt.xlabel('Время')
    #         plt.ylabel('Значение')
    #         plt.title(f'График области интереса {column}')
    #         plt.legend()
    # plt.tight_layout()
    # plt.show()
    if mean_checkbox_var.get():
        # selected_data = selected_data.drop(columns=[column_name])

        # for column in selected_data.columns:
        #     numeric_columns = selected_data.select_dtypes(include=['float64', 'int64'])
        #     data = [float(str(value).replace(',', '.')) for value in numeric_columns.values.flatten()]
        # mean_value = sum(data) / len(data)
        # mean_df = pd.DataFrame({'mean_value': [mean_value]})
        # mean_df.to_csv('mean_value.csv', index=False, header=False)
        # print(mean_value)
        # mean_label.config(text=mean_value)
        get_user_values(selected_data)
        # filepath = filedialog.askopenfilename()
        # if filepath:
        #     multiply_value = pd.read_csv(filepath, header=None)
        #     selected_data.iloc[:, 1:] *= multiply_value.iloc[0, 0]
        #     selected_data.to_csv('selected_data.csv', index=False, sep=';')
        #     multiply_label.config(text="Результат хранится в файле selected_data.csv")
    # if os.path.exists('selected_data.csv'):
    #     selected_data.to_csv('selected_data.csv', mode='a', index=False, sep=';', decimal='.', header=False)
    # else:
    #     selected_data.to_csv('selected_data.csv', mode='a', index=False, sep=';', decimal='.')
    if every_second_var.get():
        if os.path.exists('selected_data_every_second.csv'):
            selected_data.iloc[::2].to_csv('selected_data_every_second.csv', mode='a', index=False, sep=';', decimal='.', header=False, encoding='utf-8-sig')
        else:
            selected_data.iloc[::2].to_csv('selected_data_every_second.csv', mode='a', index=False, sep=';', decimal='.', encoding='utf-8-sig')
    elif every_third_var.get():
        if os.path.exists('selected_data_every_third.csv'):
            selected_data.iloc[::3].to_csv('selected_data_every_third.csv', mode='a', index=False, sep=';', decimal='.', header=False, encoding='utf-8-sig')
        else:
            selected_data.iloc[::3].to_csv('selected_data_every_third.csv', mode='a', index=False, sep=';', decimal='.', encoding='utf-8-sig')
    else:
        if os.path.exists('selected_data.csv'):
            selected_data.to_csv('selected_data.csv', mode='a', index=False, sep=';', decimal='.', header=False)
        else:
            selected_data.to_csv('selected_data.csv', mode='a', index=False, sep=';', decimal='.')

def view_graph():
    column_name = column_name_entry.get()
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    # df.to_csv('NO2_new_time.csv', index=False, sep=';', decimal='.')
    plt.figure()
    for column in df.columns:
        if column != column_name:
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Время')
            plt.ylabel('Значение')
    plt.legend()
    plt.title('Все графики')
    for column in df.columns:
        if column != column_name:
            plt.figure(f'{column}')
            plt.plot(df[column_name], df[column], label=column)
            plt.xlabel('Время')
            plt.ylabel('Значение')
            plt.title(f'График для столбца {column}')
            plt.legend()
    plt.show()

def get_user_values(df):
    user_values = []
    column_name = column_name_entry.get()
    divide_r_rair = pd.DataFrame()
    log_r_rair = pd.DataFrame()
    r_rair_rair = pd.DataFrame()
    abs_r_rair_rair = pd.DataFrame()
    time_column = df[column_name]
    df = df.drop(columns=[column_name])
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
    divide_r_rair.to_csv('divide_R_Rair.csv', index=False, sep=';')
    log_r_rair.to_csv('log_R_Rair.csv', index=False, sep=';')
    r_rair_rair.to_csv('r_rair_rair.csv', index=False, sep=';')
    abs_r_rair_rair.to_csv('abs_r_rair_rair.csv', index=False, sep=';')

def enter_index():
    air_label.pack()
    air_input.pack()
    gas_label.pack()
    gas_input.pack()
    continue_button.pack()
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def enter_air_gas():
    air_count = int(air_input.get())
    gas_count = int(gas_input.get())
    air_label.pack_forget()
    air_input.pack_forget()
    gas_input.pack_forget()
    gas_label.pack_forget()
    continue_button.pack_forget()
    multiply_checkbox_var.set(0)
    for i in range(air_count):
        air_entry_label = tk.Label(content_frame, text=f'Воздух {i+1}')
        air_entry_label.pack()
        entry_air = tk.Entry(content_frame)
        entry_air.pack()
        entry_air_entries.append(entry_air)
    for i in range(gas_count):
        gas_name_label = tk.Label(content_frame, text=f'Введите название газа {i+1}')
        gas_name_label.pack()
        entry_gas_name = tk.Entry(content_frame)
        entry_gas_name.pack()
        gas_entry_label = tk.Label(content_frame, text=f'Газ {i+1}')
        gas_entry_label.pack()
        entry_gas = tk.Entry(content_frame)
        entry_gas.pack()
        entry_gas_names.append(entry_gas_name)
        entry_gas_entries.append(entry_gas)
    add_air_gas_button = ttk.Button(content_frame, text="Продолжить", command=lambda: add_air_gas(air_count, gas_count), style='Large.TButton')
    add_air_gas_button.pack()
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# def add_air_gas(air_count, gas_count):
#     df = pd.read_csv(selected_file_path, sep=';', decimal='.')
#     air_entries = []
#     gas_entries = []
#     gas_names = []
#     final_air = []
#     final_gas = []
#     range1 = range(air_count)
#     range2 = range(gas_count)
#     for i,j in zip(range1, range2):
#         air_entries.append(entry_air_entries[i].get())
#         gas_names.append(entry_gas_names[j].get())
#         gas_entries.append(entry_gas_entries[j].get())
#         for k in range(int(air_entries[i])):
#             final_air.append('Воздух')
#         for m in range(int(gas_entries[j])):
#             final_gas.append(gas_names[j])
#         final_air.extend(final_gas)
#         final_gas=[]
#     print(final_air)
#     df['Индексы']=''
#     df['Индексы'].iloc[:len(final_air)]=final_air[:len(final_air)]
#     df['Индексы'] = df['Индексы'].fillna('')
#     df.to_csv('indexs.csv', index=False, sep=';', decimal='.', encoding='utf-8-sig')

def add_air_gas(air_count, gas_count):
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    final_indexes = []
    air_times = [float(entry_air_entries[i].get()) for i in range(air_count)]
    gas_times = [(entry_gas_names[i].get(), float(entry_gas_entries[i].get())) for i in range(gas_count)]
    time_interval = 1.4/60.0
    while air_times or gas_times:
        if air_times:
            air_time = air_times.pop(0)
            final_indexes.extend(['Air'] * math.ceil(air_time / time_interval))
        if gas_times:
            gas_name, gas_time = gas_times.pop(0)
            final_indexes.extend([gas_name] * math.ceil(gas_time / time_interval))
    df['Indexes'] = ''
    df['Indexes'].iloc[:len(final_indexes)] = final_indexes[:len(final_indexes)]
    df['Indexes'] = df['Indexes'].fillna('')
    df.to_csv('indexs.csv', index=False, sep=';', decimal='.', encoding='utf-8-sig')


# def add_air_gas(air_count, gas_count):
#     custom_font = tkFont.Font(family="Arial", size=14)
#     for i in range(air_count):
#         entry_air = entry_air_entries[i].get()
#         if not entry_air:
#             show_custom_info_dialog("Ошибка!", f"Пожалуйста, заполните поле 'Воздух {i+1}'.", custom_font)
#             return
#     for i in range(gas_count):
#         entry_gas_name = entry_gas_names[i].get()
#         entry_gas = entry_gas_entries[i].get()
#         if not entry_gas_name or not entry_gas:
#             show_custom_info_dialog("Ошибка!", f"Пожалуйста, заполните все поля для газа {i+1}.", custom_font)
#             return
#     df = pd.read_csv(selected_file_path, sep=';', decimal='.')
#     air_entries = [entry_air_entries[i].get() for i in range(air_count)]
#     gas_names = [entry_gas_names[i].get() for i in range(gas_count)]
#     gas_entries = [entry_gas_entries[i].get() for i in range(gas_count)]
#     final_indexes = []
#     max_count = max(air_count, gas_count)
#     for i in range(max_count):
#         if i < air_count:
#             final_indexes.extend(['Air'] * int(air_entries[i]))
#         if i < gas_count:
#             final_indexes.extend([gas_names[i]] * int(gas_entries[i]))
#     df['Indexes']=''
#     df['Indexes'].iloc[:len(final_indexes)]=final_indexes[:len(final_indexes)]
#     df['Indexes'] = df['Indexes'].fillna('')
#     df.to_csv('indexs.csv', index=False, sep=';', decimal='.')
#     recreate_main_menu()
#     show_custom_info_dialog("Успешно!", f"Данные успешно сохранены в файл indexs.csv.", custom_font)

# def add_air_gas(air_count, gas_count):
#     custom_font = tkFont.Font(family="Arial", size=14)
    
#     # Проверяем заполнены ли все поля для воздуха
#     for i in range(air_count):
#         entry_air = entry_air_entries[i].get()
#         if not entry_air:
#             show_custom_info_dialog("Ошибка!", f"Пожалуйста, заполните поле 'Воздух {i+1}'.", custom_font)
#             return
    
#     # Проверяем заполнены ли все поля для газа
#     for i in range(gas_count):
#         entry_gas_name = entry_gas_names[i].get()
#         entry_gas = entry_gas_entries[i].get()
#         if not entry_gas_name or not entry_gas:
#             show_custom_info_dialog("Ошибка!", f"Пожалуйста, заполните все поля для газа {i+1}.", custom_font)
#             return
    
#     # Создаем DataFrame из файла
#     df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    
#     # Получаем введенные данные о воздухе и газе
#     air_entries = [int(entry_air_entries[i].get()) for i in range(air_count)]
#     gas_names = [entry_gas_names[i].get() for i in range(gas_count)]
#     gas_entries = [int(entry_gas_entries[i].get()) for i in range(gas_count)]
    
#     # Вычисляем общее количество меток на основе последнего значения поля воздуха
#     # Вычисляем общее количество меток на основе последнего значения поля воздуха
#     total_labels = int(entry_air_entries[-1].get())

#     # Вычисляем общее количество меток для воздуха
#     total_air_labels = sum(air_entries)

#     # Вычисляем общее количество меток для газа
#     total_gas_labels = sum(gas_entries)

#     # Создадим пустой список для всех меток
#     final_indexes = []

#     # Распределение меток между воздухом и газом
#     for i in range(air_count):
#         air_label_count = int(air_entries[i] * total_labels / (total_air_labels + total_gas_labels))
#         final_indexes.extend(['Air'] * air_label_count)

#     for i in range(gas_count):
#         gas_label_count = int(gas_entries[i] * total_labels / (total_air_labels + total_gas_labels))
#         final_indexes.extend([gas_names[i]] * gas_label_count)

#     # Заполняем DataFrame сформированными метками
#     df['Indexes']=''
#     df['Indexes'].iloc[:len(final_indexes)]=final_indexes[:len(final_indexes)]
#     df['Indexes'] = df['Indexes'].fillna('')
#     # Сохраняем DataFrame в CSV файл
#     df.to_csv('indexs.csv', index=False, sep=';', decimal='.')
    
#     # Пересоздаем главное меню
#     recreate_main_menu()
    
#     # Показываем диалоговое окно об успешном сохранении
#     show_custom_info_dialog("Успешно!", f"Данные успешно сохранены в файл indexs.csv.", custom_font)

def select_mean():
    if mean_checkbox_var.get():
        multiply_checkbox_var.set(0)
        mean_label.config(text="")
        column_name = column_name_entry.get()
        df = pd.read_csv(selected_file_path, sep=';', decimal='.')
        df = df.drop(columns=[column_name])
        for idx, col in enumerate(df.columns):
            entry_label = tk.Label(root, text=col)
            entry_label.grid(row=idx+1, column=0, pady=10)
            entry = tk.Entry(root)
            entry.grid(row=idx+1, column=1, pady=10)
            mean_entries.append(entry)

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def select_multiply():
    if multiply_checkbox_var.get():
        mean_checkbox_var.set(0)
        multiply_label.config(text="")
        enter_index()

def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()
    print("Selected file:", selected_file_path)
    path_label.config(text=selected_file_path)

mean_entries = []

entry_air_entries = []

entry_gas_entries = []
entry_gas_names = []
final_indexes=[]
import tkinter as tk
from tkinter import ttk

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


root = tk.Tk()

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", on_canvas_configure)

content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")


root.title("Построение графика")

frame = ttk.Frame(content_frame, padding="20")
frame.pack()

browse_button = ttk.Button(frame, text="Выбрать файл", command=browse_file, style='Large.TButton')
browse_button.grid(column=0, row=0, pady=10)

path_label = ttk.Label(frame, text="", font=("Arial", 14))
path_label.grid(column=1, row=0, sticky=tk.W)

column_name_label = ttk.Label(frame, text="Название столбца (X):", font=("Arial", 14))
column_name_label.grid(column=0, row=1, sticky=tk.W)

column_name_entry = ttk.Entry(frame, width=20, font=("Arial", 14))
column_name_entry.grid(column=1, row=1, sticky=tk.W)

start_time_label = ttk.Label(frame, text="Начальное время:", font=("Arial", 14))
start_time_label.grid(column=0, row=2, sticky=tk.W)

start_time_entry = ttk.Entry(frame, width=10, font=("Arial", 14))
start_time_entry.grid(column=1, row=2, sticky=tk.W)

end_time_label = ttk.Label(frame, text="Конечное время:", font=("Arial", 14))
end_time_label.grid(column=0, row=3, sticky=tk.W)

end_time_entry = ttk.Entry(frame, width=10, font=("Arial", 14))
end_time_entry.grid(column=1, row=3, sticky=tk.W)

mean_checkbox_var = tk.BooleanVar()
mean_checkbox = ttk.Checkbutton(frame, text="Произвести вычисления", variable=mean_checkbox_var, command=select_mean, style='TCheckbutton')
mean_checkbox.grid(column=0, row=4, sticky=tk.W)

mean_label = ttk.Label(frame, text="", font=("Arial", 14))
mean_label.grid(column=1, row=4, sticky=tk.W)

multiply_checkbox_var = tk.BooleanVar()
multiply_checkbox = ttk.Checkbutton(frame, text="Добавить индексы", variable=multiply_checkbox_var, command=select_multiply, style='TCheckbutton')
multiply_checkbox.grid(column=0, row=5, sticky=tk.W)

every_second_var = tk.BooleanVar()
every_second_checkbox = ttk.Checkbutton(frame, text="Сохранить через одно значение", variable=every_second_var, style='TCheckbutton')
every_second_checkbox.grid(column=0, row=6, sticky=tk.W)

every_third_var = tk.BooleanVar()
every_third_checkbox = ttk.Checkbutton(frame, text="Сохранить через два значения", variable=every_third_var, style='TCheckbutton')
every_third_checkbox.grid(column=0, row=7, sticky=tk.W)

multiply_label = ttk.Label(frame, text="", font=("Arial", 14))
multiply_label.grid(column=1, row=5, sticky=tk.W)

plot_button = ttk.Button(frame, text="Построить график", command=plot_graph, style='Large.TButton')
plot_button.grid(column=0, row=8, pady=10)

view_button = ttk.Button(frame, text="Посмотреть график", command=view_graph, style='Large.TButton')
view_button.grid(column=1, row=8, columnspan=2, pady=10)
air_label = tk.Label(content_frame, text="Введите количество воздуха")

gas_label = tk.Label(content_frame, text="Введите количество газа")

gas_input = tk.Entry(content_frame)

air_input = tk.Entry(content_frame)

continue_button = ttk.Button(content_frame, text="Продолжить", command=enter_air_gas, style='Large.TButton')


root.mainloop()