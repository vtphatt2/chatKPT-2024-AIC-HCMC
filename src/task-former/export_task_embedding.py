import numpy as np
import json
import torch
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from utils import collate_fn, SimpleImageFolder, DataLoader, DataInfo
from sklearn.neighbors import NearestNeighbors 

CODE_PATH = Path('code/')
MODEL_PATH = Path('model/')
IMAGE_PATH = Path('../../data/batch1/keyframes/')
SAVE_PATH = Path('../../data/batch1/task-former')
sys.path.append(str(CODE_PATH))
model_config_file = CODE_PATH / 'training/model_configs/ViT-B-16.json'
model_file = MODEL_PATH / 'tsbir_model_final.pt'

from clip.model import convert_weights, CLIP
from clip.clip import _transform, load, tokenize

# The rest of your imports and code...

if torch.cuda.is_available():
    device = "cuda"  # Use GPU with CUDA
elif torch.backends.mps.is_available():
    device = "mps"  # Use Metal Performance Shaders for Apple Silicon
else:
    device = "cpu"  # Default to CPU
print(f"Using device: {device}")

with open(model_config_file, 'r') as f:
    model_info = json.load(f)

# Model initialization
model = CLIP(**model_info)
loc = device
checkpoint = torch.load(model_file, map_location=loc, weights_only=False)

sd = checkpoint["state_dict"]
if next(iter(sd.items()))[0].startswith('module'):
    sd = {k[len('module.'):]: v for k, v in sd.items()}

model.load_state_dict(sd, strict=False)
model.eval()
model = model.to(device)

def read_json(file_name):
    with open(file_name) as handle:
        out = json.load(handle)
    return out

convert_weights(model)
preprocess_train = _transform(model.visual.input_resolution, is_train=True)
preprocess_val = _transform(model.visual.input_resolution, is_train=False)
preprocess_fn = (preprocess_train, preprocess_val)

video_img_dict = {}
for path in IMAGE_PATH.glob('*/*/*.jpg'):
    path = str(path)
    video_name = path.rsplit('/', 2)[-2]
    if (video_name not in video_img_dict.keys()):
        video_img_dict[video_name] = [path]
    else:
        video_img_dict[video_name].append(path)

for key in video_img_dict.keys():
    video_img_dict[key].sort()

sorted_key = sorted(video_img_dict.keys())

def main():
    global model

    for video_name in sorted_key:
        print(f'Inference on... {video_name}')

        dataset = SimpleImageFolder(video_img_dict[video_name], transform=preprocess_val)
        dataloader = DataLoader(
            dataset,
            batch_size=32,
            collate_fn=collate_fn,
            shuffle=False,
            num_workers=0,  # Set this to 0 initially for debugging
            pin_memory=True,
            sampler=None,
            drop_last=False,
        )
        dataloader.num_samples = len(dataset)
        dataloader.num_batches = len(dataloader)

        data = DataInfo(dataloader, None)

        cumulative_loss = 0.0
        num_elements = 0.0
        all_image_path = []
        all_image_features = []
        batch_num = 0
        model = model.to(device)
        with torch.no_grad():
            for batch in dataloader:
                print('Batch: ' + str(batch_num), end='')
                images, image_paths = batch
                images = images.to(device, non_blocking=True)
                image_features = model.encode_image(images)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                for i in image_features:
                    all_image_features.append(i.cpu().numpy())
                for i in image_paths:
                    all_image_path.append(i)

                batch_num += 1
                print(' -- Done')

        array_of_arrays = np.array(all_image_features, dtype=np.float32)
        np.save(SAVE_PATH / f'{video_name}.npy', array_of_arrays)
        print("\n")

if __name__ == '__main__':
    main()

