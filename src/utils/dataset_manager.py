import fiftyone as fo
import os
from glob import glob
import pandas as pd
import numpy as np
import tqdm

class Dataset:
    def __init__(self, dataset_name, data_dir):
        self.data_dir = data_dir

        if fo.dataset_exists(dataset_name):
            fo.delete_dataset(dataset_name)
        self.dataset = fo.Dataset.from_images_dir(
            name=dataset_name, 
            images_dir=data_dir, 
            recursive=True
        )

    def get_fiftyone_dataset(self):
        return self.dataset
    
    def load_metadata(self):
        self.image_samples = []
        image_clip14_embedding = []
        image_task_former_embedding = []

        unique_videos = set()
        print("\n1. Load video name and keyframe_id...")
        for sample in self.dataset:
            tmp, sample['video'], sample['keyframe_id'] = sample['filepath'][:-4].rsplit(os.sep, 2)
            sample['batch'] = tmp.rsplit(os.sep, 4)[-3]
            unique_videos.add(sample['video'])
            sample.save()
            print(f"\r\t{sample['video']} with keyframe {sample['keyframe_id']} -- Finish", 
                  end='', flush=True)

        print("\n2. Set up frame idx")
        video_keyframe_dict = {}
        all_keyframe_paths = glob(os.path.join(self.data_dir, 'batch*', 'keyframes',
                                                '*', '*', '*.jpg'))
        video_frameid_dict = {}
        for b in [1, 2, 3]:
            for video in unique_videos:
                filepath = os.path.join(self.data_dir, f'batch{b}', 'map-keyframes', f'{video}.csv')
                if os.path.exists(filepath):
                    a = pd.read_csv(filepath)
                    video_frameid_dict[video] = a['frame_idx']
                    print(f"\r\t{video} is ready...", end='', flush=True)

        for kf in all_keyframe_paths:
            _, vid, kf = kf[:-4].rsplit(os.sep, 2)
            if vid not in video_keyframe_dict.keys():
                video_keyframe_dict[vid] = [kf]
            else:
                video_keyframe_dict[vid].append(kf)

        for k, v in video_keyframe_dict.items():
            video_keyframe_dict[k] = sorted(v)        

        print("\n3. Set up clip_14_dict and task_former_dict")
        embedding_clip14_dict = {}
        embedding_task_former_dict = {}
        for j in [1, 2, 3]:
            for video in unique_videos:
                clip14_path = os.path.join(self.data_dir, f'batch{j}', 
                                        'clip-features-14', f'{video}.npy')
                if os.path.exists(clip14_path):
                    a = np.load(clip14_path)
                    embedding_clip14_dict[video] = {}
                    for i, k in enumerate(video_keyframe_dict[video]):
                        embedding_clip14_dict[video][k] = a[i]

                task_former_path = os.path.join(self.data_dir, f'batch{j}', 
                            'task-former', f'{video}.npy')
                if os.path.exists(task_former_path):
                    b = np.load(task_former_path)
                    embedding_task_former_dict[video] = {}
                    for i, k in enumerate(video_keyframe_dict[video]):
                        embedding_task_former_dict[video][k] = b[i]

                print(f"\r\t{video} is ready...", end='', flush=True)

        print("\n4. Load frame_id, clip-14, task-former")
        for sample in self.dataset:            
            sample['frame_id'] = video_frameid_dict[sample['video']].iloc[int(sample['keyframe_id']) - 1]
            sample['clip-14'] = embedding_clip14_dict[sample['video']][sample['keyframe_id']]
            sample['task-former'] = embedding_task_former_dict[sample['video']][sample['keyframe_id']]
            sample.save()

            self.image_samples.append(sample)
            image_clip14_embedding.append(sample['clip-14']) 
            image_task_former_embedding.append(sample['task-former'])

            print(f"\r\t{sample['video']} is done...", end='', flush=True)
        
        self.image_clip14_embeddings = np.array(image_clip14_embedding)
        self.image_task_former_embeddings = np.array(image_task_former_embedding)