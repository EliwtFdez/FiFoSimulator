from tkinter import ttk

class ButtonFrame:
    """Clase para el marco de botones de acción"""
    def __init__(self, parent, clear_callback, exit_callback):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        
        clear_button = ttk.Button(self.frame, text="Limpiar Todo", command=clear_callback)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        exit_button = ttk.Button(self.frame, text="Salir", command=exit_callback)
        exit_button.pack(side=tk.RIGHT, padx=5)