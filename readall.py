
import datetime

def allstr_to_epoch(s):
    dt = datetime.datetime(int("20"+s[0:2]), int(s[2:4]), int(s[4:6]),
                            int(s[7:9]), int(s[9:11]), int(s[11:13]))
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

def todict(line):
    vals = line.strip().split()
    if len(vals) < 9:
        return False
    t = allstr_to_epoch(vals[0])
    return {'t': t, 'ts': vals[0], 'bm':vals[1].split(".")[0]+vals[3], 'oc': vals[8], 'rp': int(vals[4])}

def read_decodes(fp):
    decodes =[]
    for l in open(fp):
        d = todict(l)
        if(d):
            decodes.append(d)
    return(decodes)

def get_sessions(decodes):
    tg = 5*60
    t0=0
    s_idx = []
    for idx, d in enumerate(decodes):
        t1 = d['t']
        if(t1-t0 > tg):
            s_idx.append(idx)
        t0=t1
    s_idx.append(len(decodes)-1)
    sess = []
    for i, idx1 in enumerate(s_idx[0:-2]):
        idx2 = s_idx[i+1]
        sess.append((decodes[idx1]['t'], decodes[idx2]['t'], decodes[idx1]['ts'], decodes[idx2]['ts'], idx1, idx2))
    return sess

def load_allfile(fp):
    decodes = read_decodes(fp)
    sessions = get_sessions(decodes)
    return decodes, sessions

allA = r"C:\Users\drala\AppData\Local\WSJT-X\all.txt"
allB = r"C:\Users\drala\AppData\Local\WSJT-X - AltAB\all.txt"

decA, sessA = load_allfile(allA)
decB, sessB = load_allfile(allB)


print(f"Sessions in {allA}")
for t0,t1, ts0,ts1, i0,i1 in sessA:
    print(f"{ts0} to {ts1}")
print(f"Sessions in {allB}")
for t0,t1, ts0,ts1, i0,i1 in sessB:
    print(f"{ts0} to {ts1}")
