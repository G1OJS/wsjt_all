import configparser
import os
from .plotter_dual import plot_all_historic_dual, plot_live_dual
from .plotter_single import plot_all_historic_single, plot_live_single

def check_config():
    if(os.path.exists("wsjt_all.ini")):
        return True
    else:
        print("No wsjt_all.ini in current directory.")
        user_input = input("Create one? (yes/no): ")
        if user_input.lower() in ["yes", "y"]:
            txt = "[inputs]\nallA = please edit this path to WSJT-X all.txt"
            txt += "\nallB = please edit this path to secondary WSJT-X all.txt"
            txt += "\n\n[settings]"
            txt += "\nsession_guard_seconds = 300"
            txt += "\nlive_plot_window_seconds = 300"
            txt += "\nshow_best_snrs_only = N"
            txt += "\nuse_bandmode_folders = Y"
            txt += "\n"
            with open("wsjt_all.ini","w") as f:
              f.write(txt)
            print("A wsjt_all.ini file has been created, but please edit the paths to point to the two ALL.txt files you want to compare.")
        print("Exiting program")

def run(option):
    if(check_config()):
        config = configparser.ConfigParser()
        config.read("wsjt_all.ini")
        allfilepath_A, allfilepath_B = config.get("inputs","allA"), config.get("inputs","allB")    
        session_guard_seconds = int(config.get("settings","session_guard_seconds"))
        live_plot_window_seconds = int(config.get("settings","live_plot_window_seconds"))
        show_best_snrs_only = (config.get("settings","show_best_snrs_only") == "Y")
        use_bandmode_folders = (config.get("settings","use_bandmode_folders") == "Y")

        if(option=="hist_single"):
            plot_all_historic_single(allfilepath_A, "A/", session_guard_seconds, use_bandmode_folders)
            if(allfilepath_A != allfilepath_B):
                plot_all_historic_single(allfilepath_B, "B/", session_guard_seconds, use_bandmode_folders)
        if(option=="live_single"):
            plot_live_single(allfilepath_A,session_guard_seconds, live_plot_window_seconds)

        if(option=="hist_ab"):
            allfilepath_B = config.get("inputs","allB")    
            if(allfilepath_A == allfilepath_B):
                print("AB analysis requires two different all.txt files")
            else:
                plot_all_historic_dual(allfilepath_A, allfilepath_B, "AB/", session_guard_seconds, show_best_snrs_only, use_bandmode_folders)
        if(option=="live_ab"):
            allfilepath_B = config.get("inputs","allB")    
            if(allfilepath_A == allfilepath_B):
                print("AB analysis requires two different all.txt files")
            else:
                plot_live_dual(allfilepath_A, allfilepath_B, session_guard_seconds, live_plot_window_seconds, show_best_snrs_only)
            

def wsjt_all():
    run("hist_single")

def wsjt_all_live():
    run("live_single") 

def wsjt_all_ab():
    run("hist_ab")

def wsjt_all_ab_live():
    run("live_ab")        

     
