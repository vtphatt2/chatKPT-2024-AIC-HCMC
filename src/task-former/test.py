import torch
import clip
from PIL import Image

# Step 1: Load the CLIP model and the corresponding preprocessing function
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)

# Step 2: Load and preprocess the image
# Replace 'path/to/your/image.jpg' with the path to your image
image_path = '/Users/VoThinhPhat/Desktop/chatKPT-2024-AIC-HCMC/data/batch1/keyframes/keyframes_L01/L01_V001/001.jpg'
image = Image.open(image_path).convert("RGB")
image_input = preprocess(image).unsqueeze(0).to(device)

# Step 3: Generate the embeddings
with torch.no_grad():
    # Use the image encoder to get the image features
    image_features = model.encode_image(image_input)

# Step 4: Convert the features to a numpy array
image_embedding = image_features.cpu().numpy().squeeze()

# Print the shape of the embedding
print(f'Embedding shape: {image_embedding.shape}')
print(image_embedding)  # Print the embedding vector
