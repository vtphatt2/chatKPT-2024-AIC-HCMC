from glob import glob
import os
import numpy as np
from utils.SampleImage import SampleImage
import json
import pickle

class Dataset:
    def __init__(self, data_dir):
        self.dataset = {}

        self.video_clip14_embedding_dict = {}
        self.video_task_former_embedding_dict = {}
        self.video_youtube_link_dict = {}
        self.video_fps_dict = {}
        self.video_transcript_dict = {}
        self.video_ocr_dict = {}

        if (os.path.exists(os.path.join(data_dir, 'video_fps.json'))):
            with open(os.path.join(data_dir, 'video_fps.json'), 'r') as json_file:
                self.video_fps_dict = json.load(json_file)

        for batch in ['batch1', 'batch2', 'batch3']:
        # for batch in ['batch1']:
            clip14_paths = glob(os.path.join(data_dir, batch, 'clip-features-14', '*.npy'))
            clip14_paths.sort()

            for clip14_path in clip14_paths:
                video_name = clip14_path[:-4].rsplit(os.sep, 1)[-1]
                task_former_path = os.path.join(data_dir, batch, 'task-former', f'{video_name}.npy')
                transcript_path = os.path.join(data_dir, batch, 'transcript',  f'{video_name}.bin')
                ocr_path = os.path.join(data_dir, batch, 'ocr',  f'{video_name}.bin')
                self.dataset[video_name] = []

                if (os.path.exists(clip14_path)):
                    self.video_clip14_embedding_dict[video_name] = np.load(clip14_path)

                if (os.path.exists(task_former_path)):
                    self.video_task_former_embedding_dict[video_name] = np.load(task_former_path)

                if (os.path.exists(transcript_path)):
                    with open(transcript_path, 'rb') as file:
                        self.video_transcript_dict[video_name] = pickle.load(file)
                else:
                    self.video_transcript_dict[video_name] = []

                if (os.path.exists(ocr_path) and os.path.getsize(ocr_path) > 0):
                    with open(ocr_path, 'rb') as file:
                        self.video_ocr_dict[video_name] = pickle.load(file)
                else:
                    self.video_ocr_dict[video_name] = []

                metadata_path = os.path.join(data_dir, batch, 'metadata', f'{video_name}.json')
                if (os.path.exists(metadata_path)):
                    with open(metadata_path, 'r', encoding='utf-8') as file:
                        json_data = json.load(file)
                        self.video_youtube_link_dict[video_name] = json_data.get('watch_url')

                L = video_name[:3]
                keyframes_paths = glob(os.path.join(data_dir, batch, "keyframes", f"keyframes_{L}*", video_name, "*.jpg"))
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
    
    def get_video_transcript_dict(self):
        return self.video_transcript_dict
    
    def get_video_ocr_dict(self):
        return self.video_ocr_dict
                                  