
from data_buffers import Data_Buffers
from twin_rotor import Twin_Rotor
from data_plotter import Create_Gui

def main():
    twin_rotor = Twin_Rotor()
    data_buffers = Data_Buffers(1000)
    gui_application = Create_Gui(data_buffers)
    while True:
        print(twin_rotor.update_readings())
        data_buffers.update_buffers(twin_rotor)


if __name__ == "__main__":
    main()
