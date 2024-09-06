import os
import pandas as pd
import subprocess
from glob import glob
from transnetv2 import TransNetV2
import cv2
import numpy as np

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