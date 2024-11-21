import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import os
import tkinter.font as tkFont
import threading
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import r2_score

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
    for column, name in zip(dataframe.columns, gas_names):
        tree.heading(column, text=name)
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
     
def display_df_combined():
    display_dataframe_as_table(df_combined_avg, "Values")

def display_response_df_combined():
    display_dataframe_as_table(response_df_combined_avg, "Response")

def get_user_values(air_entries, experiment_name_entries, mean_entries, experiments):
    df = pd.read_csv(selected_file_path, sep=';', decimal='.')
    columns_to_drop = ["Indexes", "Humidity", "Temperature"]
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    if columns_to_drop_existing:
        df = df.drop(columns=columns_to_drop_existing)
        air_values = [int(entry.get()) for entry in air_entries]
        mean_values = [float(entry.get()) for entry in mean_entries]
        df_mean_list = []
        response_df_list = []
        global gas_names
        gas_names = [experiment_name_entries[i].get() for i in range(experiments)]
        window_size = 5
        mean_values_list = []
        for air_value in air_values:
            closest_time_index = df['Time'].sub(air_value).abs().idxmin()
            start_index = max(0, closest_time_index - window_size)
            end_index = min(len(df), closest_time_index + window_size+1)
            air_df_mean = df.iloc[start_index:end_index].mean()
            mean_values_list.append(air_df_mean)
        mean_df = pd.DataFrame(mean_values_list)
        final_mean = mean_df.mean()
        for mean_value in mean_values:
            closest_time_index = df['Time'].sub(mean_value).abs().idxmin()
            start_index = max(0, closest_time_index - window_size)
            end_index = min(len(df), closest_time_index + window_size+1)
            df_mean = df.iloc[start_index:end_index].mean()
            df_mean_list.append(df_mean)
            response_df=final_mean.div(df_mean)
            response_df-=1.0
            response_df*=100
            response_df_list.append(response_df)
        global df_combined_avg, response_df_combined_avg
        df_combined = pd.concat(df_mean_list, axis=1)
        df_combined = df_combined.drop('Time', axis=0)
        df_combined.columns = gas_names
        df_combined_avg = pd.DataFrame()
        for gas in gas_names:
            gas_columns = [col for col in df_combined.columns if col.startswith(gas)]
            df_combined_avg[gas] = df_combined[gas_columns].mean(axis=1)
        response_df_combined = pd.concat(response_df_list, axis=1)
        response_df_combined = response_df_combined.drop('Time', axis=0)
        response_df_combined.columns = gas_names
        response_df_combined_avg = pd.DataFrame()
        for gas in gas_names:
            gas_columns = [col for col in response_df_combined.columns if col.startswith(gas)]
            response_df_combined_avg[gas] = response_df_combined[gas_columns].mean(axis=1).abs()
        threads = []
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
        selected_file = f"Calibration_curves_{file_name}_{current_datetime}"
        df_combined.to_csv(selected_file+"_Values.csv", sep=';', decimal='.')
        response_df_combined.to_csv(selected_file+"_Response.csv", sep=';', decimal='.')
        new_response_df_combined=response_df_combined_avg
        for display_func in [display_df_combined, display_response_df_combined]:
            thread = threading.Thread(target=display_func)
            threads.append(thread)
            thread.start()
        num_columns = len(new_response_df_combined.columns)
        numerical_column_names = [str(i) for i in range(1, num_columns + 1)]
        new_response_df_combined.columns = numerical_column_names
        for index, row in new_response_df_combined.iterrows():
            x = new_response_df_combined.columns.astype(float).values.reshape(-1, 1)
            y = row.values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(x, y)
            slope = model.coef_[0][0]
            intercept = model.intercept_[0]
            y_pred = model.predict(x)
            r_squared = r2_score(y, y_pred)
            plt.figure(f'{index}', figsize=(10, 5))
            plt.scatter(x, y, color='blue', label='Data points')
            plt.plot(x, y_pred, color='red', label='Linear regression')
            plt.xlabel('Indexes')
            plt.ylabel('Values')
            plt.title(f'Linear Regression Plot for {index}')
            equation_text = f'y = {slope:.2f}x + {intercept:.2f}\nR^2 = {r_squared:.2f}'
            handles, labels = plt.gca().get_legend_handles_labels()
            handles.append(plt.Line2D([0], [0], color='white', label=equation_text))
            plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()
        plt.show()
        for thread in threads:
            thread.join()
        recreate_main_menu()
   
