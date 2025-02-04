import os
import cv2
import pickle
from paddleocr import PaddleOCR
import logging
from glob import glob
import paddle
import unicodedata

logging.getLogger("ppocr").setLevel(logging.ERROR)

def remove_diacritics_and_punctuation(s):
    s = s.replace("'", "")
    nkfd_form = unicodedata.normalize('NFKD', s)
    return ''.join([c for c in nkfd_form if not unicodedata.combining(c)])

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
    
    return remove_diacritics_and_punctuation(text.lower())

use_gpu = paddle.is_compiled_with_cuda()
ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=use_gpu, batch_num=8)

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

    del result
    del img
    paddle.device.cuda.empty_cache()

    return list_text

os.makedirs('ocr', exist_ok=True)

video_paths = glob(os.path.join('keyframes', '*', '*'))
video_paths.sort()

for video_path in video_paths:
    video_name = video_path.rsplit(os.sep, 1)[-1]
    
    output_file_path = os.path.join('ocr', f'{video_name}.bin')

    if os.path.exists(output_file_path):
        continue

    img_paths = glob(os.path.join(video_path, '*.jpg'))
    img_paths.sort()

    frame_data = []

    for img_path in img_paths:
        print(f"OCR for {img_path}")
        frame_data.append(process_image(img_path))

    with open(output_file_path, 'wb') as bin_file:
        pickle.dump(frame_data, bin_file)

    print(f"Completed: {output_file_path}")

