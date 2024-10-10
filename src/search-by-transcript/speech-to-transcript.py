import wave
import math
import contextlib
import speech_recognition
from moviepy.editor import AudioFileClip
from tqdm import tqdm
import os
import pickle

NO_SCRIPT_PATH = "no_transcript.txt"
GET_AUDIO_FILE = False
BASE_PATH = "../../data"

if not os.path.exists("audio"):
    os.makedirs("audio")

with open(NO_SCRIPT_PATH, 'r', encoding="utf-8") as file:
    lines = file.readlines()

for line in tqdm(lines):
    video_name = line.strip()
    filename, _ = video_name.split("_")
    file_number_video = test[1:]
    name_index = int(file_number_video)
    
    
    transcribed_audio_file_name = f"audio/{video_name}.wav"
    
    if name_index < 13:
        zoom_video_file_name = os.path.join(BASE_PATH, "batch1", "video", f"{video_name}.mp4")
    else:
        zoom_video_file_name = os.path.join(BASE_PATH, "batch2", "video", f"{video_name}.mp4")

    if not os.path.isfile(transcribed_audio_file_name):
        audioclip = AudioFileClip(zoom_video_file_name)
        audioclip.write_audiofile(transcribed_audio_file_name)

    if GET_AUDIO_FILE:
        continue

    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    
    steps = math.ceil(duration / 10)

    r = speech_recognition.Recognizer()
    
    transcript_data = []
    for i in range(steps):
        start_time = i * 10
        with speech_recognition.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=start_time, duration=min(10, duration - start_time))
            try:
                text = r.recognize_google(audio, language='vi').lower()
                transcript_data.append((f'{start_time//60:02}:{start_time%60:02}', text))
            except:
                transcript_data.append((f'{start_time//60:02}:{start_time%60:02}', ""))
        
    bin_file_path = f"transcript/{video_name}.bin"
    with open(bin_file_path, 'wb') as bin_file:
        pickle.dump(transcript_data, bin_file)

    os.remove(transcribed_audio_file_name)
