#!/usr/bin/env python
# coding: utf-8

# In[25]:


import fiftyone as fo
import os
import pandas as pd
import numpy as np
from glob import glob
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import csv
import json
import sys
sys.path.append('task-former/code')
from clip.model import convert_weights, CLIP    
from clip.clip import _transform, load, tokenize
from collections import Counter


# In[2]:


# run in about 15 seconds
if fo.dataset_exists("AIC_2024"):
    fo.delete_dataset("AIC_2024")

batch_dirs = glob(os.path.join("..", "data", "batch*", "keyframes"))
    
dataset = fo.Dataset(name="AIC_2024")

for batch_dir in batch_dirs:
    dataset.add_images_dir(batch_dir, recursive=True)


# In[3]:


# run in about 36 seconds
unique_videos = set()
for sample in dataset:
    tmp, sample['video'], sample['keyframe_id'] = sample['filepath'][:-4].rsplit(os.sep, 2)
    sample['batch'] = tmp.rsplit(os.sep, 4)[-3]
    unique_videos.add(sample['video'])
    sample.save()


# In[ ]:


# # object detection
# for sample in dataset:
#     object_paths = glob(os.path.join("..", "data", "batch*", "object", sample['video'], sample['keyframe_id'] + ".json"))

#     if not object_paths:
#         continue
#     object_path = object_paths[0]
    
#     with open(object_path) as jsonfile:
#         det_data = json.load(jsonfile)
    
#     detections = []
#     for cls, box, score in zip(det_data['detection_class_entities'], det_data['detection_boxes'], det_data['detection_scores']):
#         box = [float(coord) for coord in box] 
#         boxf = [box[1], box[0], box[3] - box[1], box[2] - box[0]]
#         scoref = float(score)
#         if scoref > 0.4:
#             detections.append(
#                 fo.Detection(label=cls, 
#                              bounding_box=boxf, 
#                              confidence=scoref)
#             )

#     sample["object_faster_rcnn"] = fo.Detections(detections=detections)
#     sample.save()


# In[50]:


# run in nearly 40 seconds
video_frameid_dict = {}
for b in [1, 2, 3]:
    for video in unique_videos:
        filepath = os.path.join('..', 'data', f'batch{b}', 'map-keyframes', f'{video}.csv')
        if os.path.exists(filepath):
            a = pd.read_csv(filepath)
            video_frameid_dict[video] = a['frame_idx']

for sample in dataset:
    print(sample['video'] + '-' + sample['keyframe_id'])
    sample['frame_id'] = video_frameid_dict[sample['video']].iloc[int(sample['keyframe_id']) - 1]
    sample.save()


# In[51]:


# run in about 1 minutes
video_keyframe_dict = {}
all_keyframe_paths = glob(os.path.join(os.getcwd(), '..', 'data', 'batch*', 'keyframes',
                            '*', '*', '*.jpg'))

for kf in all_keyframe_paths:
    _, vid, kf = kf[:-4].rsplit(os.sep, 2)
    if vid not in video_keyframe_dict.keys():
        video_keyframe_dict[vid] = [kf]
    else:
        video_keyframe_dict[vid].append(kf)

for k, v in video_keyframe_dict.items():
    video_keyframe_dict[k] = sorted(v)

embedding_dict = {}
for j in [1, 2, 3]:
    for video in unique_videos:
        clip_14_path = os.path.join('..', 'data', f'batch{j}', 
                            'clip-features-14', f'{video}.npy')
        if os.path.exists(clip_14_path):
            a = np.load(clip_14_path)
            embedding_dict[video] = {}
            for i, k in enumerate(video_keyframe_dict[video]):
                embedding_dict[video][k] = a[i]

for sample in dataset:
    sample['clip-14'] = embedding_dict[sample['video']][sample['keyframe_id']]
    sample.save()


# In[6]:


dataset.first()


# In[52]:


# run in 10 minutes
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")


# In[53]:


# run in 11 seconds
image_samples = []
image_embeddings = []
for sample in dataset:
    image_samples.append(sample)
    image_embeddings.append(sample['clip-14']) 
image_embeddings = np.array(image_embeddings)


# In[54]:


def submission(text_query, k, csv_file, Subquery=False):
    inputs = processor(text=[text_query], return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs).cpu().numpy().flatten()
    similarities = cosine_similarity([text_features], image_embeddings)[0]
    top_k_indices = similarities.argsort()[-k:][::-1]

    if fo.dataset_exists("submission"):
        fo.delete_dataset("submission")

    dataset_submission = fo.Dataset(
        name="submission"
    )

    for index in top_k_indices:
        dataset_submission.add_sample(image_samples[index])

    mode = 'a' if Subquery else 'w'
    with open(csv_file, mode=mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['video', 'frame_id'])
        for sample in dataset_submission:
            writer.writerow({'video': sample['video'], 'frame_id': sample['frame_id']})

    return dataset_submission


# In[63]:


# text_query = "A scene of a person riding a horse running parallel to two people riding a motorbike in an open field."
# output_file = "output.csv"

