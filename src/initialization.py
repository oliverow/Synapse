import tkinter as tk
import subprocess
import os

class initialization_app(tk.Tk):
    def __init__(self, config_obj, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.config_obj = config_obj

        # config app
        self.minsize(640, 480)

        # building main container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_rowconfigure(3, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        warning_label = tk.Label(container, text = "Please enter Neo4j instance path below")
        warning_label.grid(row = 0, column = 0)
        self.path_input = tk.Entry(container)
        self.path_input.grid(row = 1, column = 0)
        add_button = tk.Button(container, text = "Check", command = self.write_new_path)
        add_button.grid(row = 2, column = 0)
        self.status_var = tk.StringVar()
        status_label = tk.Label(container, textvariable = self.status_var)
        status_label.grid(row = 3, column = 0)

    def write_new_path(self):
        self.config_obj['neo4j_path'] = self.path_input.get()
        self.check_complete()

    def check_complete(self):
        db_path = self.config_obj['neo4j_path']
        if os.path.exists(db_path):
            try:
                start_result = subprocess.check_output('cd \"{}\"; ./neo4j start'.format(os.path.normpath(db_path)), stderr=subprocess.STDOUT, shell = True) # (['cd', self.config_obj['neo4j_path']])
            except subprocess.CalledProcessError as err:
                start_result = err.output
            self.status_var.set(start_result.decode('utf-8'))
            status = subprocess.check_output('cd \"{}\"; ./neo4j status'.format(os.path.normpath(db_path)), stderr=subprocess.STDOUT, shell = True).decode('utf-8')
            if status.startswith('Neo4j is running'):
                self.destroy()
                return True
        return False
