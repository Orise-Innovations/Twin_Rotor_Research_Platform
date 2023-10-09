from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys
from data_buffers import Data_Buffers
import numpy as np
import threading


class Graph_Window(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.encoder1_graph = pg.PlotWidget()
        self.encoder1_graph.setYRange(-400,400)
        self.setLayout(self.main_layout)
        self.encoder1_plot:pg.PlotDataItem = self.encoder1_graph.plot()
        self.main_layout.addWidget(self.encoder1_graph)

    def set_data(self,x_data,y_data):
        self.encoder1_plot.setData(x_data,y_data,autoRange=False)

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self,update_interval:int,data_buffers:Data_Buffers,*args,**kwargs):
        super(Main_Window,self).__init__(*args,**kwargs)
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.graph_window = Graph_Window()
        self.main_layout.addWidget(self.graph_window)
        self.update_timer = QtCore.QTimer()
        self.update_timer.setInterval(update_interval)
        self.update_timer.start()
        self.update_timer.timeout.connect(self.on_graph_update)
        self.data_buffers = data_buffers
        self.on_graph_update()

    def on_graph_update(self):
        self.graph_window.set_data(
            self.data_buffers.time.data,
            self.data_buffers.encoder1.data
        )

def run_app(data_buffers:Data_Buffers):
    app = QtWidgets.QApplication(sys.argv)
    w = Main_Window(10,data_buffers)
    w.show()
    sys.exit(app.exec_())

class Create_Gui:

    def __init__(self,data_buffers:Data_Buffers):
        self.t = threading.Thread(target=run_app,args=(data_buffers,))
        self.t.start()
    
    def __del__(self):
        self.t.join()
    


if __name__ == "__main__":
    data_buffers = Data_Buffers(100)
    gui = Create_Gui(data_buffers)
    while True:
        pass


