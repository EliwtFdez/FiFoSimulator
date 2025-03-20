import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InputFrame:
    """Clase para el marco de entrada de datos de procesos"""
    def __init__(self, parent, add_callback, calculate_callback):
        self.frame = ttk.LabelFrame(parent, text="Añadir Proceso", padding="10")
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nombre del proceso
        ttk.Label(self.frame, text="Nombre del Proceso:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.process_name = ttk.Entry(self.frame, width=15)
        self.process_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Ráfaga de CPU
        ttk.Label(self.frame, text="Ráfaga de CPU:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.burst_time = ttk.Entry(self.frame, width=10)
        self.burst_time.grid(row=0, column=3, padx=5, pady=5)
        
        # Tiempo de llegada
        ttk.Label(self.frame, text="Tiempo de Llegada:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.arrival_time = ttk.Entry(self.frame, width=10)
        self.arrival_time.grid(row=0, column=5, padx=5, pady=5)
        
        # Botones
        add_button = ttk.Button(self.frame, text="Añadir Proceso", command=add_callback)
        add_button.grid(row=0, column=6, padx=10, pady=5)
        
        calculate_button = ttk.Button(self.frame, text="Calcular FIFO", command=calculate_callback)
        calculate_button.grid(row=0, column=7, padx=10, pady=5)
    
    def get_process_data(self):
        """Obtiene los datos del proceso desde los campos de entrada"""
        name = self.process_name.get()
        try:
            burst = int(self.burst_time.get())
            arrival = int(self.arrival_time.get())
            
            if not name or burst <= 0:
                messagebox.showerror("Error", "Ingrese nombre válido y ráfaga positiva.")
                return None
            
            return {'name': name, 'burst': burst, 'arrival': arrival}
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos para ráfaga y tiempo de llegada.")
            return None
    
    def clear_fields(self):
        """Limpia los campos de entrada"""
        self.process_name.delete(0, tk.END)
        self.burst_time.delete(0, tk.END)
        self.arrival_time.delete(0, tk.END)

class ProcessListFrame:
    """Clase para el marco de lista de procesos"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Lista de Procesos", padding="10")
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Crear tabla para mostrar procesos
        columns = ('nombre', 'rafaga', 'llegada')
        self.process_table = ttk.Treeview(self.frame, columns=columns, show='headings', height=5)
        
        # Configurar encabezados
        self.process_table.heading('nombre', text='Proceso')
        self.process_table.heading('rafaga', text='Ráfaga CPU')
        self.process_table.heading('llegada', text='T. Llegada')
        
        # Ajustar ancho de columnas
        for col in columns:
            self.process_table.column(col, width=100, anchor='center')
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.process_table.yview)
        self.process_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.process_table.pack(fill=tk.BOTH, expand=True)
    
    def add_process_to_table(self, process):
        """Añade un proceso a la tabla"""
        self.process_table.insert('', tk.END, values=(process['name'], process['burst'], process['arrival']))
    
    def clear_table(self):
        """Limpia la tabla de procesos"""
        for item in self.process_table.get_children():
            self.process_table.delete(item)

class GanttFrame:
    """Clase para el marco del diagrama de Gantt"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Diagrama de Gantt", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def generate_chart(self, results):
        """Genera el diagrama de Gantt con los resultados calculados"""
        self.clear()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        y_pos = 0
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF']
        
        # Recolectar todos los tiempos de inicio y finalización
        all_times = []
        for process in results:
            all_times.append(process['arrival'])
            all_times.append(process['start'])
            all_times.append(process['completion'])
        
        # Ordenar y eliminar duplicados
        unique_times = sorted(list(set(all_times)))
        
        # Dibujar líneas verticales punteadas para cada tiempo significativo
        for time in unique_times:
            if time > 0:  # No dibujar línea en tiempo 0
                color = 'red' if any(p['arrival'] == time for p in results) else 'blue'
                ax.axvline(x=time, color=color, linestyle='--', alpha=0.7, linewidth=1)
        
        # Altura máxima para las líneas verticales
        max_y = len(results)
        
        for i, process in enumerate(results):
            color_idx = i % len(colors)
            
            # Dibujar línea punteada horizontal si el proceso esperó
            if process['start'] > process['arrival']:
                ax.plot([process['arrival'], process['start']], [y_pos, y_pos], 'r--', linewidth=2)
                # Marcar tiempo de llegada con un punto
                ax.plot(process['arrival'], y_pos, 'ro', markersize=8)
                ax.text(process['arrival'], y_pos-0.25, f"{process['arrival']}", ha='center', va='top', fontsize=8)
            
            # Dibujar barra del proceso
            ax.barh(y_pos, process['burst'], left=process['start'], color=colors[color_idx], edgecolor='black', alpha=0.8)
            ax.text(process['start'] + process['burst']/2, y_pos, process['name'], ha='center', va='center')
            
            # Marcar tiempo de inicio con un punto
            ax.plot(process['start'], y_pos, 'go', markersize=8)
            ax.text(process['start'], y_pos+0.25, f"{process['start']}", ha='center', va='bottom', fontsize=8)
            
            # Marcar tiempo de finalización con un punto
            ax.plot(process['completion'], y_pos, 'bo', markersize=8)
            ax.text(process['completion'], y_pos-0.25, f"{process['completion']}", ha='center', va='top', fontsize=8)
            
            y_pos += 1
        
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Procesos')
        ax.set_yticks(range(len(results)))
        ax.set_yticklabels([p['name'] for p in results])
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        
        max_time = max([p['completion'] for p in results]) if results else 0
        ax.set_xlim(0, max_time + 1)
        
        # Añadir leyenda para los puntos y líneas
        ax.plot([], [], 'ro', markersize=8, label='Tiempo de Llegada')
        ax.plot([], [], 'go', markersize=8, label='Tiempo de Inicio')
        ax.plot([], [], 'bo', markersize=8, label='Tiempo de Finalización')
        ax.plot([], [], 'r--', linewidth=1, label='Línea de Tiempo de Llegada')
        ax.plot([], [], 'b--', linewidth=1, label='Línea de Tiempo de Inicio/Fin')
        ax.legend(loc='upper center', bbox_to_anchor=(1, -0.15), ncol=10)
       
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def clear(self):
        """Limpia el diagrama de Gantt"""
        for widget in self.frame.winfo_children():
            widget.destroy()

class TimesFrame:
    """Clase para el marco de la tabla de tiempos"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Tabla de Tiempos", padding="10")
        self.frame.pack(fill=tk.X, padx=10, pady=10)
    
    def show_time_table(self, results):
        """Muestra la tabla de tiempos con los resultados calculados"""
        self.clear()
        
        # Crear tabla de tiempos
        columns = ('proceso', 'llegada', 'inicio', 'fin', 'tiempo_sistema', 'tiempo_espera')
        table = ttk.Treeview(self.frame, columns=columns, show='headings', height=len(results))
        
        # Configurar encabezados
        table.heading('proceso', text='Proceso')
        table.heading('llegada', text='T. Llegada')
        table.heading('inicio', text='T. Inicio')
        table.heading('fin', text='T. Finalización')
        table.heading('tiempo_sistema', text='T. Sistema')
        table.heading('tiempo_espera', text='T. Espera')
        
        # Ajustar ancho de columnas
        for col in columns:
            table.column(col, width=100, anchor='center')
        
        # Insertar datos
        total_turnaround = 0
        total_waiting = 0
        
        for process in results:
            table.insert('', tk.END, values=(
                process['name'],
                process['arrival'],
                process['start'],
                process['completion'],
                process['turnaround'],
                process['waiting']
            ))
            total_turnaround += process['turnaround']
            total_waiting += process['waiting']
        
        table.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Mostrar promedios
        stats_frame = ttk.Frame(self.frame)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        avg_turnaround = total_turnaround / len(results) if results else 0
        avg_waiting = total_waiting / len(results) if results else 0
        
        ttk.Label(stats_frame, text=f"Tiempo promedio de sistema: {avg_turnaround:.2f}").pack(side=tk.LEFT, padx=10)
        ttk.Label(stats_frame, text=f"Tiempo promedio de espera: {avg_waiting:.2f}").pack(side=tk.LEFT, padx=10)
    
    def clear(self):
        """Limpia la tabla de tiempos"""
        for widget in self.frame.winfo_children():
            widget.destroy()

class ButtonFrame:
    """Clase para el marco de botones de acción"""
    def __init__(self, parent, clear_callback, exit_callback):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        
        clear_button = ttk.Button(self.frame, text="Limpiar Todo", command=clear_callback)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        exit_button = ttk.Button(self.frame, text="Salir", command=exit_callback)
        exit_button.pack(side=tk.RIGHT, padx=5)