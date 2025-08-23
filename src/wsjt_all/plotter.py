import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import os
from .readall import read_allfile, get_overlapping_sessions
global colorseries

def init_colours():
    global colorseries
    from random import randint
    colorseries = []
    ncolors = 20
    for i in range(ncolors):
        colorseries.append('#%06X' % randint(0x333333, 0xFFFFFF))

def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['t']>= tmin and d['t']<= tmax):
            decs.append(d)
    return decs

def get_session_data(decA, decB, ts, te):
    calls_a = set()
    calls_b = set()
    dA, dB = [], []
    for d in decA:
        if(d['t']>=ts and d['t']<=te):
            calls_a.add(d['oc'])
            dA.append(d)
    print(f"{len(calls_a)} calls in A")
    for d in decB:
        if(d['t']>=ts and d['t']<=te):
            calls_b.add(d['oc'])
            dB.append(d)
    print(f"{len(calls_b)} calls in B")
    calls_ab = calls_a.intersection(calls_b)
    print(f"{len(calls_ab)} calls in both A and B")
    calls_aob = calls_a.union(calls_b)
    print(f"{len(calls_aob)} calls in either A or B")
    
    return calls_a, calls_b, calls_ab, calls_aob, dA, dB


def plot_session_counts(ax, calls, dA, dB):
    global colorseries
    decode_counts_a, decode_counts_b = [], []
    for c in calls:
        decode_counts_a.append(sum(c == da['oc'] for da in dA))  
        decode_counts_b.append(sum(c == db['oc'] for db in dB))
    xplot = [n + 0.2*random.random() for n in decode_counts_a]
    yplot = [n + 0.2*random.random() for n in decode_counts_b]
    cols = colorseries * (1+int(len(xplot)/len(colorseries)))
    ax.scatter(xplot, yplot, c = cols[0: len(xplot)] , marker ="o", alpha = 0.9)
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
    axmax = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.set_xlim(0, axmax)
    ax.set_ylim(0, axmax)
    ax.set_title("Number of decodes of each callsign in the time window above")
    ax.set_xlabel("Number of decodes in all.txt A")
    ax.set_ylabel("Number of decodes in all.txt B")


def plot_session_snrs(ax, calls, dA, dB):
    global colorseries
    for i, c in enumerate(calls):
        series_x = []
        series_y = []
        for da in dA:
            if(da['oc']==c):
                for db in dB:
                    if(db['oc'] == c):
                        if (abs(da['t'] - db['t']) <30):    # coincident reports of same callsign: append SNRs for plot
                            series_x.append(da['rp'])
                            series_y.append(db['rp'])
        if(series_x != []):
            ax.plot(series_x, series_y, color = colorseries[i % len(colorseries)] , marker ="o", alpha = 0.9)
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
    axrng = (min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1]))
    ax.set_xlim(axrng)
    ax.set_ylim(axrng)
    ax.set_title("SNRs for callsigns in both A and B")
    ax.set_xlabel("SNR in all.txt A")
    ax.set_ylabel("SNR in all.txt B")

def get_session_info_string(ts, te, bm):
    tmins = (te-ts)/60
    return(f"{datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M')} {bm} for {tmins} mins")

def list_sessions(sessions):
    for i, s in enumerate(sessions):
        print(f"{i+1} {get_session_info_string(*s)}")

def plot_all_historic(allA, allB, session_guard_seconds, dump_data_with_plots):
    
    alldecA, sA = read_allfile(allA, session_guard_seconds)
    list_sessions(sA)
    alldecB, sB = read_allfile(allB, session_guard_seconds)
    list_sessions(sB)
    sessions = get_overlapping_sessions(sA, sB)
    list_sessions(sessions)
    print("Time windowing decode lists")
    tmin, _, _ = sessions[0]
    _, tmax, _ = sessions[-1]
    decA = time_window_decodes(alldecA, tmin, tmax)
    decB = time_window_decodes(alldecB, tmin, tmax)
    init_colours()

    print("Plotting sessions:")
    for i, sess in enumerate(sessions):
        ts, te, bm = sess
        fig,ax = plt.subplots()

        session_info = get_session_info_string(*sess)        
        calls_a, calls_b, calls_ab, calls_aob, dA, dB = get_session_data(decA, decB, int(ts), int(te))
        plot_session_snrs(ax, calls_aob, dA, dB)
        calls_info = f"Callsigns found: A only, {len(calls_a)-len(calls_ab)}; A&B, {len(calls_ab)}; B only, {len(calls_b)-len(calls_ab)}"

        print(f"\nPlotting session {i+1} of {len(sessions)} {session_info}")
        fig.suptitle(f"{session_info}\n{calls_info}") 
        plt.tight_layout()
        if not os.path.exists("plots"):
            os.makedirs("plots")
        plotfile = session_info+".png"
        print(f"Saving plot plots/{plotfile}")
        plt.savefig(f"plots/{plotfile}")
        plt.close()

def plot_live(allA, allB, plot_window_seconds):

    import time
    fig,ax = plt.subplots()
    plt.ion()
    init_colours()
    while(True):
        session_guard_seconds = 0
        decA, sA = read_allfile(allA, session_guard_seconds)
        decB, sB = read_allfile(allB, session_guard_seconds)
        if(sA[-1][2] != sB[-1][2]):
            print(f"Band/modes don't match ({sA[-1][2]} vs {sB[-1][2]})")
        tmax = max(sA[-1][1], sB[-1][1])
        tmin = tmax - plot_window_seconds
        ax.cla()
        
        session_info = get_session_info_string(tmin, tmax, sA[-1][2])
        calls_a, calls_b, calls_ab, calls_aob, dA, dB = get_session_data(decA, decB, int(tmin), int(tmax))
        plot_session_counts(ax, calls_aob, dA, dB)
        calls_info = f"Callsigns found: A only, {len(calls_a)-len(calls_ab)}; A&B, {len(calls_ab)}; B only, {len(calls_b)-len(calls_ab)}"
        
        fig.suptitle(f"{session_info}\n{calls_info}") 
        plt.tight_layout()
        plt.pause(5)



