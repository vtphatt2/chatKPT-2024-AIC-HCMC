import os
from functools import partial
from multiprocessing.pool import Pool

import cv2
import youtube_dl

def process_video_parallel(url, skip_frames, process_number):
    cap = cv2.VideoCapture(url)
    num_processes = os.cpu_count()
    frames_per_process = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // num_processes
    cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)
    x = 0
    count = 0
    while x < 10 and count < frames_per_process:
        ret, frame = cap.read()
        if not ret:
            break
        filename =r"PATH\shot"+str(x)+".png"
        x += 1
        cv2.imwrite(filename.format(count), frame)
        count += skip_frames  # Skip 300 frames i.e. 10 seconds for 30 fps
        cap.set(1, count)
    cap.release()



video_url = "https://www.youtube.com/watch?v=1CIAW2V5eIE"  # The Youtube URL
ydl_opts = {}
ydl = youtube_dl.YoutubeDL(ydl_opts)
info_dict = ydl.extract_info(video_url, download=False)

formats = info_dict.get('formats', None)

print("Obtaining frames")
for f in formats:
    if f.get('format_note', None) == '144p':
        url = f.get('url', None)
        cpu_count = os.cpu_count()
        with Pool(cpu_count) as pool:
            pool.map(partial(process_video_parallel, url, 300), range(cpu_count))