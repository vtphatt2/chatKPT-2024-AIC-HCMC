import os
import pandas as pd
import subprocess
from glob import glob
from transnetv2 import TransNetV2
import cv2
import numpy as np
import shutil

def get_and_save_frame(video_path, frame_id, save_path, filename):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame {frame_id}.")
        cap.release()
        return
    os.makedirs(save_path, exist_ok=True)
    save_file_path = os.path.join(save_path, filename)
    cv2.imwrite(save_file_path, frame)
    print(f"Frame {frame_id} saved successfully at {save_file_path}.")
    cap.release()

os.makedirs('keyframes', exist_ok=True)
os.makedirs('videos', exist_ok=True)
os.makedirs('map-keyframes', exist_ok=True)
model = TransNetV2('/root/transnetv2-weights')

links = pd.read_csv("link_down_video.csv")
links = links[links['Type'] == 'Video']
video_link_dict = {}

for index, row in links.iterrows():
    video_link_dict[row['Filename'][:-4]] = row['Direct Link']

for video, link in video_link_dict.items():
    if (os.path.exists(f'video/{video}')):
        continue
    
    command = [
        'aria2c', link, 
        '--dir', f'videos/', 
        '-s', '16',
        '-x', '16', 
    ]
    subprocess.run(command, check=True)

    command = ['unzip', f'videos/{video}.zip', '-d', 'videos/']
    subprocess.run(command, check=True)

    os.remove(f'videos/{video}.zip')
    os.rename('videos/video', f'videos/{video}')
    shutil.move(f'videos/{video}', 'video/')
    os.rmdir('videos')

    L = video[-3:]
    os.makedirs(f'keyframes/keyframes_{L}', exist_ok=True)

    videos = glob(os.getcwd() + '/' + f'video/{video}/*.mp4')
    videos.sort()
    print(videos)
    
    for sub_video in videos:
        video_name = sub_video[:-4].rsplit('/', 1)[-1]
        with open(f'map-keyframes/{video_name}.csv', 'a') as file:
            file.write('n,pts_time,fps,frame_idx\n')
        video_frames, single_frame_predictions, all_frame_predictions = \
            model.predict_video(sub_video)
        frame_interval = model.predictions_to_scenes(single_frame_predictions)
        os.makedirs(f'keyframes/keyframes_{L}/{video_name}', exist_ok=True)
        for i, row in enumerate(frame_interval):
            frame_id_extracted = int((row[0] + row[1])/2)
            get_and_save_frame(sub_video, frame_id_extracted, f'keyframes/keyframes_{L}/{video_name}', f'{(i+1):03d}.jpg')
            with open(f'map-keyframes/{video_name}.csv', 'a') as file:
                file.write(f'{i+1},{round(frame_id_extracted / 25.0, 2)},25.0,{frame_id_extracted}\n')
        print(f"Finish {video_name}")

    shutil.make_archive(f'keyframes/keyframes_{L}', 'zip', f'keyframes/keyframes_{L}')
