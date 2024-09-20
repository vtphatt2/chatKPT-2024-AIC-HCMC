import fiftyone as fo
import os
from glob import glob
import pandas as pd
import numpy as np
import tqdm

class Dataset:
    def __init__(self, dataset_name, images_dir):
        self.images_dir = images_dir

        if fo.dataset_exists(dataset_name):
            fo.delete_dataset(dataset_name)
        self.dataset = fo.Dataset.from_images_dir(
            name=dataset_name, 
            images_dir=images_dir, 
            recursive=True
        )

    def get_fo_dataset(self):
        return self.dataset
    
    def load_metadata(self):
        self.image_samples = []
        image_clip14_embedding = []
        image_task_former_embedding = []

        unique_videos = set()
        print("Load video and keyframe_id...")
        for sample in self.dataset:
            print(sample['filepath'])
            tmp, sample['video'], sample['keyframe_id'] = sample['filepath'][:-4].rsplit(os.sep, 2)
            sample['batch'] = tmp.rsplit(os.sep, 4)[-3]
            unique_videos.add(sample['video'])
            sample.save()

        print("Load video_keyframe_dict")
        video_keyframe_dict = {}
        all_keyframe_paths = glob(os.path.join(self.images_dir, 'batch*', 'keyframes',
                                                '*', '*', '*.jpg'))
        video_frameid_dict = {}
        for b in [1, 2, 3]:
            for video in unique_videos:
                print(video)
                filepath = os.path.join(self.images_dir, f'batch{b}', 'map-keyframes', f'{video}.csv')
                if os.path.exists(filepath):
                    a = pd.read_csv(filepath)
                    video_frameid_dict[video] = a['frame_idx']

        for kf in all_keyframe_paths:
            print(kf)
            _, vid, kf = kf[:-4].rsplit(os.sep, 2)
            if vid not in video_keyframe_dict.keys():
                video_keyframe_dict[vid] = [kf]
            else:
                video_keyframe_dict[vid].append(kf)

        for k, v in video_keyframe_dict.items():
            video_keyframe_dict[k] = sorted(v)        

        print("Load clip_14_dict and task_former_dict")
        embedding_clip14_dict = {}
        embedding_task_former_dict = {}
        for j in [1, 2, 3]:
            for video in unique_videos:
                print(video)
                clip14_path = os.path.join(self.images_dir, f'batch{j}', 
                                        'clip-features-14', f'{video}.npy')
                if os.path.exists(clip14_path):
                    a = np.load(clip14_path)
                    embedding_clip14_dict[video] = {}
                    for i, k in enumerate(video_keyframe_dict[video]):
                        embedding_clip14_dict[video][k] = a[i]

                task_former_path = os.path.join(self.images_dir, f'batch{j}', 
                            'task-former', f'{video}.npy')
                if os.path.exists(task_former_path):
                    b = np.load(task_former_path)
                    embedding_task_former_dict[video] = {}
                    for i, k in enumerate(video_keyframe_dict[video]):
                        embedding_task_former_dict[video][k] = b[i]

        for sample in self.dataset:
            print(sample['video'] + ' - ' + sample['keyframe_id'], end='')
            
            sample['frame_id'] = video_frameid_dict[sample['video']].iloc[int(sample['keyframe_id']) - 1]
            sample['clip-14'] = embedding_clip14_dict[sample['video']][sample['keyframe_id']]
            sample['task-former'] = embedding_task_former_dict[sample['video']][sample['keyframe_id']]
            self.image_samples.append(sample)
            image_clip14_embedding.append(sample['clip-14']) 
            image_task_former_embedding.append(sample['task-former'])

            print(" ---  Done")
            sample.save()
        
        self.image_clip14_embeddings = np.array(image_clip14_embedding)
        self.image_task_former_embeddings = np.array(image_task_former_embedding)
        
        return self