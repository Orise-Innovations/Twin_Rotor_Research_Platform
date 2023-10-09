from data_logger import Simple_Logger,File_Logger,CSV_Logger
from twin_rotor import Twin_Rotor




def test_simple_logger():
    FILE_PATH =  "logging_test/human_readable.txt"
    twin_rotor = Twin_Rotor()
    data_logger = Simple_Logger(File_Logger(FILE_PATH))
    while True:
        print(twin_rotor.update_readings())
        data_logger.log(twin_rotor)
    

def test_csv_logger():
    FILE_PATH =  "logging_test/csv_data_logger.csv"
    twin_rotor = Twin_Rotor()
    data_logger = CSV_Logger(FILE_PATH)
    while True:
        print(twin_rotor.update_readings())
        data_logger.log(twin_rotor)

if __name__ == "__main__":
    # test_simple_logger()
    test_csv_logger()
    