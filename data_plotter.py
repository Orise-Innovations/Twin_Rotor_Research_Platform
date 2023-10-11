from PyQt5 import QtWidgets, QtCore,QtGui
import pyqtgraph as pg
import sys
from data_buffers import Data_Buffers
import numpy as np
import threading
from collections import defaultdict
from typing import Dict,Iterable,List,Callable,Optional

class Colors:
    ORISE_YELLOW  = (251,170,29)
    ORISE_ORANGE  = (242,107,36)
    WHITE = (255,255,255)

class READING_NAMES:
    ENCODER1 = "encoder1"
    ACC_X  = "acc_x"
    ACC_Y ="acc_y"
    ACC_Z = "acc_z"
    GYRO_X = "gyro_x"
    GYRO_Y = "gyro_y"
    GYRO_Z = "gyro_z"
    MAG_X = "mag_x"
    MAG_Y = "mag_y"
    MAG_Z = "mag_z"


Buffer_Data_Func = Callable[[Data_Buffers],Iterable[float]]
class Graph_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        


        self.plot_widgets:List[pg.PlotWidget] = []
        self.setLayout(self.main_layout)
        self.plots:List[pg.PlotDataItem] = []
        self.update_functions:List[Buffer_Data_Func] = []

    def add_time_graph(self,title:str,*buffer_data_func:Buffer_Data_Func,colors,names):
        # print(f"{buffer_data_func=}")
        self.plot_widgets.append(pg.PlotWidget())
        self.plot_widgets[-1].getPlotItem().showGrid(True,True)#type:ignore
        self.plot_widgets[-1].getPlotItem().setTitle(title,color=Colors.WHITE) #type:ignore
        legend = self.plot_widgets[-1].getPlotItem().addLegend(labelTextColor=Colors.WHITE) #type:ignore
        for func,color,name in zip(buffer_data_func,colors,names):
            # print(f"{func=}")
            self.plots.append(self.plot_widgets[-1].plot(pen=pg.mkPen(color=color)))
            if(name is not None):
                legend.addItem(self.plots[-1],name)
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
        self.time_graphs = defaultdict(lambda : [])
    def start(self):
        self.t.start()
    def add_time_graph(self,title:str,buffer_data_func:Buffer_Data_Func,color=Colors.ORISE_YELLOW,name:Optional[str]=None):
        self.time_graphs[title].append((buffer_data_func,color,name))

    def add_twin_rotor_data(self,title:str,reading_name:str,color=Colors.ORISE_YELLOW,name:Optional[str]=None):
        if(not hasattr(self.data_buffers,reading_name)):
            print("Reading name is invalid -- ignoring the plot")
            return
        self.add_time_graph(title,lambda x: getattr(x,reading_name).data,color,name)


    
    @property
    def active(self):
        return self.t.is_alive()

    def __del__(self):
        # print("Joining")
        self.t.join()

    def __run(self):
        app = QtWidgets.QApplication(sys.argv)
        w = Main_Window(50,self.data_buffers)
        for title in self.time_graphs:
            # print(f"{graphs=}")
            graphs,colors,names = tuple(a[0] for a in self.time_graphs[title]),tuple(a[1] for a in self.time_graphs[title]),tuple(a[2] for a in self.time_graphs[title])
            w.graph_window.add_time_graph(title,*graphs,colors=colors,names=names)
        w.show()
        app.exec()
        w.update_timer.stop()
    
    


if __name__ == "__main__":
    data_buffers = Data_Buffers(100)
    run_app(data_buffers)
    # gui = Create_Gui(data_buffers)
    # while True:
    #     pass


