
import datetime

def get_session_info_string(sess):
    ts, te, bm = sess
    tmins = (te-ts)/60
    return(f"{datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M')} {bm} for {tmins} mins")

def allstr_to_epoch(s):
    dt = datetime.datetime(int("20"+s[0:2]), int(s[2:4]), int(s[4:6]),
                            int(s[7:9]), int(s[9:11]), int(s[11:13]))
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

def todict(line):
    vals = line.strip().split()
    if len(vals) < 9:
        return False
    t = allstr_to_epoch(vals[0])
    return {'t': int(t), 'ts': vals[0], 'bm':vals[1].split(".")[0]+vals[3], 'oc': vals[8], 'rp': int(vals[4])}

def get_decodes(fp):
    decodes =[]
    for l in open(fp):
        d = todict(l)
        if(d):
            decodes.append(d)
    return(decodes)

def get_single_file_sessions(decodes, session_split_guard_secs):
    # is this picking up the very last session?
    t0=0
    bm0 = ""
    s_idx = []
    for idx, d in enumerate(decodes):
        t1 = int(d['t'])
        if(t1-t0 > session_split_guard_secs or d['bm'] != bm0): # new session
            s_idx.append([idx, idx-1])
        t0=t1
        bm0 = d['bm']
    s_idx.append([None, len(decodes)-1])
    sess = []
    for i, idx in enumerate(s_idx[0:-1]):
        idxs = s_idx[i][0]
        idxe = s_idx[i+1][1]
        sess.append((int(decodes[idxs]['t']), int(decodes[idxe]['t']), decodes[idxs]['bm']))
    return sess

def read_allfile(fp, session_split_guard_secs):
    decodes = get_decodes(fp)
    sessions = get_single_file_sessions(decodes, session_split_guard_secs)
    return decodes, sessions


def debug_print_overlap(a_left, a_right, b_left, b_right, ab_left, ab_right):
    def hm(ts):
        return datetime.datetime.fromtimestamp(ts).strftime('%H%M')
    print(datetime.datetime.fromtimestamp(a_left).strftime('%Y-%m-%d'))
    print(f"A: {hm(a_left)} to {hm(a_right)}")
    print(f"B: {hm(b_left)} to {hm(b_right)}")
    print(f"AB: {hm(ab_left)} to {hm(ab_right)}")

def get_overlapping_sessions(a,b, min_session_secs = 60):
    ranges = []
    i = j = 0
    while i < len(a) and j < len(b):
        a_left, a_right, a_bm = a[i]
        b_left, b_right, b_bm = b[j]
        if a_right < b_right:
            i += 1
        else:
            j += 1
        if(a_left>=b_left and a_left < b_right - min_session_secs and a_bm == b_bm):
            ranges.append([a_left, min(a_right, b_right), a_bm])
            #debug_print_overlap(a_left, a_right, b_left, b_right, ranges[-1][0], ranges[-1][1])

        if(b_left>=a_left and b_left < a_right - min_session_secs and a_bm == b_bm):
            ranges.append([b_left, min(a_right, b_right), a_bm])
            #debug_print_overlap(a_left, a_right, b_left, b_right, ranges[-1][0], ranges[-1][1])


        
 
    return ranges



           
