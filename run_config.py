from Dualis_Scanner import get_grades
import configparser
import  pickle
from os import path

def run_config():

    # Get Config
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf8")

    for key in config:
        username = config[key]["user"]
        password = config[key]["password"]
        mail = config[key]["mail"]
        filename = key + "_grades.pkl"

        data_new = get_grades(username, password)

        if path.exists(filename):
            pkl_file = open(filename, 'rb')
            data_old = pickle.load(pkl_file)
            pkl_file.close()

            if data_new != data_old:
                #Mail mit neuen Noten
                output = open(filename, 'wb')
                pickle.dump(data_new, output)
                output.close()

        else:
            pass
            #Willkommensmail





if __name__ == "__main__":
    run_config()