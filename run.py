import matplotlib.pyplot as plt
from readall import read_allfile, get_overlapping_sessions

def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['ts'] in range(int(tmin), int(tmax))):
            decs.append(d)
    return decs

def plot_session(decA, decB, ts, te):
    fig,ax = plt.subplots()
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
   # plt.ion()
    timewin_secs = 7*60

    from random import randint
    colors = []
    ncolors = 20
    for i in range(ncolors):
        colors.append('#%06X' % randint(0, 0xFFFFFF))

    calls = set()
    for d in decA:
        if(d['t'] in range(ts,te)):
            calls.add(d['oc'])
    print(f"{len(calls)} callsigns from all A")
    for d in decB:
        if(d['t'] in range(ts,te)):
            calls.add(d['oc'])
    print(f"{len(calls)} callsigns from all A and all B")

    for i, c in enumerate(calls):
        series_x = []
        series_y = []
        for da in decA:
            if(da['oc']==c):
                for db in decB:
                    if(db['oc'] == c and db['t'] == d['t']): # coincident reports same callsign
                        series_x.append(da['rp'])
                        series_y.append(db['rp'])
                ax.plot(series_x, series_y, color = colors[i % ncolors], marker ="o")
    plt.show()

     
allA = r"C:\Users\drala\AppData\Local\WSJT-X\all.txt"
allB = r"C:\Users\drala\AppData\Local\WSJT-X - AltAB\all.txt"

print("Reading all files")
alldecA, sA = read_allfile(allA)
alldecB, sB = read_allfile(allB)

print("Finding overlapping sessions")
coinc = get_overlapping_sessions(sA,sB)

print("Time windowing decode lists")
tmin, _ = coinc[0]
_, tmax = coinc[-1]
decA = time_window_decodes(alldecA, tmin, tmax)
decB = time_window_decodes(alldecB, tmin, tmax)

print("Plotting sessions")
for c in coinc:
    ts, te = c
    tmins = (te-ts)/60
    if(tmins < 30):
        print(f"Session {tmins} mins from {ts}")
        plot_session(decA, decB, int(ts), int(te))


