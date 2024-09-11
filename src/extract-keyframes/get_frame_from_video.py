import cv2

def save_keyframe(video_path, frame_id, output_path):
    """
    Extract and save a specific frame from the video.
    
    :param video_path: Path to the video file.
    :param frame_id: The frame ID to extract.
    :param output_path: Path to save the extracted frame.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Set the frame position to the desired frame ID
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

    # Read the frame
    ret, frame = cap.read()
    
    if ret:
        # Save the frame to the output path
        cv2.imwrite(output_path, frame)
        print(f"Frame {frame_id} saved successfully to {output_path}.")
    else:
        print(f"Error: Could not retrieve frame {frame_id}.")
    
    # Release the video capture object
    cap.release()

# Example usage:
video_path = '/Users/VoThinhPhat/Desktop/chatKPT-2024-AIC-HCMC/data/batch1/video/Videos_L01/L01_V001.mp4'  # Replace with your video path
frame_id = 24495                        # Replace with the desired frame ID
output_path = 'output_frame.jpg'       # Replace with the desired output path

save_keyframe(video_path, frame_id, output_path)
