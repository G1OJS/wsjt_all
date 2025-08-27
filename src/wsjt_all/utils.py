import hashlib
global colourseries
import random
import os

def hash_color(callsign, cmap):
    h = int(hashlib.sha1(callsign.encode()).hexdigest(), 16)
    return cmap(h % cmap.N)

def save_chart(plt, plotfile):
    if not os.path.exists("plots"):
        os.makedirs("plots")
    print(f"Saving plot plots/{plotfile}")
    plt.savefig(f"plots/{plotfile}")

def dither(vals, amplitude_factor):
    amplitude = amplitude_factor * (max(vals) - min(vals))
    return [v + amplitude*random.random()  for v in vals]
