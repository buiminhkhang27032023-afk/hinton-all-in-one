#!/bin/bash
cd /workspace/video-learn
ls tiktok-duyluandethuong/*.mp4 tiktok-dinhhanai/*.mp4 tiktok-leduyhiep.aihub/*.mp4 youtube-VarunMayya/*.mp4 youtube-JeffSu/*.mp4 tiktokintl-tommythings/*.mp4 tiktokintl-adam.digital/*.mp4 tiktokintl-brandnat/*.mp4 > tr_new.txt
nice /workspace/.whisper-venv/bin/python tools/transcribe.py --force $(cat tr_new.txt)
nice /workspace/.whisper-venv/bin/python tools/transcribe.py --force $(cat tr_old.txt)
echo TRNEW_DONE
