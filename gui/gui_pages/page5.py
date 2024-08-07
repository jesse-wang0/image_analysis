import sys
import os
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ttkbootstrap.tableview import Tableview
import ttkbootstrap as tb

current_directory = os.path.dirname(sys.path[0])
if current_directory not in sys.path:
    sys.path.append(current_directory)

from generate_graph_cli.generate_graph import read_csv, calculate_acceleration, calculate_velocity

#graph display
class Page5(tk.Frame):
    def __init__(self, parent, control_btns, vid_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.control_btns = control_btns
        tk.Label(self, text="Stage 3: Results", 
                 font='TkDefaultFont 14 bold').pack(pady=20)
        self.setup_table()
        self.setup_graph()
        self.setup_button()
        self.current_graph = None

    def setup_button(self):
        plot_types = ["x Position", "y Position", "x Velocity", "y Velocity", 
                       "x Acceleration", "y Acceleration"]
        self.item_var = tk.StringVar(value=plot_types[0])
        graph_button = tk.OptionMenu(self.table_container, self.item_var, *plot_types, 
                                     command=self.plot_graph)
        graph_button.pack(pady=10)

    def setup_graph(self):
        graph_frame = tk.Frame(self)
        graph_frame.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.fig.tight_layout(pad=2)
        self.canvas.draw()
        test = tk.Frame(graph_frame)
        test.pack(fill=tk.X, padx=(100,50), pady=(40,0))
        toolbar = NavigationToolbar2Tk(self.canvas, test)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def setup_table(self):
        self.table_container = tk.Frame(self)
        self.table_container.pack(side=tk.RIGHT, fill=tk.Y)
        coldata = [
            {"text": "Time (sec)"},
            {"text": "X Position (m)"},
            {"text": "Y Position (m)"},
        ]
        self.table = Tableview(master=self.table_container, coldata=coldata, 
                       paginated=False, searchable=False, bootstyle="primary")
        self.table.config(height=10)
        self.table.pack(side=tk.TOP, padx=(0,10), pady=(50,0))
        
    def add_table_values(self, path):
        self.times = []
        self.x = []
        self.y = []
        self.times, self.x, self.y = read_csv(path)
        rows_to_insert = []
        for i in range(len(self.times)):
            round_time = round(self.times[i], 4)
            round_x = round(self.x[i], 4)
            round_y = round(self.y[i], 4)
            rows_to_insert.append([round_time, round_x, round_y])

        self.table.insert_rows('end', rows_to_insert)
        self.table.unload_table_data()
        self.table.load_table_data()
        self.table.autoalign_columns()
        self.table.autofit_columns()
        self.table.sort_column_data(cid=0, sort=0)
        
        self.np_x_coords = np.array(self.x)
        self.np_y_coords = np.array(self.y)
        self.np_times = np.array(self.times)

        self.plot_graph("x Position")
        
    def plot_graph(self, plot_type):
        if plot_type == "x Position":
            x, y = self.np_times, self.np_x_coords
            x_label = 'Time (seconds)'
            y_label ='X Coordinate'
            title = 'X Coordinate vs Time'

        elif plot_type == "y Position":
            x, y = self.np_times, self.np_y_coords
            x_label = 'Time (seconds)'
            y_label = 'Y Coordinate'
            title = 'Y Coordinate vs Time'

        elif plot_type == "x Velocity":
            x_velocity, times = calculate_velocity(self.x, self.times)
            x, y = times, x_velocity
            x_label = 'Time (seconds)'
            y_label = 'X Velocity (m/s)'
            title = 'X Velocity vs Time'

        elif plot_type == "y Velocity":
            y_velocity, times = calculate_velocity(self.y, self.times)
            x, y = times, y_velocity
            x_label = 'Time (seconds)'
            y_label = 'Y Velocity (m/s)'
            title = 'Y Velocity vs Time'

        elif plot_type == "x Acceleration":
            x_acceleration, times = calculate_acceleration(self.x, self.times)
            x, y = times, x_acceleration
            x_label = 'Time (seconds)'
            y_label = 'X Acceleration (m$^2$/s)'
            title = 'X Acceleration vs Time'
            
        elif plot_type == "y Acceleration":
            y_acceleration, times = calculate_acceleration(self.y, self.times)
            x, y = times, y_acceleration
            x_label = 'Time (seconds)'
            y_label = 'Y Acceleration (m$^2$/s)'
            title = 'Y Acceleration vs Time'

        self.ax.clear()
        self.plot = self.ax.scatter(x, y, color='blue', marker='+', label=title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True, which='both', linestyle='--')
        self.ax.axhline(0, color='black', linewidth=1.25)
        self.ax.axvline(0, color='black', linewidth=1.25)
        self.canvas.draw()

        self.annotation = self.ax.annotate(
            text='',
            xy=(0,0),
            xytext=(-50,20),
            textcoords='offset points',
            bbox={'boxstyle': 'round', 'fc': 'w'},
            arrowprops={'arrowstyle': '->'}
        )
        self.annotation.set_visible(False)

        self.fig.canvas.mpl_connect('motion_notify_event', self.detect_point)
        
    def detect_point(self, event):
        annotation_visibility = self.annotation.get_visible()
        if event.inaxes == self.ax:
            is_point, annotation_index = self.plot.contains(event)
            if is_point:
                point_location = self.plot.get_offsets()[annotation_index['ind'][0]]
                self.annotation.xy = point_location
                text_label = f"({round(point_location[0], 4)}, {round(point_location[1], 4)})" 
                self.annotation.set_text(text_label)
                self.annotation.set_alpha(0.8)
                self.annotation.set_visible(True)
                self.canvas.draw_idle()
            else:
                if annotation_visibility:
                    self.annotation.set_visible(False)
                    self.canvas.draw_idle()

    def can_next(self):
        return False