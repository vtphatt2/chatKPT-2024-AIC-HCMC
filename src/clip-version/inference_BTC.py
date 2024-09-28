from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np
import os
import glob 
import subprocess
import pandas as pd
import shutil

links = pd.read_csv("link_down_video.csv")
links = links[links['Type'] == 'Keyframe']
keyframe_link_dict = {}

for index, row in links.iterrows():
    keyframe_link_dict[row['Filename'][:-4]] = row['Direct Link']

os.makedirs('keyframes/', exist_ok=True)
os.makedirs('keyframe/', exist_ok=True)
os.makedirs('clip-features-14/', exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")

for keyframe, link in keyframe_link_dict.items():
    command = [
        'aria2c', link, 
        '--dir', f'keyframe/', 
        '-s', '16',
        '-x', '16', 
    ]
    subprocess.run(command, check=True)

    command = ['unzip', f'keyframe/{keyframe}.zip', '-d', 'keyframe/']
    subprocess.run(command, check=True)

    os.rename('keyframe/keyframes', f'keyframe/{keyframe}')
    shutil.move(f'keyframe/{keyframe}', 'keyframes')

    unique_videos = set()
    for path in glob.glob(os.getcwd() + f'/keyframes/{keyframe}/*'):
        video_name = path.rsplit('/', 1)[-1]
        unique_videos.add(video_name)

    unique_videos = sorted(unique_videos)

    for video_name in unique_videos:
        print(video_name)
        images_paths = glob.glob(os.getcwd() + f'/keyframes/{keyframe}/{video_name}/*')
        images_paths.sort()
        embeddings = []

        for image_path in images_paths:
            print(image_path)
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(device)
            with torch.no_grad():
                image_features = model.get_image_features(**inputs).to(device)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            embeddings.append(image_features.cpu().numpy().flatten())
        
        embeddings_array = np.array(embeddings)
        path_save = os.path.join(os.getcwd(), 'clip-features-14', video_name + ".npy") 
        np.save(path_save, embeddings_array)