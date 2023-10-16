
from Orise_Twin_Rotor import Twin_Rotor
from time import sleep


def main():
    sleep(1)
    t = Twin_Rotor()
    sleep(2)
    t.motors.stop()
    sleep(3)
    print("Done")


if __name__ == "__main__":
    main()
