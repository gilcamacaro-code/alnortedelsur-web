import sys, wave
import numpy as np
SR=44100
out_path=sys.argv[1]; DUR=float(sys.argv[2]); cuts=[float(x) for x in sys.argv[3].split(',') if x]; dings=[float(x) for x in sys.argv[4].split(',') if x]
BPM=124; beat=60/BPM; n=int(SR*DUR); out=np.zeros(n)
def add(sig,st):
    i=int(st*SR)
    if i<0 or i>=n: return
    e=min(n,i+len(sig)); out[i:e]+=sig[:e-i]
def kick():
    tt=np.arange(int(.22*SR))/SR
    ph=2*np.pi*np.cumsum(110*np.exp(-tt*25)+48)/SR
    return np.sin(ph)*np.exp(-tt*10)*.8
def clap():
    tt=np.arange(int(.14*SR))/SR
    return np.random.default_rng(2).standard_normal(len(tt))*np.exp(-tt*30)*.22
def hat():
    tt=np.arange(int(.04*SR))/SR
    return np.diff(np.random.default_rng(1).standard_normal(len(tt)+1))*np.exp(-tt*90)*.10
def pluck(f,amp=.2,d=.28):
    tt=np.arange(int(d*SR))/SR
    s=np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*2*f*tt)+.25*np.sin(2*np.pi*3*f*tt)
    return s*np.exp(-tt*9)*amp
def bass(f):
    tt=np.arange(int(.3*SR))/SR
    return np.sin(2*np.pi*f*tt)*np.exp(-tt*6)*.34
def ding(f=1568):
    tt=np.arange(int(.9*SR))/SR
    return (np.sin(2*np.pi*f*tt)+.4*np.sin(2*np.pi*f*2.01*tt))*np.exp(-tt*5)*.3
def whoosh():
    d=.28; tt=np.arange(int(d*SR))/SR
    r=np.random.default_rng(5).standard_normal(len(tt))
    # crude rising band via modulation
    return r*np.sin(2*np.pi*(300+3000*tt/d)*tt)*np.sin(np.pi*tt/d)*.35
# C-G-Am-F, bright major
chords=[(261.63,329.63,392.0),(196.0,246.94,293.66),(220.0,261.63,329.63),(174.61,220.0,261.63)]
roots=[130.81,98.0,110.0,87.31]
e=beat/2
for k in range(int(DUR/e)+2):
    st=k*e; bar=(k//8)%4; ch=chords[bar]
    if k%2==0: add(kick(),st) if k%4!=0 or True else None
    if k%4==2: add(clap(),st)
    add(hat(),st+0)
    if k%2==1: add(bass(roots[bar]*(2 if k%4==3 else 1)),st)
    if st>=.4:
        note=ch[k%3]*(2 if (k//3)%2 else 1)
        add(pluck(note),st)
for c in cuts: add(whoosh(),max(0,c-.12))
for d in dings: add(ding(),d)
t=np.arange(n)/SR
out*=np.clip(np.minimum(t/.05,(DUR-t)/.6),0,1)
out=out/(np.abs(out).max()+1e-9)*.88
with wave.open(out_path,'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
