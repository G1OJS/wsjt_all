import matplotlib.pyplot as plt
import os
from .load_sessions import load_sessions, load_overlapping_sessions, get_session_info_string, time_window_decodes
from .utils import *
import datetime

def make_chart_single(plt, fig, axs, decodes_A, session_info):
    decs_A = time_window_decodes(decodes_A, session_info[0], session_info[1])
    session_info_string = get_session_info_string(session_info)
        
    print("Plotting number of reports")
    timerange_mins = int((session_info[1] - session_info[0]) / 60)
    numbs = [0] * timerange_mins
    call_rpts = {}
    for d in decodes_A:
        t = d['t'] - session_info[0]
        if(t>=0 and t < 60*timerange_mins):
            call_rpts.setdefault(d['oc'],[]).append({'t':t, 'rp':d['rp']})
            tmins = int(t/60)
            numbs[tmins] += 1
    xc = [x + 0.5 for x in range(0,timerange_mins)] # marker at centre of minute bin
    axs[0].plot(xc, numbs, marker = 'o', alpha = 0.9, lw = 0.5)

    axs[0].set_title("Decode rate")
    axs[0].set_xlabel("Time (mins)")
    axs[0].set_ylabel("Number of decodes per minute")

    print("Plotting snr of reports")
    cols = []
    for i, c in enumerate(call_rpts):
        xc, yc = [], []
        cols.append(hash_color(c, plt.cm.tab20))
        for rpt in call_rpts[c]:
            if(rpt['t']>= 0 and rpt['t']<= 60*timerange_mins):
                xc.append(rpt['t'] / 60)
                yc.append(rpt['rp'])
        axs[1].plot(xc, yc, label = c, marker ="o", color = cols[i], alpha = 0.9, lw = 0.2)

    axs[1].set_title("SNR per callsign")
    axs[1].set_xlabel("Time (mins)")
    axs[1].set_ylabel("SNR per callsign")

    axs[0].set_xlim(0, int((session_info[1]-session_info[0])/60)+.1)
    axs[0].set_ylim(0)
    axs[1].set_xlim(0, int((session_info[1]-session_info[0])/60)+.1)

    fig.suptitle(f"Session: {session_info_string}") 
    plt.tight_layout()

def plot_live_single(allfilepath_A, session_guard_seconds, plot_window_seconds, show_best_snrs_only):
    fig, axs = plt.subplots(2,1, figsize=(6, 9), height_ratios = (1,1))
    plt.ion()
    print("Waiting for live session data")
    while(True):
        t_recent = datetime.datetime.now().timestamp() - plot_window_seconds * 3 # allow for delay in receiving live spots
        decodes_A, sessions_A = load_sessions(allfilepath_A, session_guard_seconds, skip_all_before = t_recent)
        if(len(sessions_A)>0):
            te = sessions_A[-1][1]
            ts = te - plot_window_seconds
            bm = sessions_A[-1][2]
            session_info=(ts,te,bm)
            axs[0].cla(), axs[1].cla()
            make_chart_single(plt, fig, axs, decodes_A, session_info)
            plt.pause(5)

def plot_all_historic_single(allfilepath_A, session_guard_seconds):
    decodes_A, sessions_A = load_sessions(allfilepath_A, session_guard_seconds)
    for i, session_info in enumerate(sessions_A):
        if(session_info[1] > session_info[0] and len(sessions_A)>2):
            session_info_string = get_session_info_string(session_info)
            print(f"Plotting session {i+1} of {len(sessions_A)}: {session_info_string}")
            fig, axs = plt.subplots(2,1, figsize=(6, 9), height_ratios = (1,1))
            make_chart_single(plt, fig, axs, decodes_A, session_info)
            save_chart(plt, session_info_string+"_timeline.png")
            plt.close()
