from PyQt5 import QtWidgets, QtCore,QtGui
import pyqtgraph as pg
import sys
from data_buffers import Data_Buffers
import numpy as np
import threading
from typing import Dict,Iterable,List,Callable

class Colors:
    ORISE_YELLOW  = (251,170,29)
    ORISE_ORANGE  = (242,107,36)

Buffer_Data_Func = Callable[[Data_Buffers],Iterable[float]]
class Graph_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        


        self.plot_widgets:List[pg.PlotWidget] = []
        self.setLayout(self.main_layout)
        self.plots:List[pg.PlotDataItem] = []
        self.update_functions:List[Buffer_Data_Func] = []

    def add_time_graph(self,title:str,*buffer_data_func:Buffer_Data_Func,colors=None):
        # print(f"{buffer_data_func=}")
        self.plot_widgets.append(pg.PlotWidget())
        self.plot_widgets[-1].getPlotItem().showGrid(True,True)#type:ignore
        self.plot_widgets[-1].getPlotItem().setTitle(title) #type:ignore
        if(colors is None):
            colors = tuple(Colors.ORISE_ORANGE for _ in range(len(buffer_data_func)))
        assert(len(buffer_data_func) == len(colors))
        for func,color in zip(buffer_data_func,colors):
            # print(f"{func=}")
            self.plots.append(self.plot_widgets[-1].plot(pen=pg.mkPen(color=color)))
            self.update_functions.append(func)
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
        self.setWindowTitle("Orise Twin Rotor")

        self.label = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap("assets/orise_slider.png")
        self.pixmap = self.pixmap.scaled(self.pixmap.width()//4,self.pixmap.height()//4)
        self.label.setPixmap(self.pixmap)
        self.main_layout.addWidget(self.label)

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
        self.data_buffers = data_buffers
        self.t = threading.Thread(target=self.__run)
        self.time_graphs = []
    def start(self):
        self.t.start()
    def add_time_graph(self,title:str,*buffer_data_func:Buffer_Data_Func,colors=None):
        self.time_graphs.append((buffer_data_func,title,colors))
    
    @property
    def active(self):
        return self.t.is_alive()

    def __del__(self):
        # print("Joining")
        self.t.join()

    def __run(self):
        app = QtWidgets.QApplication(sys.argv)
        w = Main_Window(50,self.data_buffers)
        for graphs,title,colors in self.time_graphs:
            # print(f"{graphs=}")
            w.graph_window.add_time_graph(title,*graphs,colors=colors)
        w.show()
        app.exec()
        w.update_timer.stop()
    
    


if __name__ == "__main__":
    data_buffers = Data_Buffers(100)
    run_app(data_buffers)
    # gui = Create_Gui(data_buffers)
    # while True:
    #     pass


