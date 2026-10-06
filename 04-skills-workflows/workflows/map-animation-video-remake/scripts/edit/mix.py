import json,subprocess
p=json.load(open('/workspace/proj1/edit/plan.json')); B=[b/30 for b in p['B']]; END=B[7]
A='/workspace/proj1/audio/'
peaks={'whoosh_a':.92,'whoosh_b':.33,'whoosh_c':.04,'whoosh_d':.06}
ev=[]
for k,w in zip(range(1,7),['whoosh_b','whoosh_c','whoosh_a','whoosh_d','whoosh_b','whoosh_a']):
    ev.append((w,B[k]-peaks[w]-0.04,-9))
for n,t in json.load(open('/workspace/proj1/edit/sfx_text.json')):
    g={'pop_a':-10,'pop_b':-11,'ding_a':-9,'impact_a':-4}[n]; ev.append((n,t,g))
ev.append(('riser_scene6_5s',B[6]-5.0,-10))
inputs=["-i",A+"vo_full.mp3","-i",A+"music/bgm_main_epic_bertsz_74s.mp3"]
fc=("[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=%.3f,asplit[vo][sc];"%END)
fc+=("[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:%.3f,volume=-12dB[m0];"%END)
fc+="[m0][sc]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=400:knee=4[md];"
fc+=("[md]volume='if(lt(t,58.45),1,min(1.9,1+0.9*(t-58.45)/0.5))':eval=frame,afade=t=out:st=%.3f:d=2.2[mus];"%(END-2.3))
labels=["[vo]","[mus]"]
for i,(n,t,g) in enumerate(ev):
    inputs+=["-i",A+f"sfx/{n}.wav"]; ms=int(max(0,t)*1000)
    fc+=f"[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[e{i}];"; labels.append(f"[e{i}]")
fc+="".join(labels)+f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{END:.3f}[mix]"
cmd=["ffmpeg","-v","error","-y"]+inputs+["-filter_complex",fc,"-map","[mix]","-c:a","pcm_s24le","/workspace/proj1/work/mix_pre.wav"]
subprocess.run(cmd,check=True)
for n,t,g in ev: print(f"{n:16s} {t:6.2f}s {g}dB")
