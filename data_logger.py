from typing import Callable,Optional,Protocol
from twin_rotor import Twin_Rotor
from abc import ABC,abstractmethod
import csv


class Logger:

    @abstractmethod
    def write(self,str:str):
        ...

    def writeln(self,str:str):
        self.write(f"{str}\n")
    

class Print_Logger(Logger):
    def write(self,str:str):
        print(str,end='')

class File_Logger(Logger):
    def __init__(self,file_path:str,mode:str='w'):
        '''
        file_path : path to file
        mode: 'a' to append or 'w' to overwrite
        '''
        if(mode not in {'a','w'}):
            raise Exception("mode must be either a or w")
        self.file_path = file_path
        self.file = open(self.file_path,mode)

    def write(self,str:str):

        self.file.write(str)

    def __del__(self):
        self.file.close()

    
class Twin_Rotor_Logger(Protocol):

    def log(self,twin_rotor:Twin_Rotor)->None:
        ...

class Simple_Logger(Twin_Rotor_Logger):
    '''
    Can provide any Logging Function by default it logs in human readable format
    t=? encoder1=? encoder2=? acc.x=? acc.y=? acc.z=? gyro.x=? gyro.y=? gyro.z=?
    writes each log entry in newLine
    '''
    def __init__(self,data_logger:Logger,logging_func:Optional[Callable[[Twin_Rotor],str]]=None):
        self.data_logger = data_logger
        self.logging_function = self.basic_logging 
        if(logging_func is not None):
            self.logging_function = logging_func

    @staticmethod
    def basic_logging(twin_rotor:Twin_Rotor):
        return str(twin_rotor)

    def log(self,twin_rotor:Twin_Rotor):
        self.data_logger.writeln(self.logging_function(twin_rotor))



class CSV_Logger(Twin_Rotor_Logger):
    def __init__(self,file_path,append=False):
        mode = 'w' if append else 'a'
        self._file = open(file_path,'w')
        self._writer = csv.writer(self._file)
        header = ['time','encoder1', 'encoder2','acc.x','acc.y','acc.z','gyro.x','gyro.y','gyro.z']
        if(not append):
            self._writer.writerow(header)

    def __del__(self):
        self._file.close()

    def log(self,twin_rotor:Twin_Rotor):
        data = [
            twin_rotor.time_of_last_update,
            twin_rotor.encoder.encoder1,
            twin_rotor.encoder.encoder2,
            *twin_rotor.imu.acceleration,
            *twin_rotor.imu.gyro
                ]
        self._writer.writerow(data)




    
        