def select_mean():
    custom_font = tkFont.Font(family="Arial", size=14)
    global column_name
    column_name = 'Time' 
    if selected_file_path=='':
        show_custom_info_dialog("Error!", "Please specify the path to the file.", custom_font)
        return
    for widget in frame.winfo_children():
        widget.destroy()
    air_experiments_label = ttk.Label(frame, text="Enter the number of Rair:", font=("Arial", 14))
    air_experiments_label.grid(row=0, column=1, pady=10)
    air_experiments_entry = ttk.Entry(frame, font=("Arial", 14), width=15)
    air_experiments_entry.grid(row=0, column=2, pady=10)
    experiments_label = ttk.Label(frame, text="Enter the number of Experiments:", font=("Arial", 14))
    experiments_label.grid(row=1, column=1, pady=10)
    experiments_entry = ttk.Entry(frame, font=("Arial", 14), width=15)
    experiments_entry.grid(row=1, column=2, pady=10)
    experiment_name_entries = []
    def create_input_widgets(air_experiments_count, experiments):
        experiments_label.grid_forget()
        experiments_entry.grid_forget()
        air_experiments_label.grid_forget()
        air_experiments_entry.grid_forget()
        for idx in range(air_experiments_count):
            air_value_label = ttk.Label(frame, text=f"Timestamps for Rair {idx + 1}:", font=("Arial", 14))
            air_value_label.grid(row=idx, column=1, pady=10)
            air_value_entry = ttk.Entry(frame, font=("Arial", 14), width=15)
            air_value_entry.grid(row=idx, column=2, pady=10)
            air_entries.append(air_value_entry)
        for idx in range(experiments):
            name_label = ttk.Label(frame, text=f"Name of Experiment {idx + 1}:", font=("Arial", 14))
            name_label.grid(row=air_experiments_count + idx + 1, column=1, pady=10)
            name_entry = ttk.Entry(frame, font=("Arial", 14), width=15)
            name_entry.grid(row=air_experiments_count + idx + 1, column=2, pady=10)
            experiment_name_entries.append(name_entry)
            value_label = ttk.Label(frame, text=f"Timestamps for Experiment {idx + 1}:", font=("Arial", 14))
            value_label.grid(row=air_experiments_count + idx + 1, column=3, pady=10, padx=(10,0))
            value_entry = ttk.Entry(frame, font=("Arial", 14), width=10)
            value_entry.grid(row=air_experiments_count + idx + 1, column=4, pady=10)
            mean_entries.append(value_entry)
        def continue_button_click():
            name_values = [entry.get() for entry in experiment_name_entries]
            value_values = [entry.get() for entry in mean_entries]
            if not all(name_values) or not all(value_values):
                show_custom_info_dialog("Error!", "Please fill in all the fields.", custom_font)
            else:
                get_user_values(air_entries, experiment_name_entries, mean_entries, experiments)
        continue_mean_button = ttk.Button(frame, text="Continue", command=continue_button_click, style='Large.TButton')
        continue_mean_button.grid(row=air_experiments_count + experiments + 1, column=2, pady=10)
        continue_experiments_button.grid_forget()
        main_menu_button = ttk.Button(frame, text="Main menu", command=recreate_main_menu, style='Large.TButton')
        main_menu_button.grid(column=3, row=air_experiments_count + experiments + 1, pady=10, padx=30)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        root.geometry(f"850x380")
    def handle_experiments_entry():
        experiments_num=experiments_entry.get()
        if not experiments_num:
            show_custom_info_dialog("Error!", "Please enter the number of experiments.", custom_font)
            return
        experiments = int(experiments_entry.get())
        air_experiments_count = int(air_experiments_entry.get())
        create_input_widgets(air_experiments_count, experiments)
    continue_experiments_button = ttk.Button(frame, text="Continue", command=handle_experiments_entry, style='Large.TButton')
    continue_experiments_button.grid(row=2, columnspan=3, pady=10)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    root.geometry(f"520x180")

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
    root.geometry(f"{root_width}x150")

def recreate_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    view_main_menu()

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def view_main_menu():
    for widget in frame.winfo_children():
        widget.destroy()
    global selected_file_path,air_entries,mean_entries,entry_air_entries,entry_gas_entries,entry_gas_names,final_indexes, column_name,browse_button,path_label,start_time_label,start_time_entry,end_time_label,end_time_entry,plot_button,view_button,multiply_checkbox_var,every_second_var, every_third_var
    mean_entries = []
    air_entries=[]
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
    plot_button = ttk.Button(frame, text="Calculation of calibration curves", command=select_mean, style='Large.TButton')
    view_button = ttk.Button(frame, text="View the chart", command=view_graph, style='Large.TButton')
    browse_button.grid(column=0, row=0, pady=10)
    path_label.grid(column=1, row=0, sticky=tk.W)
    # start_time_label.grid(column=0, row=1, sticky=tk.W)
    # start_time_entry.grid(column=1, row=1)
    # end_time_label.grid(column=0, row=2, sticky=tk.W)
    # end_time_entry.grid(column=1, row=2)
    plot_button.grid(column=0, row=1, pady=10)
    view_button.grid(column=1, row=1, pady=10, padx=(50,0))
    width = 500
    height = 150
    root.geometry(f"{width}x{height}")
    root.minsize(500,150)

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
root.title("Calculate calibration curves")
frame = ttk.Frame(frame, padding="20")
frame.pack()
view_main_menu()
root.mainloop()