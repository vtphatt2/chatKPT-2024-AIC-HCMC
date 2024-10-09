from glob import glob
import os
import numpy as np
from utils.SampleImage import SampleImage
import json
import csv

class Dataset:
    def __init__(self, data_dir):
        self.dataset = {}

        self.video_clip14_embedding_dict = {}
        self.video_task_former_embedding_dict = {}
        self.video_youtube_link_dict = {}

        with open(os.path.join(data_dir, 'video_fps.json'), 'r') as json_file:
            self.video_fps_dict = json.load(json_file)

        for batch in ['batch1', 'batch2', 'batch3']:
            clip14_paths = glob(os.path.join(data_dir, batch, 'clip-features-14', '*.npy'))
            clip14_paths.sort()

            for clip14_path in clip14_paths:
                video_name = clip14_path[:-4].rsplit(os.sep, 1)[-1]
                task_former_path = os.path.join(data_dir, batch, 'task-former', f'{video_name}.npy')
                self.dataset[video_name] = []

                self.video_clip14_embedding_dict[video_name] = np.load(clip14_path)
                self.video_task_former_embedding_dict[video_name] = np.load(task_former_path)

                metadata_path = os.path.join(data_dir, batch, 'metadata', f'{video_name}.json')
                with open(metadata_path, 'r') as file:
                    json_data = json.load(file)
                    self.video_youtube_link_dict[video_name] = json_data.get('watch_url')

                L = video_name[:3]
                keyframes_paths = glob(os.path.join(data_dir, batch, "keyframes", f"keyframes_{L}", video_name, "*.jpg"))
                keyframes_paths.sort()

                for i in range(0, len(keyframes_paths)):
                    self.dataset[video_name].append(SampleImage(keyframes_paths[i]))
                
    def get_dataset(self):
        return self.dataset

    def get_video_clip14_embedding_dict(self):
        return self.video_clip14_embedding_dict

    def get_video_task_former_embedding_dict(self):
        return self.video_task_former_embedding_dict
    
    def get_video_youtube_link_dict(self):
        return self.video_youtube_link_dict
    
    def get_video_fps_dict(self):
        return self.video_fps_dict
                                  