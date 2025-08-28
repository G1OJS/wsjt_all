import hashlib
import random
import os

def hash_color(callsign, cmap):
    h = int(hashlib.sha1(callsign.encode()).hexdigest(), 16)
    return cmap(h % cmap.N)

def save_chart(plt, plotfile, subfolder, session_info, use_bandmode_folders):
    print(use_bandmode_folders)
    folder = f"plots/{session_info[2].replace('-','/')}/{subfolder}" if(use_bandmode_folders) else "plots"
    if not os.path.exists(folder):
        os.makedirs(folder)
    print(f"Saving {plotfile}")
    plt.savefig(f"{folder}/{plotfile}")

def dither(vals, amplitude_factor):
    amplitude = amplitude_factor * (max(vals) - min(vals))
    return [v + amplitude*random.random() if (v>0) else 0 for v in vals]
