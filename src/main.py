print("[1] Load libraries")
from utils import dataset_manager, model_manager
import os
from flask import Flask, request, jsonify
from routes.interact_with_csv_files import csv_routes
from deep_translator import GoogleTranslator
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import base64
from io import BytesIO
from PIL import Image

SUBMISSION_FOLDER = os.path.join("..", "submission")

print("[2] Load dataset")
data_dir = os.path.join(os.getcwd(), '..', 'data') # link to 'data' folder, remember to organize as described in Github
# data_dir = '/Users/VoThinhPhat/Desktop/data'
dataset_manager = dataset_manager.Dataset(data_dir=data_dir)


print("\n[3] Load models and translator")
# clip vit large patch14 model
model_clip14 = model_manager.CLIP_14_model()

# remember to download model_config_file and model_file (contact vtphatt2 for link)
model_config_file = os.path.join(os.getcwd(), 'task-former', 'code', 'training', 
                                 'model_configs', 'ViT-B-16.json')
model_file = os.path.join(os.getcwd(), 'task-former', 'model', 'tsbir_model_final.pt')
model_task_former = model_manager.TASK_former_model(model_config_file=model_config_file,
                                                    model_file=model_file)

# traslate from Vietnames to English
translator = GoogleTranslator(source='vi', target='en')


print("[4] Load functions")
def searchByText(text_query, k = 200, discarded_videos = "", output_file = ""):
    submission_list = []
    text_embedding = [model_clip14.inference(text_query)]

    discarded_set = set(video.strip() for video in discarded_videos.split(','))

    dataset = dataset_manager.get_dataset()
    results = []
    for video_name, embeddings_array in dataset_manager.get_video_clip14_embedding_dict().items():
        if (video_name in discarded_set):
            continue
        
        sim_scores = cosine_similarity(text_embedding, embeddings_array).flatten()
        for index, score in enumerate(sim_scores):
            results.append((video_name, index, score))

    results.sort(key=lambda item: item[2], reverse=True)

    if (output_file != "" and output_file.endswith('.csv')):
        output_file = os.path.join(SUBMISSION_FOLDER, output_file)
        with open(output_file, 'w') as file:
            pass  

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            left = results[i][1]
            right = results[i][1]
            visited[i] = True
            video_name = results[i][0]
            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])]]

            if (output_file != "" and output_file.endswith('.csv')):
                with open(output_file, 'a') as file:
                    file.write(f"{video_name},{dataset[video_name][results[i][1]]['frame_id']}\n")

            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    left = min(left, results[j][1])
                    right = max(right, results[j][1])
                    visited[j] = True

                    if (output_file != "" and output_file.endswith('.csv')):
                        with open(output_file, 'a') as file:
                            file.write(f"{video_name},{dataset[video_name][results[j][1]]['frame_id']}\n")
            
            if (len(x[2]) < 5) :
                low = max(0, left - 2)
                high = min(right + 3, len(dataset[video_name]))
                for i in range(low, left):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))
                for i in range(right + 1, high):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))

            x[2] = sorted(x[2], key=lambda a:a[1])
            submission_list.append(x)
    
    return submission_list

def temporalSearch(text_first_this, text_then_that, k = 100, range_size = 8, discarded_videos = "", output_file = ""):
    submission_list = []
    x = model_clip14.inference(text_first_this)
    y = model_clip14.inference(text_then_that)

    discarded_set = set(video.strip() for video in discarded_videos.split(','))

    if (output_file != "" and output_file.endswith('.csv')):
        output_file = os.path.join(SUBMISSION_FOLDER, output_file)
        with open(output_file, 'w') as file:
            pass 

    results = []
    for video_name, embeddings_array in dataset_manager.get_video_clip14_embedding_dict().items():
        if (video_name in discarded_set):
            continue

        num_vectors = len(embeddings_array)
        for i in range(0, num_vectors - range_size + 1, int(range_size / 2)):
            block = embeddings_array[i:i+range_size]
            x_cos_sim = cosine_similarity([x], block[:int(0.65 * range_size)])[0]
            y_cos_sim = cosine_similarity([y], block[int(0.35 * range_size):])[0]
            block_similarity = (np.max(x_cos_sim) + np.max(y_cos_sim)) / 2
            
            results.append((block_similarity, video_name, i))

    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:k]

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    dataset = dataset_manager.get_dataset()
    for similarity, video_name, best_index in top_results:
        x = [video_name, video_youtube_link_dict[video_name], []]
        if (output_file != "" and output_file.endswith('.csv')):
            with open(output_file, 'a') as file:
                file.write(f"{video_name},{dataset[video_name][best_index + int(0.12 * range_size)]['frame_id']}\n")        
        for j in range(best_index, best_index + range_size):
            x[2].append((dataset[video_name][j]['filepath'], dataset[video_name][j]['frame_id']))
        submission_list.append(x)
    
    return submission_list

