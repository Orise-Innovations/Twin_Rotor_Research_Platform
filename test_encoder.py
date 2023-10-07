import serial
from encoder import Encoder
from time import time,sleep

def main():
    ser = serial.Serial('/dev/ttyS0',9600,timeout=1)
    e = Encoder(ser)
    while True:
        data = e.get_data()
        if(data is not None):
            break
        print("STM32 Not Ready yet")
        sleep(1)
    t = time()
    while True:
        print(e.get_data())
    print(time()-t)


if __name__ == "__main__":
    main()
