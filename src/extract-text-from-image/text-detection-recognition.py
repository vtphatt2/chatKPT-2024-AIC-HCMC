import os
import cv2
import pickle
from paddleocr import PaddleOCR
import logging
from glob import glob

logging.getLogger("ppocr").setLevel(logging.ERROR)

def normalize_text(text):
    replacements = {
        'ö': 'o',
        'ü': 'u',
        'ä': 'a',
        'ß': 'ss',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ô': 'o',
        'î': 'i',
        'â': 'a',
        '@': 'a',
    }
    
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    
    return text.lower()

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

def process_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Image not found at {img_path}.")
        return

    result = ocr.ocr(img_path, cls=True)

    if result and result[0]:
        list_text = set(normalize_text(elements[1][0]) for elements in result[0])
    else:
        list_text = set()

    return list_text


output_dir = 'OCR-Objects'
os.makedirs(output_dir, exist_ok=True)

video_paths = glob(os.path.join(os.getcwd(), 'keyframes', '*', '*'))
video_paths.sort()

for video_path in video_paths:
    video_name = video_path.rsplit(os.sep, 1)[-1]
    
    img_paths = glob(video_path, '*.jpg')
    img_paths.sort()

    frame_data = []

    for img_path in img_paths:
        print(img_path)
        frame_data.append(process_image(img_path))

    output_file_path = os.path.join(output_dir, f'{video_name}.bin')

    with open(output_file_path, 'wb') as bin_file:
        pickle.dump(frame_data, bin_file)

    print(f"Completed: {output_file_path}")
