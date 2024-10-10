import re
import pickle
import os
import json
from glob import glob

def load_transcript_binary(file_path):
    with open(file_path, 'rb') as file:
        transcript = pickle.load(file)
    return transcript

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    transcript_folder = "transcript"
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)
        
    video_transcript_dict = {}
    for path in glob(os.path.join(transcript_folder, '*.bin')):
        video_name = os.path.splitext(os.path.basename(path))[0]
        video_transcript_dict[video_name] = load_transcript_binary(path)
    
    while True:
        user_input = input("\nNhập các từ khóa, phân cách bởi dấu phẩy (hoặc 'exit' để thoát): ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("Thoát chương trình.")
            break
        keywords = [kw.strip().lower() for kw in user_input.split(',') if kw.strip()]
        if not keywords:
            print("Không có từ khóa nào được nhập. Vui lòng thử lại.")
            continue
        clear_terminal()
        print(f"Đã nhận các từ khóa: {keywords}")
        results = {}
        keyword_counts = {}
        for video_name, transcript_list in video_transcript_dict.items():
            full_text = ' '.join(text for _, text in transcript_list).lower()
            if all(keyword in full_text for keyword in keywords):
                total_count = 0
                segments = []
                for start_time, text in transcript_list:
                    text_lower = text.lower()
                    count = sum(text_lower.count(keyword) for keyword in keywords)
                    if count > 0:
                        total_count += count
                        segments.append((start_time, text))
                if total_count > 0:
                    results[video_name] = segments
                    keyword_counts[video_name] = total_count
        if results:
            sorted_videos = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)[:15]
            print("\nCác video chứa các từ khóa đã nhập (tối đa 15 video):")
            for video_name, _ in sorted_videos:
                print(f"\nVideo: {video_name}")
                for start_time, text in results[video_name]:
                    print(f"  {start_time}: {text}")
        else:
            print("\nKhông tìm thấy video nào chứa các từ khóa đã nhập.")

if __name__ == "__main__":
    main()