def searchByTextAndSketch(text_query, sketch_image, k = 200, discarded_videos = "", output_file = ""):
    submission_list = []
    embedding = [model_task_former.inference(text_query, sketch_image)]

    discarded_set = set(video.strip() for video in discarded_videos.split(','))

    dataset = dataset_manager.get_dataset()
    results = []
    for video_name, embeddings_array in dataset_manager.get_video_task_former_embedding_dict().items():
        if (video_name in discarded_set):
            continue
        
        sim_scores = cosine_similarity(embedding, embeddings_array).flatten()
        for index, score in enumerate(sim_scores):
            results.append((video_name, index, score))

    results.sort(key=lambda item: item[2], reverse=True)

    if (output_file != "" and output_file.endswith('.csv')):
        output_file = os.path.join(SUBMISSION_FOLDER, output_file)
        with open(output_file, 'w') as file:
            pass  

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            left = results[i][1]
            right = results[i][1]
            visited[i] = True
            video_name = results[i][0]
            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])]]

            if (output_file != "" and output_file.endswith('.csv')):
                with open(output_file, 'a') as file:
                    file.write(f"{video_name},{dataset[video_name][results[i][1]]['frame_id']}\n")

            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    print((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    left = min(left, results[j][1])
                    right = max(right, results[j][1])
                    visited[j] = True

                    if (output_file != "" and output_file.endswith('.csv')):
                        with open(output_file, 'a') as file:
                            file.write(f"{video_name},{dataset[video_name][results[j][1]]['frame_id']}\n")
            
            if (len(x[2]) < 5) :
                low = max(0, left - 2)
                high = min(right + 3, len(dataset[video_name]))
                for i in range(low, left):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))
                for i in range(right + 1, high):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))

            x[2] = sorted(x[2], key=lambda a:a[1])
            submission_list.append(x)
    
    return submission_list

print("[5] Launch the local Web UI")
app = Flask(__name__)

# Register the blueprint with the main app
app.register_blueprint(csv_routes)

@app.route('/search_by_text', methods=['POST'])
def search_by_text():
    data = request.json
    search_text = data.get('searchText') 
    discarded_videos = data.get('discardedVideos')
    new_file_name = data.get('newFileName')
    translated_text = translator.translate(search_text)
    submission_list = searchByText(translated_text, k=100, discarded_videos=discarded_videos, output_file=new_file_name)  # Ensure this returns an ordered dict if necessary

    response = jsonify({
        "translated_text": translated_text,
        "submission_list": submission_list  # Use a list instead of a dict
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response, 200

@app.route('/temporal_search', methods=['POST'])
def temporal_search():
    # Extract the request data
    data = request.json
    text_first_this = data.get('textFirstThis')
    text_then_that = data.get('textThenThat')
    discarded_videos = data.get('discardedVideos')
    new_file_name = data.get('newFileName')
    translated_first_this = translator.translate(text_first_this)
    translated_then_that = translator.translate(text_then_that)

    submission_list = temporalSearch(translated_first_this, translated_then_that, k=100, range_size=20,
                                     discarded_videos=discarded_videos, output_file=new_file_name)

    # Prepare and return the response
    response = jsonify({
        "translated_first_this": translated_first_this,
        "translated_then_that": translated_then_that,
        "submission_list": submission_list
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response, 200

@app.route('/search_text_and_sketch', methods=['POST'])
def search_by_text_and_sketch():
    # Extract the request data
    data = request.json
    text_query = data.get('textSearch')
    sketch_image = data.get('sketch')
    discarded_videos = data.get('discardedVideos')
    new_file_name = data.get('newFileName')

    translated_text = translator.translate(text_query)

    if sketch_image:
        header, encoded = sketch_image.split(',', 1)  # Tách phần header (data:image/png;base64)
        sketch_image_data = base64.b64decode(encoded)  # Giải mã dữ liệu base64
        sketch_image = Image.open(BytesIO(sketch_image_data))  # Tạo ảnh từ dữ liệu

        # Lưu ảnh để kiểm tra (tùy chọn)
        sketch_image.save("received_sketch.png")
        
    submission_list = searchByTextAndSketch(text_query, sketch_image, k=100, discarded_videos=discarded_videos, output_file=new_file_name)

    # Prepare and return the response
    response = jsonify({
        "translated_text": translated_text,
        "submission_list": submission_list
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response, 200

app.run(debug=True, use_reloader=False)