import datetime

def allstr_to_epoch(s):
    dt = datetime.datetime(int("20"+s[0:2]), int(s[2:4]), int(s[4:6]),
                            int(s[7:9]), int(s[9:11]), int(s[11:13]))
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

def allfile_line_to_dict(line):
    vals = line.strip().split()
    if len(vals) < 9:
        return False
    t = allstr_to_epoch(vals[0])
    MHz = round(float(vals[1]),3)
    return {'t': int(t), 'ts': vals[0], 'bm':f'{MHz}MHz-{vals[3]}', 'oc': vals[8], 'rp': int(vals[4])}

def get_session_info_string(sess):
    ts, te, bm = sess
    tmins = (te-ts)/60
    return(f"{bm} {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M')} for {tmins} mins")

def list_sessions(sessions):
    for i, s in enumerate(sessions):
        print(f"{i+1} {get_session_info_string(s)}")
        
def load_sessions(allfilepath, session_split_guard_secs, skip_all_before = 0):
    decodes =[]
    for line in open(allfilepath):
        if(allstr_to_epoch(line) > skip_all_before):
            decode = allfile_line_to_dict(line)
            if(decode):
                decodes.append(decode)
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
    sessions = []
    for i, idx in enumerate(s_idx[0:-1]):
        idxs = s_idx[i][0]
        idxe = s_idx[i+1][1]
        sessions_info = (int(decodes[idxs]['t']), int(decodes[idxe]['t']), decodes[idxs]['bm'])
        sessions.append(sessions_info)
    list_sessions(sessions)
    return decodes, sessions

def get_time_overlaps(sessions_A, sessions_B, min_overlap_secs = 60):
    ranges = []
    i = j = 0
    while i < len(sessions_A) and j < len(sessions_B):
        t_start_A, t_stop_A, bm_A = sessions_A[i]
        t_start_B, t_stop_B, bm_B = sessions_B[j]
        if t_stop_A < t_stop_B:
            i += 1
        else:
            j += 1
        if(t_start_A>=t_start_B and t_start_A < t_stop_B - min_overlap_secs and bm_A == bm_B):
            ranges.append([t_start_A, min(t_stop_A, t_stop_B), bm_A])
        if(t_start_B>=t_start_A and t_start_B < t_stop_A - min_overlap_secs and bm_A == bm_B):
            ranges.append([t_start_B, min(t_stop_A, t_stop_B), bm_A])
    return ranges

def time_window_decodes(decodes, tmin, tmax):
    decs = []
    for d in decodes:
        if (d['t']>= tmin and d['t']<= tmax):
            decs.append(d)
    return decs

def load_overlapping_sessions(allfilepath_A, allfilepath_B, session_guard_seconds):
    decodes_A, sessions_A = load_sessions(allfilepath_A, session_guard_seconds)
    decodes_B, sessions_B = load_sessions(allfilepath_B, session_guard_seconds)
    sessions_AB = get_time_overlaps(sessions_A, sessions_B)
    print("Time windowing decode lists")
    tmin, _, _ = sessions_AB[0]
    _, tmax, _ = sessions_AB[-1]
    decodes_A_windowed = time_window_decodes(decodes_A, tmin, tmax)
    decodes_B_windowed = time_window_decodes(decodes_B, tmin, tmax)
    return sessions_AB, decodes_A_windowed, decodes_B_windowed
           
