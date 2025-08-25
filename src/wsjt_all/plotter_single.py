import matplotlib.pyplot as plt
import random
import os
from wsjt_all.load_sessions import load_sessions, time_window_decodes,get_session_info_string
global colourseries
import datetime
import mplcursors
import hashlib

def hash_color(callsign, cmap=plt.cm.tab20):
    h = int(hashlib.sha1(callsign.encode()).hexdigest(), 16)
    return cmap(h % cmap.N)

def make_chart_single(plt, fig, axs, decodes_A, session_info):
    decs_A = time_window_decodes(decodes_A, session_info[0], session_info[1])
    session_info_string = get_session_info_string(session_info)
        
    print("Plotting number of reports")
    timerange_mins = int((session_info[1] - session_info[0]) / 60)
    numbs = [0] * timerange_mins
    call_rpts = {}
    for d in decodes_A:
        call_rpts.setdefault(d['oc'],[]).append({'t':d['t'], 'rp':d['rp']})
        tmins = int((int(d['t']) - session_info[0])/60)
        if(tmins>=0 and tmins < timerange_mins):
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
        cols.append(hash_color(c))
        for rpt in call_rpts[c]:
            if(rpt['t']>= session_info[0] and rpt['t']<= session_info[1]):
                xc.append((rpt['t'] - session_info[0]) / 60)
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


