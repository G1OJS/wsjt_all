
import matplotlib.pyplot as plt
import os
from .readall import read_allfile, get_overlapping_sessions, get_session_info_string

def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['t']>= tmin and d['t']<= tmax):
            decs.append(d)
    return decs

def plot_session(ax, decA, decB, ts, te, bm):
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))

    # need to move this so it doesn't initialise each plot - global or __init__ if making a class
    from random import randint
    colorseries = []
    ncolors = 20
    for i in range(ncolors):
        colorseries.append('#%06X' % randint(0, 0xFFFFFF))

    calls_a = set()
    calls_b = set()
    bandModes = set()
    dA, dB = [], []
    for d in decA:
        if(d['t']>=ts and d['t']<=te):
            calls_a.add(d['oc'])
            bandModes.add(d['bm'])
            dA.append(d)
    a_info=f"{len(calls_a)} calls in A"
    print(a_info)
    for d in decB:
        if(d['t']>=ts and d['t']<=te):
            calls_b.add(d['oc'])
            bandModes.add(d['bm'])
            dB.append(d)
    b_info=f"{len(calls_b)} calls in B"
    print(b_info)
    calls = calls_a.intersection(calls_b)
    ab_info=f"{len(calls)} calls in both A and B"
    print(ab_info)

    for i, c in enumerate(calls):
        series_x = []
        series_y = []
        colors=[]
        for da in dA:
            if(da['oc']==c):
                for db in dB:
                    if(db['oc'] == c and abs(da['t'] - db['t']) <30): # coincident reports same callsign
                        series_x.append(da['rp'])
                        series_y.append(db['rp'])
        
        ax.plot(series_x, series_y, c = colorseries[i % ncolors] , marker ="o")
    axrng = (min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1]))
    ax.set_xlim(axrng)
    ax.set_ylim(axrng)
    info = f"Callsigns found: A only, {len(calls_a)-len(calls)}; A&B, {len(calls)}; B only, {len(calls_b)}"
    ax.set_title("SNRs for callsigns in both A and B")
    ax.set_xlabel("SNR in all A")
    ax.set_ylabel("SNR in all B")

    return info


def plot_all_historic(allA, allB, session_guard_seconds):
    print(f"Reading All A: from {allA}")
    print("Sessions found:")
    alldecA, sA = read_allfile(allA, session_guard_seconds)
    for i, s in enumerate(sA):
        print(f"{i+1} {get_session_info_string(s)}")
    print(f"Reading All B: from {allB}")
    print("Sessions found:")
    alldecB, sB = read_allfile(allB, session_guard_seconds)
    for i, s in enumerate(sB):
        print(f"{i+1} {get_session_info_string(s)}")

    print("Finding overlapping sessions:")
    coinc = get_overlapping_sessions(sA, sB)
    for i, c in enumerate(coinc):
        print(f"{i+1} {get_session_info_string(c)}")
        
    print("Time windowing decode lists")
    tmin, _, _ = coinc[0]
    _, tmax, _ = coinc[-1]
    decA = time_window_decodes(alldecA, tmin, tmax)
    decB = time_window_decodes(alldecB, tmin, tmax)

    print("Plotting sessions:")
    for i, c in enumerate(coinc):
        session_info = get_session_info_string(c)
        ts, te, bm = c
        print(f"\nPlotting session {i+1} of {len(coinc)} {session_info}")
        fig,ax = plt.subplots()
        calls_info = plot_session(ax, decA, decB, int(ts), int(te), bm)
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
    while(True):
        session_guard_seconds = 0
        decA, sA = read_allfile(allA, session_guard_seconds)
        decB, sB = read_allfile(allB, session_guard_seconds)
        if(sA[-1][2] != sB[-1][2]):
            print(f"Band/modes don't match ({sA[-1][2]} vs {sB[-1][2]})")
        tmax = max(sA[-1][1], sB[-1][1])
        tmax = time.time()
        tmin = tmax - plot_window_seconds
        ax.cla()
        session_info = get_session_info_string(sA[-1])
        calls_info = plot_session(ax, decA, decB, int(tmin), int(tmax), sB[-1][2])
        fig.suptitle(f"{session_info}\n{calls_info}") 
        plt.tight_layout()
        plt.pause(5)



