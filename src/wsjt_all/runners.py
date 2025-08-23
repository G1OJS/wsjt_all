import configparser
import os
from .plotter import plot_all_historic, plot_live


def check_config():
    if(not os.path.exists("wsjt_all.ini")):
        print("No wsjt_all.ini in current directory.")
        user_input = input("Create one? (yes/no): ")
        if user_input.lower() in ["yes", "y"]:
            txt = "[inputs]\nallA = please edit this path to WSJT-X all.txt"
            txt += "\nallB = please edit this path to secondary WSJT-X all.txt"
            txt += "\n\n[settings]"
            txt += "\nsession_guard_seconds = 300"
            txt += "\nlive_plot_window_seconds = 300\n"
            with open("wsjt_all.ini","w") as f:
              f.write(txt)
            print("A wsjt_all.ini file has been created, but please edit the paths to point to the two ALL.txt files you want to compare.")
            print("Exiting program")    
        else:
            print("Exiting program")
        return False
    else:
        return True     

def wsjt_all_ab():
    if(check_config()):
        config = configparser.ConfigParser()
        config.read("wsjt_all.ini")
        allA = config.get("inputs","allA")
        allB = config.get("inputs","allB")
        session_guard_seconds = int(config.get("settings","session_guard_seconds"))
        dump_data_with_plots = config.get("settings","dump_data_with_plots")
        plot_all_historic(allA, allB, session_guard_seconds, dump_data_with_plots)


def wsjt_all_ab_live():
    if(check_config()):
        config = configparser.ConfigParser()
        config.read("wsjt_all.ini")
        allA = config.get("inputs","allA")
        allB = config.get("inputs","allB")
        live_plot_window_seconds = int(config.get("settings","live_plot_window_seconds"))
        plot_live(allA, allB, live_plot_window_seconds)
