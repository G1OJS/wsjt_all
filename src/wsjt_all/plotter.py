import matplotlib.pyplot as plt
import random
import os
from .load_sessions import get_session_info_string
global colourseries

def init_colours():
    global colourseries
    from random import randint
    colourseries = []
    ncolors = 20
    for i in range(ncolors):
        colourseries.append('#%06X' % randint(0x333333, 0xFFFFFF))

def save_chart(plt, plotfile):
    if not os.path.exists("plots"):
        os.makedirs("plots")
    print(f"Saving plot plots/{plotfile}")
    plt.savefig(f"plots/{plotfile}")

def dither(vals, amplitude_factor):
    amplitude = amplitude_factor * (max(vals) - min(vals))
    return [v + amplitude*random.random()  for v in vals]

def plot_counts(ax, calls, decodes_A, decodes_B):
    global colourseries
    decode_counts_A, decode_counts_B = [], []
    for c in calls:
        decode_counts_A.append(sum(c == da['oc'] for da in decodes_A))  
        decode_counts_B.append(sum(c == db['oc'] for db in decodes_B))
    xplot = dither(decode_counts_A, 0.01)
    yplot = dither(decode_counts_B, 0.01)
    cols = colourseries * (1+int(len(xplot)/len(colourseries)))
    ax.scatter(xplot, yplot, c = cols[0: len(xplot)] , marker ="o", alpha = 0.9)
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
    axmax = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.set_xlim(0, axmax)
    ax.set_ylim(0, axmax)
    ax.set_title("Number of decodes per callsign")
    ax.set_xlabel("Number of decodes in all.txt A")
    ax.set_ylabel("Number of decodes in all.txt B")

def plot_snrs(ax, calls, decodes_A, decodes_B, show_best_snrs_only):
    global colourseries
    for i, c in enumerate(calls):
        series_x = []
        series_y = []
        for da in decodes_A:
            if(da['oc']==c):
                for db in decodes_B:
                    if(db['oc'] == c):
                        if (abs(da['t'] - db['t']) <30):    # coincident reports of same callsign: append SNRs for plot
                            series_x.append(da['rp'])
                            series_y.append(db['rp'])
        if(series_x != []):
            if(show_best_snrs_only):
                series_x = [max(series_x)]
                series_y = [max(series_y)]
            ax.plot(series_x, series_y, color = colourseries[i % len(colourseries)] , marker ="o", alpha = 0.9)
    ax.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
    axrng = (min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1]))
    ax.set_xlim(axrng)
    ax.set_ylim(axrng)
    ax.set_title("SNR of simultaneous decodes")
    ax.set_xlabel("SNR in all.txt A")
    ax.set_ylabel("SNR in all.txt B")

def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['t']>= tmin and d['t']<= tmax):
            decs.append(d)
    return decs

def get_callsigns(decodes):
    callsigns = set()
    for d in decodes:
            callsigns.add(d['oc'])
    return callsigns

def venn(ax, ns):
    x1 = ns[0]/sum(ns)
    x2 = (sum(ns)-ns[2])/sum(ns)
    ax.set_axis_off()
    ax.add_patch(plt.Rectangle((0,0), x1,1, color = 'green', alpha = 0.3))
    ax.add_patch(plt.Rectangle((x1,0), x2-x1,1, color = 'yellow', alpha = 0.3))
    ax.add_patch(plt.Rectangle((x2,0),1-x2,1, color = 'red', alpha = 0.3))
    ax.text(x1/2,0.5, f'A {ns[0]}', horizontalalignment='center',verticalalignment='center')
    ax.text(x1+(x2-x1)/2,0.5, f'AB {ns[1]}', horizontalalignment='center',verticalalignment='center')
    ax.text(0.5+x2/2,0.5, f'B {ns[2]}', horizontalalignment='center',verticalalignment='center')
    ax.set_title("Number of callsigns in A only, A&B, B only")

def make_chart(plt, fig, axs, decodes_A, decodes_B, session_info, show_best_snrs_only = False):
    decs_A = time_window_decodes(decodes_A, session_info[0], session_info[1])
    decs_B = time_window_decodes(decodes_B, session_info[0], session_info[1])
    calls_a= get_callsigns(decs_A)
    calls_b= get_callsigns(decs_B)
    calls_ab = calls_a.intersection(calls_b)
    calls_aob = calls_a.union(calls_b)
    session_info_string = get_session_info_string(session_info)
    venn(axs[0], [len(calls_a)-len(calls_ab), len(calls_ab), len(calls_b)-len(calls_ab)])
    plot_counts(axs[1], calls_aob, decs_A, decs_B)
    plot_snrs(axs[2], calls_aob, decs_A, decs_B, show_best_snrs_only)
    fig.suptitle(f"Session: {session_info_string}") 
    plt.tight_layout()
       


