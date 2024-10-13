import os
import cv2
import pickle
from paddleocr import PaddleOCR

# "L01_V001", "L01_V002", "L01_V003",...
COMPLETED = []

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

def process_image(img_path, output_dir):
    img = cv2.imread(img_path)

    if img is None:
        return

    result = ocr.ocr(img_path, cls=True)

    if result and result[0]:
        list_text = {normalize_text(elements[1][0]) for elements in result[0]}
        
        frame_id_with_ext = os.path.basename(img_path)
        frame_id, _ = os.path.splitext(frame_id_with_ext)
        frame_id = int(frame_id)

        video_name = os.path.basename(os.path.dirname(img_path))

        output_path = os.path.join(output_dir, f"{video_name}.bin")
        
        if os.path.exists(output_path):
            with open(output_path, 'rb') as bin_file:
                data = pickle.load(bin_file)
        else:
            data = []

        data.append((frame_id, list_text))

        with open(output_path, 'wb') as bin_file:
            pickle.dump(data, bin_file)

def process_directory(root_path):
    # Change and rename output directory here
    output_dir = 'OCR-Objects'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            if file.endswith('.jpg'):
                img_path = os.path.join(dirpath, file)

                video_name = os.path.basename(os.path.dirname(img_path))

                if video_name in COMPLETED:
                    print(f"Skipping {video_name} as it is already processed.")
                    continue

                process_image(img_path, output_dir)

    for video_name in os.listdir(output_dir):
        if video_name.endswith('.bin'):
            video_name_no_ext = os.path.splitext(video_name)[0]

            if video_name_no_ext in COMPLETED:
                print(f"Skipping {video_name_no_ext} (bin file) as it is already processed.")
                continue

            output_path = os.path.join(output_dir, video_name)
            with open(output_path, 'rb') as bin_file:
                data = pickle.load(bin_file)

            data_sorted = sorted(data, key=lambda x: x[0]) 

            new_data = [text_set for _, text_set in data_sorted]

            with open(output_path, 'wb') as bin_file:
                pickle.dump(new_data, bin_file)

# Change the input path "../../data"
root_path = '../../dataset'
process_directory(root_path)
