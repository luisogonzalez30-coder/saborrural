import numpy as np, wave, sys
dur=float(sys.argv[1]); sr=44100; bpm=88; beat=60/bpm; T=dur+0.3
n=int(sr*T); out=np.zeros(n)
def add(sig,start,g=1.0):
    i=int(start*sr); j=min(n,i+len(sig))
    if i<n: out[i:j]+=sig[:j-i]*g
def pluck(f,d=0.9):
    x=np.arange(int(sr*d))/sr
    w=np.sin(2*np.pi*f*x)+0.3*np.sin(4*np.pi*f*x)*np.exp(-x*8)+0.1*np.sin(6*np.pi*f*x)*np.exp(-x*12)
    return w*np.exp(-x*5.5)*np.minimum(1,x*400)
def pad(f,d):
    x=np.arange(int(sr*d))/sr
    w=sum(np.sin(2*np.pi*f*k*x+p) for k,p in ((1,0),(2,1.1),(3,2.2)))*np.array([1])
    env=np.minimum(1,x/0.8)*np.minimum(1,(d-x)/1.0)
    return w*env/3
def soft(x0=None):
    return None
C=lambda m:440*2**((m-69)/12)
prog=[(48,[60,64,67]),(45,[60,64,69]),(41,[60,65,69]),(43,[59,62,67])]
bars=int(T/(beat*4))+1
rng=np.random.default_rng(3)
for bar in range(bars):
    root,ch=prog[bar%4]; st=bar*beat*4
    for m in ch: add(pad(C(m),beat*4.2),st,0.10)
    add(pad(C(root),beat*4.2),st,0.16)
    for k in range(8):
        add(pluck(C(ch[(k*2+bar)%3]+12)),st+k*beat/2,0.18 if k%2==0 else 0.11)
    # latido suave
    for bi in (0,2):
        x=np.arange(int(sr*0.3))/sr; f=55+60*np.exp(-x*30); ph=2*np.pi*np.cumsum(f)/sr
        add(np.sin(ph)*np.exp(-x*10),st+bi*beat,0.22 if bar>=1 else 0)
    for bi in range(4):
        x=np.arange(int(sr*0.04))/sr; nz=rng.standard_normal(len(x)); b=nz-np.convolve(nz,np.ones(8)/8,mode='same')
        add(b*np.exp(-x*80),st+bi*beat+beat/2,0.05)
out=np.tanh(out*1.1)
fi=int(sr*0.8); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.6); out[-fo:]*=np.linspace(1,0,fo)
pcm=(out/np.max(np.abs(out))*0.8*32767).astype('<i2')
with wave.open('musica-suave.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
