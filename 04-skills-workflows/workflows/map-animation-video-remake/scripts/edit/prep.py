import subprocess, json
FPS=30
DF=10
D=DF/FPS
starts=[0,7.0,17.312,27.144,38.272,49.472,54.528]; END=62.64+0.8
ends=starts[1:]+[END]
spans=[e-s for s,e in zip(starts,ends)]
B=[round(x*FPS) for x in starts]+[round(END*FPS)]
LF=[(B[i+1]-B[i])+(DF//2 if i in (0,6) else DF) for i in range(7)]
L=[x/FPS for x in LF]
src=[145/24 if i in (0,5) else 241/24 for i in range(7)]
WM={0,3,4,5,6}  # scenes (0-based) with watermark ghost
zoom_dir=[1,-1,1,-1,1,1,1]
plan=[]
for i in range(7):
    f=(L[i]+0.02)/src[i]
    z0,z1=(1.0,1.06) if zoom_dir[i]>0 else (1.06,1.0)
    if i==5: z0,z1=1.0,1.08   # suspense slow push
    zexpr=f"({z0}+({z1-z0})*t/{L[i]:.4f})"
    chain=f"[0:v:0]setpts={f:.5f}*PTS,fps=30,format=yuv420p"
    if i in WM:
        chain+=(",split[a][b];[b]crop=460:360:180:900,boxblur=16:2,format=yuva420p,"
                "geq=lum='p(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*clip(min(min(X,W-1-X),min(Y,H-1-Y))/70,0,1)'[bl];"
                "[a][bl]overlay=180:900:format=auto")
    chain+=(f",scale=w='2*trunc(540*{zexpr})':h='2*trunc(960*{zexpr})':eval=frame:flags=lanczos,"
            "crop=1080:1920:(iw-1080)/2:(ih-1920)/2,"
            "eq=contrast=1.07:saturation=1.13:gamma=0.98,unsharp=5:5:0.55:5:5:0,setsar=1,format=yuv420p")
    chain+=f",trim=end_frame={LF[i]},setpts=PTS-STARTPTS[v]"
    cmd=["ffmpeg","-v","error","-y","-i",f"/workspace/proj1/gen/scene{i+1}.mp4","-filter_complex",chain,
         "-map","[v]","-an","-c:v","libx264","-preset","medium","-crf","14","-r","30",
         f"/workspace/proj1/work/s{i+1}.mp4"]
    plan.append(dict(scene=i+1,L=L[i],speed=src[i]/L[i]))
    import os
    if os.environ.get('ONLY') and str(i+1) not in os.environ['ONLY'].split(','): continue
    subprocess.run(cmd,check=True)
    print(i+1, f"L={L[i]:.3f} speed={src[i]/L[i]:.3f}x", flush=True)
json.dump(dict(B=B,LF=LF,DF=DF,D=D,starts=starts,END=END,L=L,plan=plan),open("/workspace/proj1/edit/plan.json","w"),indent=1)
