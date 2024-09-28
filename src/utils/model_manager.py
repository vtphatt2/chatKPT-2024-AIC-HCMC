import torch
from transformers import CLIPProcessor, CLIPModel
import os
import json
import sys
from PIL import Image
sys.path.append("utils/")
from clip.model import convert_weights, CLIP
from clip.clip import _transform, load, tokenize

class CLIP_14_model:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = "cuda"  
        elif torch.backends.mps.is_available():
            self.device = "mps"  
        else:
            self.device = "cpu"
        print(f"Model openai-clip-vit-large-patch14 is using {self.device}")  

        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(self.device)    
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336") 

    def inference(self, text_input):
        inputs = self.processor(text=[text_input], return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs).cpu().numpy().flatten()
        return text_features
    
class TASK_former_model:
    def __init__(self, model_config_file=None, model_file=None):
        if (not model_config_file):
            print("Missing model_config_file...!")
            return
        if (not model_file):
            print("Missing model_file...!")
            return
        self.model_config_file = model_config_file
        self.model_file = model_file

        if torch.cuda.is_available():
            self.device = "cuda"  
        elif torch.backends.mps.is_available():
            self.device = "mps"  
        else:
            self.device = "cpu"
        print(f"Model TASK-former is using {self.device}")  
        with open(self.model_config_file, 'r') as f:
            self.model_info = json.load(f)

        self.model = CLIP(**self.model_info)
        loc = self.device
        checkpoint = torch.load(model_file, map_location=loc)
        sd = checkpoint["state_dict"]
        if next(iter(sd.items()))[0].startswith('module'):
            sd = {k[len('module.'):]: v for k, v in sd.items()}      
        self.model.load_state_dict(sd, strict=False)
        self.model.eval()
        self.model = self.model.to(self.device)  
        convert_weights(self.model)
        preprocess_val = _transform(self.model.visual.input_resolution, is_train=False)
        self.transformer = preprocess_val

    def get_feature(self, query_sketch, query_text):
        img1 = self.transformer(query_sketch).unsqueeze(0).to(self.device)
        txt = tokenize([str(query_text)])[0].unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            sketch_feature = self.model.encode_sketch(img1)
            text_feature = self.model.encode_text(txt)
            text_feature = text_feature / text_feature.norm(dim=-1, keepdim=True)
            sketch_feature = sketch_feature / sketch_feature.norm(dim=-1, keepdim=True)

        return self.model.feature_fuse(sketch_feature, text_feature)        
    
    def inference(self, text, sketch):
        query_feat = self.get_feature(sketch, text).cpu().numpy().flatten()
        return query_feat