import snapshot_data

calls = set()

for d in snapshot_data.decA:
    calls.add(d['oc'])

for d in snapshot_data.decB:
    calls.add(d['oc'])

data = []
for i, c in enumerate(calls):
    data.append({'c':c, 'A':{'n':0, 'f':50, 't':-50}, 'B':{'n':0, 'f':50, 't':-50}})
    for d in snapshot_data.decA:
        if(c==d['oc']):
            data[-1]['A']['n'] += 1
            if (d['rp']> data[i]['A']['t']):
                data[i]['A']['t'] = d['rp']
            if (d['rp']< data[i]['A']['f']):
                data[i]['A']['f'] = d['rp']            
    for d in snapshot_data.decB:
        if(c==d['oc']):
            data[-1]['B']['n'] += 1
            if (d['rp']> data[i]['B']['t']):
                data[i]['B']['t'] = d['rp']
            if (d['rp']< data[i]['B']['f']):
                data[i]['B']['f'] = d['rp']             

for i, c in enumerate(calls):
    print(c, data[i]['A']['n'], data[i]['A']['f'], data[i]['A']['t'],
          data[i]['B']['n'], data[i]['B']['f'], data[i]['B']['t'],)
