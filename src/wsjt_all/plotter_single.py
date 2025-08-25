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

    call_rpts = {}
    for d in decodes_A:
        call_rpts.setdefault(d['oc'],[]).append({'t':d['t'], 'rp':d['rp']})

    if(session_info[1]-session_info[0] < 1000):
        print("number of reports")
        times = range(session_info[0],session_info[1]+1)
        numbs = []
        for t in times:
            print(f"{(t-session_info[0])/(session_info[1]-session_info[0]):.0%}")
            numbs.append(0)
            for c in call_rpts:
                if(t in [rpt['t'] for rpt in call_rpts[c]]):
                    numbs[-1]+=1
        axs[0].bar(times, numbs, alpha = 0.9)
        axs[0].set_title("Number of decodes")
        axs[0].set_xlabel("Time")
        axs[0].set_ylabel("Number of decodes")


    print("snr of reports")
    cols = []
    for i, c in enumerate(call_rpts):
        xc, yc = [], []
        cols.append(hash_color(c))
        for rpt in call_rpts[c]:
            if(rpt['t']>= session_info[0] and rpt['t']<= session_info[1]):
                xc.append(rpt['t'])
                yc.append(rpt['rp'])
        axs[1].plot(xc, yc, label = c, marker ="o", color = cols[i], alpha = 0.9)
    mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
    axs[1].set_title("SNR per callsign")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("SNR per callsign")

    axs[0].set_xlim(session_info[0],session_info[1]+1)
    axs[1].set_xlim(session_info[0],session_info[1]+1)

    fig.suptitle(f"Session: {session_info_string}") 
    plt.tight_layout()


