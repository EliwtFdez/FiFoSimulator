


from Algorithm.fifo_algorithm import FIFOAlgorithm
from gui import ButtonFrame, GanttFrame, TimesFrame
from gui.ProcessListFrame import ProcessListFrame
from gui.gui_components import InputFrame


class FIFOSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Algoritmo de Planificación FIFO")
        self.root.geometry("900x800")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para almacenar procesos
        self.processes = []
        
        # Crear el marco principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inicializar algoritmo FIFO
        self.fifo_algorithm = FIFOAlgorithm()
        
        # Crear componentes de la interfaz
        self.input_frame = InputFrame(main_frame, self.add_process, self.calculate_fifo)
        self.process_list_frame = ProcessListFrame(main_frame)
        self.gantt_frame = GanttFrame(main_frame)
        self.times_frame = TimesFrame(main_frame)
        self.button_frame = ButtonFrame(main_frame, self.clear_all, root.destroy)
    
    def add_process(self):
        """Añade un proceso a la lista desde los campos de entrada"""
        process_data = self.input_frame.get_process_data()
        if process_data:
            self.processes.append(process_data)
            self.process_list_frame.add_process_to_table(process_data)
            self.input_frame.clear_fields()
    
    def calculate_fifo(self):
        """Calcula el algoritmo FIFO con los procesos disponibles"""
        if not self.processes:
            return
        
        results = self.fifo_algorithm.calculate(self.processes)
        self.gantt_frame.generate_chart(results)
        self.times_frame.show_time_table(results)
    
    def clear_all(self):
        """Limpia todos los componentes"""
        self.processes = []
        self.input_frame.clear_fields()
        self.process_list_frame.clear_table()
        self.gantt_frame.clear()
        self.times_frame.clear()