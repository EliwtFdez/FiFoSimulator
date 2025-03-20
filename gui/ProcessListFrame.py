import tkinter as tk
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt

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
