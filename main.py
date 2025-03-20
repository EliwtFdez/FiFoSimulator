import tkinter as tk

from scheduler.scheduler_app import FIFOSchedulerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FIFOSchedulerApp(root)
    root.mainloop()