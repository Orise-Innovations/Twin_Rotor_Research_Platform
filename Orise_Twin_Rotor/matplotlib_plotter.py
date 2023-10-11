import matplotlib.pyplot as plt
from Orise_Twin_Rotor.data_buffers import Data_Buffers
from typing import Tuple,Callable,Iterable,List,Optional
Buffer_Data_Func = Callable[[Data_Buffers],Iterable[float]]



class Matplotlib_Plotter:
    def __init__(self,data_buffers:Data_Buffers,plot_shape:Tuple[int,int]):
        self.data_buffers =data_buffers
        self.fig,self.axes = plt.subplots(*plot_shape,squeeze=False)
        self.plot_shape = plot_shape
        self.plot_funcs= [[None for _ in range(self.plot_shape[1])] for _ in range(self.plot_shape[0])]

    def add_time_plot(self,plot_func:Buffer_Data_Func,title:str,row:int,column:int):
        self.plot_funcs[row][column] = (title,lambda x: (self.data_buffers.time.data, plot_func(x)))#type:ignore
        self.axes[row][column].set_title(title)

    def draw(self,pause=0.001):
        for row_f,row_p in zip(self.plot_funcs,self.axes):#type:ignore
            for data,axis in zip(row_f,row_p):
                if(data is None):
                    continue
                (title,func) =data
                axis.clear()
                axis.plot(*func(self.data_buffers))
        plt.pause(pause)

    @property
    def figure(self):
        return self.fig

    




    
        
    

