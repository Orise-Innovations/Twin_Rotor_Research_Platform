from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys
from data_buffers import Data_Buffers
import numpy as np
import threading
from typing import Dict,Iterable,List,Callable


Buffer_Data_Func = Callable[[Data_Buffers],Iterable[float]]
class Graph_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        


        self.plot_widgets:List[pg.PlotWidget] = []
        self.setLayout(self.main_layout)
        self.plots:List[pg.PlotDataItem] = []
        self.update_functions:List[Buffer_Data_Func] = []

    def add_time_graph(self,buffer_data_func:Buffer_Data_Func):
        self.plot_widgets.append(pg.PlotWidget())
        self.plots.append(self.plot_widgets[-1].plot())
        self.plot_widgets[-1].getPlotItem().showGrid(True,True)#type:ignore
        self.update_functions.append(buffer_data_func)
        self.main_layout.addWidget(self.plot_widgets[-1])

        return self.plot_widgets[-1],self.plots[-1]

    def update(self,data_buffer:Data_Buffers):
        for plot,update_function in zip(self.plots,self.update_functions):
            data = update_function(data_buffer)
            plot.setData(data_buffer.time.data,data)
        

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self,update_interval:int,data_buffers:Data_Buffers,*args,**kwargs):
        super(Main_Window,self).__init__(*args,**kwargs)
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.graph_window = Graph_Window()
        self.update_timer = QtCore.QTimer()
        self.update_timer.setInterval(update_interval)
        self.update_timer.start()
        self.update_timer.timeout.connect(self.on_graph_update)
        self.main_layout.addWidget(self.graph_window)

        self.data_buffers = data_buffers
        self.on_graph_update()

    def on_graph_update(self):
        self.data_buffers.lock.acquire()
        self.graph_window.update(self.data_buffers)
        self.data_buffers.lock.release()


def run_app(data_buffers:Data_Buffers):
    app = QtWidgets.QApplication(sys.argv)
    w = Main_Window(10,data_buffers)
    w.show()
    # app.exec_()


class Create_Gui:

    def __init__(self,data_buffers:Data_Buffers):
        self.w = None
        self.data_buffers = data_buffers
        self.t = threading.Thread(target=self.__run)
        self.time_graphs = []
    def start(self):
        self.t.start()
    def add_time_graph(self,buffer_data_func:Buffer_Data_Func):
        self.time_graphs.append(buffer_data_func)

    def __del__(self):
        self.t.join()

    def __run(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.w = Main_Window(50,self.data_buffers)
        for graph in self.time_graphs:
            self.w.graph_window.add_time_graph(graph)
        self.w.show()
        self.app.exec_()
    
    


if __name__ == "__main__":
    data_buffers = Data_Buffers(100)
    run_app(data_buffers)
    # gui = Create_Gui(data_buffers)
    # while True:
    #     pass


