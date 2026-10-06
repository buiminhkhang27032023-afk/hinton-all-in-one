import json,subprocess
p=json.load(open('/workspace/proj1/edit/plan.json'))
B=p['B']; tr=["zoomin","smoothleft","fadewhite","smoothup","circleopen","fadewhite"]
inp=[]
for i in range(7): inp+=["-i",f"/workspace/proj1/work/s{i+1}.mp4"]
inp+=["-loop","1","-i","/workspace/proj1/edit/grad.png"]
fc=""; prev="[0:v]"
for k in range(6):
    off=(B[k+1]-5)/30; out=f"[x{k}]"
    fc+=f"{prev}[{k+1}:v]xfade=transition={tr[k]}:duration={10/30:.5f}:offset={off:.5f}{out};"; prev=out
fc+=f"{prev}vignette=angle=PI/5.5,format=rgba[vv];[vv][7:v]overlay=0:0:shortest=1,format=yuv420p,ass=/workspace/proj1/edit/overlay.ass:fontsdir='/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro',trim=end_frame={B[7]},setpts=PTS-STARTPTS[v]"
cmd=["ffmpeg","-v","error","-y"]+inp+["-filter_complex",fc,"-map","[v]","-r","30","-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p","-profile:v","high","/workspace/proj1/work/video_v2.mp4"]
subprocess.run(cmd,check=True)
