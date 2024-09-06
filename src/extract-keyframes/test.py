import cv2
import os

def get_and_save_frame(video_path, frame_id, save_path, filename):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame {frame_id}.")
        cap.release()
        return
    os.makedirs(save_path, exist_ok=True)
    save_file_path = os.path.join(save_path, filename)
    cv2.imwrite(save_file_path, frame)
    print(f"Frame {frame_id} saved successfully at {save_file_path}.")
    cap.release()

# Example usage
video_path = '/Users/VoThinhPhat/Desktop/chatKPT-2024-AIC-HCMC/data/batch1/video/Videos_L01/L01_V001.mp4'  # Path to your video file
frame_id = 5  # Frame number to extract
save_path = 'keyframes'  # Folder where the frame will be saved
filename = '0001.jpg'  # Desired filename for the saved frame

get_and_save_frame(video_path, frame_id, save_path, filename)
