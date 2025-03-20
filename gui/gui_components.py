import tkinter as tk
from tkinter import ttk, messagebox
from ..Algorithm.fifo_algorithm import FIFOAlgorithm
from .ProcessListFrame import ProcessListFrame
from .gui_components import InputFrame   # Se importa la clase InputFrame desde gui/gui_components.py

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
