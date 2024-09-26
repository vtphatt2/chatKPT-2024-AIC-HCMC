import os

class SampleImage:
    def __init__(self, filepath):
        self.filepath = filepath
        _, self.video, self.frame_id = self.filepath[:-4].rsplit(os.sep, 2)

        print(f"\rFinish {self.video} with frame_id {self.frame_id}...", end='', flush=True)

    def __getitem__(self, key):
        if key == 'filepath':
            return self.filepath
        if key == 'video':
            return self.video
        if key == 'frame_id':
            return self.frame_id
        else:
            raise KeyError(f"Key '{key}' not found.")
    
