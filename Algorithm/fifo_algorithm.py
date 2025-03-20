class FIFOAlgorithm:
    """Implementación del algoritmo de planificación FIFO (First-In, First-Out)"""
    
    def calculate(self, processes):
        """
        Calcula los tiempos de los procesos utilizando el algoritmo FIFO
        
        Args:
            processes (list): Lista de diccionarios con datos de procesos
                              Cada diccionario debe tener 'name', 'burst' y 'arrival'
        
        Returns:
            list: Lista de diccionarios con los resultados de cada proceso
        """
        if not processes:
            return []
        
        # Ordenar procesos por tiempo de llegada (FIFO)
        sorted_processes = sorted(processes, key=lambda x: x['arrival'])
        
        current_time = 0
        results = []
        
        # Calcular tiempos para cada proceso
        for process in sorted_processes:
            if current_time < process['arrival']:
                current_time = process['arrival']
            
            start_time = current_time
            current_time += process['burst']
            completion_time = current_time
            
            # Calcular tiempos adicionales
            turnaround_time = completion_time - process['arrival']
            waiting_time = turnaround_time - process['burst']
            
            results.append({
                'name': process['name'], 
                'start': start_time, 
                'burst': process['burst'], 
                'arrival': process['arrival'],
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
        
        return results