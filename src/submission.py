# %%
import fiftyone as fo
import os
import pandas as pd
import numpy as np
from glob import glob
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import csv

# %%
# run in about 15 seconds
if fo.dataset_exists("AIC_2024"):
    fo.delete_dataset("AIC_2024")
    
dataset = fo.Dataset.from_images_dir(
    name="AIC_2024", 
    images_dir=os.path.join("..", "data", "batch1", "keyframes"), 
    recursive=True
)

# %%
# run in about 36 seconds
unique_videos = set()
for sample in dataset:
    tmp, sample['video'], sample['keyframe_id'] = sample['filepath'][:-4].rsplit(os.sep, 2)
    sample['batch'] = tmp.rsplit(os.sep, 4)[-3]
    unique_videos.add(sample['video'])
    sample.save()

# %%
# run in nearly 40 seconds
video_frameid_dict = {}
for b in [1, 2, 3]:
    for video in unique_videos:
        filepath = os.path.join('..', 'data', f'batch{b}', 'map-keyframes', f'{video}.csv')
        if os.path.exists(filepath):
            a = pd.read_csv(filepath)
            video_frameid_dict[video] = a['frame_idx']

for sample in dataset:
    # print(sample['video'] + '-' + sample['keyframe_id'])
    sample['frame_id'] = video_frameid_dict[sample['video']].iloc[int(sample['keyframe_id']) - 1]
    sample.save()

# %%
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

# %%
# run in 10 minutes
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")

# %%
# run in 11 seconds
image_samples = []
image_embeddings = []
for sample in dataset:
    image_samples.append(sample)
    image_embeddings.append(sample['clip-14']) 
image_embeddings = np.array(image_embeddings)

# %%
def submission(text_query, k, csv_file):
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

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['video', 'frame_id'])
        # writer.writeheader()
        for sample in dataset_submission:
            writer.writerow({'video': sample['video'], 'frame_id': sample['frame_id']})

    return dataset_submission

# # %%
# text_query = "A scene from a radiation emergency response exercise. The first shot shows a person in yellow and blue clothes lying on the ground wearing a mask, followed by a fire brigade using a fire extinguisher to spray smoke. It ends with two people in blue protective suits carrying a victim on a stretcher. How many people use the fire extinguisher in the scene?"
# output_file = "output.csv"

# output_file = os.path.join('..', 'submission', output_file)
# dataset_submission = submission(text_query, 100, output_file)
# session = fo.launch_app(dataset_submission, auto=False)
# session.open_tab()


