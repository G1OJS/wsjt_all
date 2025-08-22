import matplotlib.pyplot as plt
import os
from readall import read_allfile, get_overlapping_sessions, get_session_info_string


def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['t']>= tmin and d['t']<= tmax):
            decs.append(d)
    return decs

def plot_session(decA, decB, ts, te, plotfile):
    fig,ax = plt.subplots()
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))

    from random import randint
    colors = []
    ncolors = 20
    for i in range(ncolors):
        colors.append('#%06X' % randint(0, 0xFFFFFF))

    calls = set()
    bandModes = set()
    dA, dB = [], []
    for d in decA:
        if(d['t']>=ts and d['t']<=te):
            calls.add(d['oc'])
            bandModes.add(d['bm'])
            dA.append(d)
    print(f"{len(calls)} callsigns from all A")
    for d in decB:
        if(d['t']>=ts and d['t']<=te):
            calls.add(d['oc'])
            bandModes.add(d['bm'])
            dB.append(d)
    print(f"{len(calls)} callsigns from all A and all B")

    # plotfile = plotfile + " "+ ",".join(list(bandModes))+".png"
    nReports = 0
    for i, c in enumerate(calls):
     #   if(i % 10 ==0):
     #       print(f"At callsign {i} of {len(calls)}: accumulated {nReports} reports")
        series_x = []
        series_y = []
        for da in dA:
            if(da['oc']==c):
                for db in dB:
                    if(db['oc'] == c and abs(da['t'] - db['t']) <30): # coincident reports same callsign
                        series_x.append(da['rp'])
                        series_y.append(db['rp'])
        ax.plot(series_x, series_y, color = colors[i % ncolors], marker ="o")
        nReports += len(series_x)
    if(nReports>0):
        plt.tight_layout()
        if not os.path.exists("plots"):
            os.makedirs("plots")
        print(f"Saving plot plots/{plotfile}")
        plt.savefig(f"plots/{plotfile}")
    plt.close()

allA = r"C:\Users\drala\AppData\Local\WSJT-X\all.txt"
allB = r"C:\Users\drala\AppData\Local\WSJT-X - AltAB\all.txt"

print("Reading all files")
alldecA, sA = read_allfile(allA)
for s in sA:
    print(f"A: {get_session_info_string(s)}")
alldecB, sB = read_allfile(allB)
for s in sB:
    print(f"B: {get_session_info_string(s)}")

print("Finding overlapping sessions")
coinc = get_overlapping_sessions(sA,sB)
for c in coinc:
    print(f"AB: {get_session_info_string(c)}")
    
print("Time windowing decode lists")
tmin, _, _ = coinc[0]
_, tmax, _ = coinc[-1]
decA = time_window_decodes(alldecA, tmin, tmax)
decB = time_window_decodes(alldecB, tmin, tmax)

print("Plotting sessions")
for c in coinc:
    info_str = get_session_info_string(c)
    ts, te, bm = c
    print(f"\nPlotting {info_str}")
    plot_session(decA, decB, int(ts), int(te), f"{info_str}.png")


