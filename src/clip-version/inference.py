from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np
import os
import glob 

# run in about 3 minutes in the first time installed
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")

batch_videos_dict = {}
path_pattern = os.path.join(os.getcwd(), '..', '..', 'data', 
                            'batch*', 'keyframes', '*', '*')
paths = glob.glob(path_pattern)

for path in paths:
    _, batch_name, _, _, video_name = path.rsplit(os.sep, 4)
    if batch_name not in batch_videos_dict:
        batch_videos_dict[batch_name] = []
    batch_videos_dict[batch_name].append(video_name)

for batch in batch_videos_dict.keys():
    batch_videos_dict[batch].sort()

for batch in batch_videos_dict.keys():
    for video in batch_videos_dict[batch]:
        path_save = os.path.join(os.getcwd(), '..', '..', 'data', 
                            batch, 'clip-features-14', video + ".npy") 
        if os.path.isfile(path_save):
            continue

        path_to_keyframe = os.path.join(os.getcwd(), '..', '..', 'data', 
                            batch, 'keyframes', 'keyframes_' + video[:3], video) 
        print(path_to_keyframe)

        embeddings = []
        image_files = [os.path.join(path_to_keyframe, f) for f in os.listdir(path_to_keyframe) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        image_files.sort()

        for image_path in image_files:
            print(image_path)
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(device)
            with torch.no_grad():
                image_features = model.get_image_features(**inputs).to(device)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            embeddings.append(image_features.cpu().numpy().flatten())
        embeddings_array = np.array(embeddings)
        path_save = os.path.join(os.getcwd(), '..', '..', 'data', 
                            batch, 'clip-features-14', video + ".npy") 
        np.save(path_save, embeddings_array)
