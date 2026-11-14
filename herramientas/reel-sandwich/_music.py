import numpy as np, wave
def music(total,bpm,seed,path):
    sr=44100; beat=60/bpm; Tm=total+0.3; n=int(sr*Tm); out=np.zeros(n); rng=np.random.default_rng(seed)
    def add(sig,st,g=1.0):
        i=int(st*sr); j=min(n,i+len(sig))
        if i<n: out[i:j]+=sig[:j-i]*g
    def pluck(f,d=0.5):
        x=np.arange(int(sr*d))/sr; return (np.sin(2*np.pi*f*x)+0.3*np.sin(4*np.pi*f*x)*np.exp(-x*8))*np.exp(-x*7)*np.minimum(1,x*400)
    def pad(f,d):
        x=np.arange(int(sr*d))/sr; w=sum(np.sin(2*np.pi*f*k*x+p) for k,p in ((1,0),(2,1.1),(3,2.2)))/3; return w*np.minimum(1,x/0.6)*np.minimum(1,(d-x)/0.8)
    Cn=lambda m:440*2**((m-69)/12); prog=[(48,[60,64,67]),(43,[59,62,67]),(45,[60,64,69]),(41,[60,65,69])]
    for bar in range(int(Tm/(beat*4))+1):
        root,ch=prog[bar%4]; st=bar*beat*4
        for m in ch: add(pad(Cn(m),beat*4.2),st,0.09)
        add(pad(Cn(root),beat*4.2),st,0.15)
        for k in range(8): add(pluck(Cn(ch[(k*2+bar)%3]+12)),st+k*beat/2,0.17 if k%2==0 else 0.10)
        for bi in range(4):
            x=np.arange(int(sr*0.3))/sr; f=55+70*np.exp(-x*32); add(np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-x*11),st+bi*beat,0.24)
            x=np.arange(int(sr*0.05))/sr; nz=rng.standard_normal(len(x)); add((nz-np.convolve(nz,np.ones(8)/8,mode='same'))*np.exp(-x*70),st+bi*beat+beat/2,0.06)
    out=np.tanh(out*1.1); fi=int(sr*0.5); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.6); out[-fo:]*=np.linspace(1,0,fo)
    pcm=(out/np.max(np.abs(out))*0.8*32767).astype('<i2')
    with wave.open(path,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