# output_file = os.path.join('..', 'src', output_file)
# dataset_submission = submission(text_query, 500, output_file)
# session = fo.launch_app(dataset_submission, auto=False)
# session.open_tab()


# In[11]:


import csv
from collections import OrderedDict

def organizeOutput(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    organized_data = OrderedDict()
    for row in data:
        key = row[0]
        if key not in organized_data:
            organized_data[key] = []
        organized_data[key].append(row)

    for key in organized_data:
        organized_data[key].sort(key=lambda x: float(x[1]))

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for rows in organized_data.values():
            writer.writerows(rows)


# In[67]:


def calculate_keyframe_id(path):
    df = pd.read_csv(path, header=None, names=['video', 'frame_id'])
    keyframe_paths = []
    for index, row in df.iterrows():
        video = row['video']
        frame_id = row['frame_id']
        if video in video_frameid_dict and (video_frameid_dict[video] == frame_id).any():
            key_frame = video_frameid_dict[video][video_frameid_dict[video] == frame_id].index[0] + 1
            batch_dirs = glob(os.path.join("..", "data", "batch*", "keyframes"))
            for batch_dir in batch_dirs:
                keyframe_path = os.path.join(
                    batch_dir,
                    f"keyframes_{video.split('_')[0]}",
                    video,
                    f"{key_frame:03d}.jpg"
                )
                if os.path.exists(keyframe_path):
                    absolute_path = os.path.abspath(keyframe_path)
                    keyframe_paths.append(absolute_path)
        else:
            print(f'Video {video} and frame_id {frame_id} not found in the dataset')

    with open("image_result_path.txt", "w") as file:
        for path in keyframe_paths:
            file.write(path + "\n")

    return keyframe_paths


# In[15]:


def loadKeyframes(image_path):
    keyframe_paths = []
    directory = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    base_number = int(os.path.splitext(base_name)[0])
    
    for i in range(max(0, base_number - 10), base_number + 11):
        keyframe_path = os.path.join(directory, f"{i:03d}.jpg") 
        if os.path.exists(keyframe_path):
            keyframe_paths.append(keyframe_path)
                
    return keyframe_paths


# In[16]:


def getMajorInfo(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        publish_date = data.get('publish_date')
        watch_url = data.get('watch_url')
        return publish_date, watch_url

def getImageInformation(path):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(path))))
    video_id = os.path.basename(os.path.dirname(path))
    metadata_filename = f"{video_id}.json"
    metadata_path = os.path.join(base_dir, "metadata", metadata_filename)
    publish_date, watch_url = getMajorInfo(metadata_path)
  
    return publish_date, watch_url


# In[66]:


# find the object detection json files
def findObjectPaths(image_result_path):
    with open(image_result_path, 'r') as file:
        image_paths = file.readlines()

    def convert_to_object_path(image_path):
        object_path = image_path.replace('keyframes', 'object')
        object_path = os.path.splitext(object_path)[0] + '.json'
        parts = object_path.split(os.sep)
        if 'object' in parts:
            index = parts.index('object')
            if index + 1 < len(parts):
                parts.pop(index + 1)
        object_path = os.sep.join(parts)
        return object_path
    
    object_paths = [convert_to_object_path(image_path.strip()) for image_path in image_paths]
    matched_files = []
    for object_path in object_paths:
        matched_files.extend(glob(object_path))
    
    return matched_files

# get top objects
def getTopObjects(json_file_path, top_k):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Get top k objects
    scores = list(map(float, data['detection_scores']))
    entities = data['detection_class_entities']
    score_entity_pairs = list(zip(scores, entities))
    score_entity_pairs.sort(reverse=True, key=lambda x: x[0])
    seen_entities = set()
    top_entities = []
    for score, entity in score_entity_pairs:
        if entity not in seen_entities:
            seen_entities.add(entity)
            top_entities.append(entity)
        if len(top_entities) == top_k:
            break
    
    # Save to CSV
    output_csv_path = os.path.abspath(os.path.join('..', 'src', 'top_objects.csv'))
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df = pd.DataFrame({
        'json_file_path': [json_file_path],
        'top_entities': [', '.join(top_entities)]
    })

    if os.path.exists(output_csv_path):
        df.to_csv(output_csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(output_csv_path, index=False)

# get object insights
def getObjectInsights(top_objects_csv_path, k):
    df = pd.read_csv(top_objects_csv_path)
    all_entities = []
    for entities in df['top_entities']:
        all_entities.extend(entities.split(', '))
    
    entity_counts = Counter(all_entities)
    top_k_entities = entity_counts.most_common(k)
    
    return top_k_entities
    
# organize object data
def organizeObjectData(image_result_path, k):
    object_paths = findObjectPaths(image_result_path)
    for object_path in object_paths:
        getTopObjects(object_path, k)

    top_objects_csv_path = os.path.join('..', 'src', 'top_objects.csv')
    top_k_entities = getObjectInsights(top_objects_csv_path, k)
    return top_k_entities


