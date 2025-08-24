import configparser
import os
import datetime
import matplotlib.pyplot as plt
from .plotter import make_chart, save_chart, init_colours
from .load_sessions import load_sessions, load_overlapping_sessions, get_session_info_string

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
            txt += "\nlive_plot_window_seconds = 300\n"
            with open("wsjt_all.ini","w") as f:
              f.write(txt)
            print("A wsjt_all.ini file has been created, but please edit the paths to point to the two ALL.txt files you want to compare.")
        print("Exiting program")

def plot_all_historic(allfilepath_A, allfilepath_B, session_guard_seconds, dump_data_with_plots):
    sessions_AB, decodes_A, decodes_B = load_overlapping_sessions(allfilepath_A, allfilepath_B, session_guard_seconds)
    init_colours()
    print("Plotting sessions:")
    for session_info in sessions_AB:
        session_info_string = get_session_info_string(session_info)
        fig, axs = plt.subplots(2,1, figsize=(6, 8))
        make_chart(plt, fig, axs, decodes_A, decodes_B, session_info)
        save_chart(plt, session_info_string+".png")
        plt.close()

def plot_live(allfilepath_A, allfilepath_B, plot_window_seconds):
    fig, axs = plt.subplots(2,1, figsize=(6, 8))
    plt.ion()
    init_colours()
    print("Waiting for live session data from both ALL files")
    while(True):
        session_guard_seconds = 0
        t_recent = datetime.datetime.now().timestamp() - plot_window_seconds * 3 # allow for delay in receiving live spots
        decodes_A, sessions_A = load_sessions(allfilepath_A, session_guard_seconds, skip_all_before = t_recent)
        decodes_B, sessions_B = load_sessions(allfilepath_B, session_guard_seconds, skip_all_before = t_recent)
        if(len(sessions_A)>0 and len(sessions_B)>0):
            if(sessions_A[-1][2] != sessions_B[-1][2]):
                print(f"Band/modes don't match ({sessions_A[-1][2]} vs {sessions_B[-1][2]})")
            te = max(sessions_A[-1][1], sessions_B[-1][1])
            ts = te - plot_window_seconds
            bm = sessions_A[-1][2]
            session_info=(ts,te,bm)
            axs[0].cla(), axs[1].cla()
            make_chart(plt, fig, axs, decodes_A, decodes_B, session_info)
            plt.pause(5)

def run(option):
    if(check_config()):
        config = configparser.ConfigParser()
        config.read("wsjt_all.ini")
        allfilepath_A, allfilepath_B = config.get("inputs","allA"), config.get("inputs","allB")    
        session_guard_seconds = int(config.get("settings","session_guard_seconds"))
        dump_data_with_plots = config.get("settings","dump_data_with_plots")
        live_plot_window_seconds = int(config.get("settings","live_plot_window_seconds"))
        if(option=="hist"):
            plot_all_historic(allfilepath_A, allfilepath_B, session_guard_seconds, dump_data_with_plots)
        else:
            plot_live(allfilepath_A, allfilepath_B, live_plot_window_seconds)

def wsjt_all_ab():
    run("hist")

def wsjt_all_ab_live():
    run("live")        
