from utils import load_dataset, display_dataset
from utils.display_dataset import display_dataset
import os
import fiftyone as fo

images_dir = os.path.join("..", "data")
# dataset = load_dataset.Dataset(dataset_name='AIC_2024',
#                                images_dir=images_dir).load_metadata()
dataset = load_dataset.Dataset(dataset_name='AIC_2024',
                               images_dir=images_dir)
dataset = dataset.get_fo_dataset()
display_dataset(dataset, open_tab=False)