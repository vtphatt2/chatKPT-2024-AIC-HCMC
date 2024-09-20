import torch
from transformers import CLIPProcessor, CLIPModel

class Model:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = "cuda"  # Use GPU with CUDA
        elif torch.backends.mps.is_available():
            self.device = "mps"  # Use Metal Performance Shaders for Apple Silicon
        else:
            self.device = "cpu"  # Default to CPU

        print(f"Using: {self.device}")
        self.model_clip14 = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")

    