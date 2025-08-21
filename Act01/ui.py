import os
import time
import algorithms
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Root(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.default_font = tkFont.Font(family="Calibri",size=12)
        self.title("Actividad 01")
        self.geometry("1359x493")
        self.option_add('*font', self.default_font)
        self.array = []
        self.selected_array_size = tk.StringVar()
        self.selected_array_size.set(100)
        self.size_options = [100, 1000, 10000, 100000]
        self.time_text = tk.StringVar()
        self.array_size_label_variable = tk.StringVar()
        self.search_result = tk.StringVar()
        self.search_result.set("Resultados: ")
        self.placeholder_text = "Escribe un número a buscar..."
        self.placeholder_color = "gray"
        self.default_color = "black"
        self.time_text.set("Tiempo: ")
        self.array_size_label_variable.set("Tamaño: ")
        self.linear_search_time_list = [0, 0, 0, 0]
        self.binary_search_time_list = [0, 0, 0, 0]
        self.create_widgets()

    def create_widgets(self):
        self.frame_label_pack = tk.Frame(self)
        self.frame_label_pack.pack(padx=30, pady=10, fill='x')
        self.array_label = tk.Label(self.frame_label_pack, text="Elige la cantidad de elementos que contendra el arreglo:").pack(anchor='w')

        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack(fill='x')

        self.size_list = ttk.Combobox(self.frame_grid, values=self.size_options, textvariable=self.selected_array_size, state="readonly")
        self.size_list.set(100)
        self.size_list.grid(row=0, column=0, padx=30, pady=10, sticky='w')

        self.create_sorted_array_button = tk.Button(self.frame_grid, text="Crear arreglo ordenado", command=self.on_button_click_create_sorted_array)
        self.create_unsorted_array_button = tk.Button(self.frame_grid, text="Crear arreglo desordenado", command=self.on_button_click_create_unsorted_array)
        self.create_sorted_array_button.grid(row=0, column=1, padx=30, pady=5, sticky='ew')
        self.create_unsorted_array_button.grid(row=1, column=1, padx=30, pady=5, sticky='ew')

        self.write_at_txt_array_button = tk.Button(self.frame_grid, text="Escribir arreglo en txt", state=tk.DISABLED, command=self.write_data)
        self.write_at_txt_array_button.grid(row=1, column=0, padx=30, pady=5, sticky='ew')

        self.frame_listbox = tk.Frame(self.frame_grid)
        self.scrollbar = tk.Scrollbar(self.frame_listbox, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.frame_listbox, yscrollcommand=self.scrollbar.set, width=52, height=5)
        self.scrollbar.config(command=self.listbox.yview)

        self.search_value = tk.Entry(self.frame_grid, width=30)
        self.search_value.grid(row=3, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        self.add_placeholder()
        self.search_value.bind("<FocusIn>", self.on_focus_in)
        self.search_value.bind("<FocusOut>", self.on_focus_out)

        self.linear_search_button = tk.Button(self.frame_grid, text="Busqueda Lineal", state=tk.DISABLED, command=self.on_button_click_linear_search)
        self.binary_search_button = tk.Button(self.frame_grid, text="Busqueda Binaria", state=tk.DISABLED, command=self.on_button_click_binary_search)
        self.linear_search_button.grid(row=4, column=0, padx=30, pady=10, sticky='ew')
        self.binary_search_button.grid(row=4, column=1, padx=30, pady=10, sticky='ew')

        self.generate_plot_button = tk.Button(self.frame_grid, text="Generar gráfica automaticamente", command=self.on_button_click_generate_graphic)
        self.generate_plot_button.grid(row=5, column=0, columnspan=2, padx=30, pady=10, sticky='ew')

        self.frame_results = tk.Frame(self.frame_grid, relief="sunken", borderwidth=1)
        self.frame_results.grid(row=6, column=0, columnspan=2, padx=30, pady=10, sticky='ew')

        self.search_found_label = tk.Label(self.frame_results, textvariable=self.search_result, anchor='w', wraplength=200)
        self.time_label = tk.Label(self.frame_results, textvariable=self.time_text, anchor='w', wraplength=200)
        self.array_size_label = tk.Label(self.frame_results, textvariable=self.array_size_label_variable, anchor='w', wraplength=200)
        self.search_found_label.grid(row=0, column=0, rowspan=2, padx=(20, 60), pady=10, sticky='nw')
        self.time_label.grid(row=0, column=1, padx=20, pady=10, sticky='w')
        self.array_size_label.grid(row=1, column=1, padx=20, pady=10, sticky='w')


        self.frame_plot = tk.Frame(self.frame_grid)
        self.frame_plot.grid(row=0, column=2, columnspan=10, rowspan=20, padx=30, pady=10)
        self.plot_array()


    def create_popup(self, msg:str):
        if not isinstance(msg, str):
            raise TypeError("PopUp no creado correctamente, es necesario una string.")
        self.warning = tk.Toplevel(self)
        self.warning.title("Info")
        self.warning.geometry("300x100")

        self.label = tk.Label(self.warning, text=msg, wraplength=250)
        self.label.pack(expand=True, fill='both')

    def activate_button(self, state1, state2, state3):
        self.write_at_txt_array_button.config(state=state1)
        self.linear_search_button.config(state=state2)
        self.binary_search_button.config(state=state3)
        self.frame_listbox.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky='ew')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)


    def write_data(self):
        with open('numeros.txt', 'w') as file:
            for number in self.array:
                file.write(str(number) + ', ')
        
        if os.path.exists('numeros.txt'):
            self.create_popup("✅ El archivo se creó exitosamente.")
        else:
            self.create_popup("❌ Error: El archivo no se pudo crear.")

    def plot_array(self):
        # Limpiar el frame de la gráfica si ya existe un widget
        for widget in self.frame_plot.winfo_children():
            widget.destroy()

        # Crear una figura de Matplotlib
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Graficar las dos listas en el mismo eje usando líneas
        ax.plot(self.size_options, self.linear_search_time_list, color="red", label="Búsqueda Lineal")
        ax.plot(self.size_options, self.binary_search_time_list, color="blue", label="Búsqueda Binaria")

        # Etiquetas y leyenda
        ax.set_xlabel("Tamaño Lista")
        ax.set_ylabel("Tiempo (milisegundos)")
        ax.legend()
        ax.grid(True)

        # Integrar la figura en el Canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Empaquetar el widget del Canvas en el frame de la GUI
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_button_click_create_sorted_array(self):
        self.array = algorithms.create_sorted_array(int(self.selected_array_size.get()))
        self.activate_button(tk.NORMAL, tk.NORMAL, tk.NORMAL)
        self.array_size_label_variable.set(f"Tamaño: {self.selected_array_size.get()}")
        self.fill_listbox()

    def on_button_click_create_unsorted_array(self):
        self.array = algorithms.create_unsorted_array(int(self.selected_array_size.get()))
        self.activate_button(tk.NORMAL, tk.NORMAL, tk.DISABLED)
        self.array_size_label_variable.set(f"Tamaño: {self.selected_array_size.get()}")
        self.fill_listbox()

    def fill_listbox(self):
        self.listbox.delete(0, tk.END)
        for i in range(len(self.array)):
            self.listbox.insert(tk.END, self.array[i])

    def on_button_click_binary_search(self):
        start_time = time.perf_counter()
        if algorithms.binary_search(self.array, int(self.search_value.get())) == 1:
            self.search_result.set(f"Resultados: \nNúmero {self.search_value.get()} encontrado")
        else:
            self.search_result.set(f"Resultados: \nNúmero {self.search_value.get()} no encontrado")
        end_time = time.perf_counter()

        duration = ((start_time - end_time) * 1000)
        total_time = int(duration * 10**4) / 10**4
        self.time_text.set(f"Tiempo: {total_time}ms")

        self.update_time_array(self.binary_search_time_list, total_time)
        self.plot_array()

    def on_button_click_linear_search(self):
        start_time = time.perf_counter()
        if algorithms.linear_search(self.array, int(self.search_value.get())) == 1:
            self.search_result.set(f"Resultados: \nNúmero {self.search_value.get()} encontrado")
        else:
            self.search_result.set(f"Resultados: \nNúmero {self.search_value.get()} no encontrado")
        end_time = time.perf_counter()
        duration = ((end_time - start_time) * 1000)
        total_time = int(duration * 10**4) / 10**4
        self.time_text.set(f"Tiempo: {total_time}ms")
        self.update_time_array(self.linear_search_time_list, total_time)
        self.plot_array()

    def on_button_click_generate_graphic(self):
        self.create_popup("Gráfica generada con éxito")
        self.create_automatic_graphic()

    def create_automatic_graphic(self):
        self.search_value.delete(0, tk.END)
        self.search_value.insert(0, 1)
        for i in range(10):
            for j in self.size_options:
                self.test_cases(j)
        self.plot_array()
            
    def test_cases(self, number):
        self.selected_array_size.set(number)
        self.array = algorithms.create_sorted_array(number)
        self.on_button_click_binary_search()
        self.array= algorithms.create_unsorted_array(number)
        self.on_button_click_linear_search()

    def update_time_array(self, actual_array, total_time):
        if(self.selected_array_size.get() == "100"):
            actual_array[0] = (actual_array[0] + total_time) / 2
        elif(self.selected_array_size.get() == "1000"):
            actual_array[1] = (actual_array[1] + total_time) / 2
        elif(self.selected_array_size.get() == "10000"):
            actual_array[2] = (actual_array[2] + total_time) / 2
        elif(self.selected_array_size.get() == "100000"):
            actual_array[3] = (actual_array[3] + total_time) / 2
        else:
            print("Size out of range")

    def add_placeholder(self):
        if not self.search_value.get():
            self.search_value.insert(0, self.placeholder_text)
            self.search_value.config(fg=self.placeholder_color)

    def on_focus_in(self, event):
        if self.search_value.get() == self.placeholder_text:
            self.search_value.delete(0, tk.END)
            self.search_value.config(fg=self.default_color)

    def on_focus_out(self, event):
        if not self.search_value.get():
            self.add_placeholder()

    def run(self):
        self.mainloop()