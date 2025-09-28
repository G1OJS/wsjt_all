import snapshot_data
import matplotlib.pyplot as plt


def plot_counts_diff(ax, calls, decodes_A, decodes_B):
    diffs = dict()
    for c in calls:
        decode_counts_A = sum(c == da['oc'] for da in decodes_A)
        decode_counts_B = sum(c == db['oc'] for db in decodes_B)
        diffs[c] = {'diff':decode_counts_A - decode_counts_B, 'sA':decodes_A[c]['rp'], 'sB':decodes_B[c]['rp']}
    dd2 = dict(sorted(diffs.items(), key=lambda key_val: -key_val[1]))
    xcats = [k for k in dd2.keys()]
    n = [v['n'] for v in dd2.values]
    sa = [v['sA'] for v in dd2.values()]
    ax.plot(xcats,y)
    ax.tick_params("x", rotation=90, labelsize =7)
    ax.set_title("Decodes A - Decodes B")
    ax.set_xlabel("Callsign")
    ax.set_ylabel("Number of decodes")




calls = set()
for d in snapshot_data.decA:
    calls.add(d['oc'])
for d in snapshot_data.decB:
    calls.add(d['oc'])

fig, ax = plt.subplots(1,1, figsize=(12, 9))
plot_counts_diff(ax, calls, snapshot_data.decA, snapshot_data.decB)
plt.show()
