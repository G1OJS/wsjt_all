from readall import read_allfile


allA = r"C:\Users\drala\AppData\Local\WSJT-X\all.txt"
allB = r"C:\Users\drala\AppData\Local\WSJT-X - AltAB\all.txt"

decA, sessA = read_allfile(allA)
decB, sessB = read_allfile(allB)


print(f"Sessions in {allA}")
for t0,t1, ts0,ts1, i0,i1 in sessA:
    print(f"{ts0} to {ts1}")
print(f"Sessions in {allB}")
for t0,t1, ts0,ts1, i0,i1 in sessB:
    print(f"{ts0} to {ts1}")
