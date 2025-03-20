from tkinter import ttk
import tkinter as tk

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
