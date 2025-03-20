from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt

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
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def clear(self):
        """Limpia el diagrama de Gantt"""
        for widget in self.frame.winfo_children():
            widget.destroy()