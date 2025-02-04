from login import getSessionID, getEvaluationID
import getpass
from rapidfuzz import fuzz

username = "team22"
password = "MMxyYefPZk"
session_id = getSessionID.get_session_id(username, password)
if session_id:
    print(f"Login successful!")
    evaluation_id = getEvaluationID.get_evaluation_id(session_id)
    if evaluation_id:
        print(f"Evaluation ID: {evaluation_id}")
else:
    print("Failed to retrieve the session ID.")

print("[1] Load libraries")
from utils import dataset_manager, model_manager
from utils import utils
import os
from flask import Flask, request, jsonify
from routes.interact_with_csv_files import csv_routes
from deep_translator import GoogleTranslator
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import re

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
def searchByText(text_query, k = 100, discarded_videos = "", keywords = ""):
    submission_list = []
    text_embedding = model_clip14.inference(text_query)

    discarded_set = set(video.strip() for video in discarded_videos.split(','))
    keywords_list = []
    if (keywords != ""):
        keywords_list = keywords.split(', ')

    dataset = dataset_manager.get_dataset()
    results = []
    for video_name, embeddings_array in dataset_manager.get_video_clip14_embedding_dict().items():
        if (video_name in discarded_set):
            continue

        if ("batch 1" in discarded_set):
            if (int(video_name[1:3]) <= 12):
                continue

        if ("batch 2" in discarded_set):
            if (int(video_name[1:3]) <= 24 and int(video_name[1:3]) >= 13):
                continue

        if ("batch 3" in discarded_set):
            if (int(video_name[1:3]) >= 25):
                continue
        
        for i in range(0, len(embeddings_array)):
            score = np.dot(text_embedding, embeddings_array[i])
            results.append((video_name, i, score))

    results.sort(key=lambda item: item[2], reverse=True)

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    video_transcript_dict = dataset_manager.get_video_transcript_dict()
    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            left = results[i][1]
            right = results[i][1]
            visited[i] = True
            video_name = results[i][0]
            
            transcript = utils.concatenate_surrounding_strings(video_transcript_dict[video_name], dataset[video_name][results[i][1]]['frame_id'], video_fps_dict[video_name])
            if (len(keywords_list) != 0):
                if not utils.contains_keyword_fuzzy(transcript, keywords_list, threshold=85):
                    continue

                transcript = utils.highlight_keywords(transcript, keywords_list)

            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])], video_fps_dict[video_name], transcript]

            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    left = min(left, results[j][1])
                    right = max(right, results[j][1])
                    visited[j] = True
            
            if (len(x[2]) < 6) :
                low = max(0, left - 2)
                high = min(right + 3, len(dataset[video_name]))
                for i in range(low, left):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))
                for i in range(right + 1, high):
                    x[2].append((dataset[video_name][i]['filepath'], dataset[video_name][i]['frame_id']))

            x[2] = sorted(x[2], key=lambda a:a[1])
            submission_list.append(x)
    
    return submission_list

def temporalSearch(text_first_this, text_then_that, k = 100, range_size = 8, discarded_videos = "", keywords = ""):
    submission_list = []
    x = model_clip14.inference(text_first_this)
    y = model_clip14.inference(text_then_that)
    
    keywords_list = []
    if (keywords != ""):
        keywords_list = keywords.split(',')

    discarded_set = set(video.strip() for video in discarded_videos.split(','))

    results = []
    for video_name, embeddings_array in dataset_manager.get_video_clip14_embedding_dict().items():
        if (video_name in discarded_set):
            continue

        if ("batch 1" in discarded_set):
            if (int(video_name[1:3]) <= 12):
                continue

        if ("batch 2" in discarded_set):
            if (int(video_name[1:3]) <= 24 and int(video_name[1:3]) >= 13):
                continue

        if ("batch 3" in discarded_set):
            if (int(video_name[1:3]) >= 25):
                continue

        # num_vectors = len(embeddings_array)
        # sub_size = int(0.65 * range_size + 1)
        # window1 = np.sum(embeddings_array[0:sub_size], axis=0)
        # window2 = np.sum(embeddings_array[(range_size - sub_size):range_size], axis=0)
        # x_cos_sim = cosine_similarity([x], [window1])[0][0]
        # y_cos_sim = cosine_similarity([y], [window2])[0][0]
        # index = 0
        # j = range_size
        # results.append((x_cos_sim * y_cos_sim, video_name, index))
        # while j < num_vectors - 1:
        #     index += 1
        #     j += 1

        #     x_cos_sim -= cosine_similarity([x], [embeddings_array[index - 1]])[0][0]
        #     x_cos_sim += cosine_similarity([x], [embeddings_array[index + sub_size]])[0][0]

        #     y_cos_sim -= cosine_similarity([y], [embeddings_array[j - sub_size]])[0][0]
        #     y_cos_sim += cosine_similarity([y], [embeddings_array[j]])[0][0]

        #     results.append((x_cos_sim * y_cos_sim, video_name, index))

        num_vectors = len(embeddings_array)
        prefix_sum_embedding = [embeddings_array[0]]
        for i in range(1, num_vectors):
            prefix_sum_embedding.append(prefix_sum_embedding[i - 1] + embeddings_array[i])

        for i in range(0, num_vectors - range_size + 1, int(range_size / 2)):
            x_cos_sim = cosine_similarity([x], [prefix_sum_embedding[i + int(0.65 * range_size)] - prefix_sum_embedding[i]])[0]
            y_cos_sim = cosine_similarity([y], [prefix_sum_embedding[i + range_size - 1] - prefix_sum_embedding[i + int(0.35 * range_size)]])[0]
            results.append((x_cos_sim + y_cos_sim, video_name, i))

        # for i in range(0, num_vectors - range_size + 1, int(range_size / 2)):
        #     block = embeddings_array[i:i+range_size]
        #     x_cos_sim = cosine_similarity([x], block[:int(0.65 * range_size)])[0]
        #     y_cos_sim = cosine_similarity([y], block[int(0.35 * range_size):])[0]
        #     block_similarity = (np.max(x_cos_sim) + np.max(y_cos_sim)) / 2

        # for i in range(0, num_vectors - range_size + 1, int(range_size / 2)):
        #     block = embeddings_array[i:i+range_size]
        #     x_cos_sim = cosine_similarity([x], block[:int(0.65 * range_size)])[0]
        #     y_cos_sim = cosine_similarity([y], block[int(0.35 * range_size):])[0]
        #     block_similarity = (np.max(x_cos_sim) * np.max(y_cos_sim))
            
        #     results.append((block_similarity, video_name, i))

    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:k]

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    video_transcript_dict = dataset_manager.get_video_transcript_dict()
    dataset = dataset_manager.get_dataset()
    # existed_video = set()
    for similarity, video_name, best_index in top_results:
        transcript = utils.concatenate_surrounding_strings(video_transcript_dict[video_name], dataset[video_name][best_index]['frame_id'], video_fps_dict[video_name])
        if (len(keywords_list) != 0):
            if not utils.contains_keyword_fuzzy(transcript, keywords_list, threshold=85):
                continue
            transcript = utils.highlight_keywords(transcript, keywords_list)

        # if (video_name in existed_video):
        #     continue

        x = [video_name, video_youtube_link_dict[video_name], [], video_fps_dict[video_name], transcript]  
        # existed_video.add(video_name)  
        for j in range(best_index, best_index + range_size):
            x[2].append((dataset[video_name][j]['filepath'], dataset[video_name][j]['frame_id']))
        submission_list.append(x)
    
    return submission_list

def searchByTextAndSketch(text_query, sketch_image, k = 200, discarded_videos = "", keywords = ""):
    submission_list = []
    embedding = [model_task_former.inference(text_query, sketch_image)]

    discarded_set = set(video.strip() for video in discarded_videos.split(','))
    keywords_list = []
    if (keywords != ""):
        keywords_list = keywords.split(',')

    dataset = dataset_manager.get_dataset()
    results = []
    for video_name, embeddings_array in dataset_manager.get_video_task_former_embedding_dict().items():
        if (video_name in discarded_set):
            continue

        if ("batch 1" in discarded_set):
            if (int(video_name[1:3]) <= 12):
                continue

        if ("batch 2" in discarded_set):
            if (int(video_name[1:3]) <= 24 and int(video_name[1:3]) >= 13):
                continue

        if ("batch 3" in discarded_set):
            if (int(video_name[1:3]) >= 25):
                continue
        
        sim_scores = cosine_similarity(embedding, embeddings_array).flatten()
        for index, score in enumerate(sim_scores):
            results.append((video_name, index, score))

    results.sort(key=lambda item: item[2], reverse=True)

    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    video_transcript_dict = dataset_manager.get_video_transcript_dict()
    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            left = results[i][1]
            right = results[i][1]
            visited[i] = True
            video_name = results[i][0]

            transcript = utils.concatenate_surrounding_strings(video_transcript_dict[video_name], dataset[video_name][results[i][1]]['frame_id'], video_fps_dict[video_name])
            if (len(keywords_list) != 0):
                if not utils.contains_keyword_fuzzy(transcript, keywords_list, threshold=85):
                    continue

                transcript = utils.highlight_keywords(transcript, keywords_list)

            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])], video_fps_dict[video_name], transcript]

            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    left = min(left, results[j][1])
                    right = max(right, results[j][1])
                    visited[j] = True
            
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

def searchByTranscript(keywords = "", k = 200,):
    keywords = keywords.split(', ')

    submission_list = []
    
    video_transcript_dict = dataset_manager.get_video_transcript_dict()
    results = []
    for video_name, transcript_list in video_transcript_dict.items():
        for i in range(0, len(transcript_list) - 1, 2):
            text = transcript_list[i][1] + " " + transcript_list[i + 1][1]
            results.append((video_name, i, utils.count_keywords_in_string(keywords, text), text))
    results.sort(key=lambda item: item[2], reverse=True)

    dataset = dataset_manager.get_dataset()
    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    for i in range(0, k):
        video_name = results[i][0]
        target_frame_id = utils.time_to_seconds(video_transcript_dict[video_name][results[i][1]][0]) * video_fps_dict[video_name]
        transcript = utils.highlight_keywords(results[i][3], keywords)
        x = [video_name, video_youtube_link_dict[video_name], [], video_fps_dict[video_name], transcript]
        closest_index = utils.find_closest_frame_index(dataset[video_name], target_frame_id)

        for j in range(closest_index, min(closest_index + 15, len(dataset[video_name]))):
            x[2].append((dataset[video_name][j]['filepath'], dataset[video_name][j]['frame_id']))
            
        submission_list.append(x)

    return submission_list

def searchByOCR(words = "", k = 200):
    data = request.json
    words = data.get('words')
    k = data.get('k')

    words = words.split(', ')
    words = [utils.remove_diacritics_and_lowercase(word).replace(" ", "") for word in words]

    results = []
    video_ocr_dict = dataset_manager.get_video_ocr_dict()
    for video_name, words_list in video_ocr_dict.items():
        for i in range(0, len(words_list)):
            score = -1
            for word in words:
                for w in words_list[i]:
                    w.replace(" ", "")
                    score = max(score, utils.similarity_score_two_words(word, w))

            results.append((video_name, i, score))
    results.sort(key=lambda item: item[2], reverse=True)

    submission_list = []
    dataset = dataset_manager.get_dataset()
    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    video_transcript_dict = dataset_manager.get_video_transcript_dict()
    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            visited[i] = True
            video_name = results[i][0]
            transcript = utils.concatenate_surrounding_strings(video_transcript_dict[video_name], dataset[video_name][results[i][1]]['frame_id'], video_fps_dict[video_name])
            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])], video_fps_dict[video_name], transcript]
            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    visited[j] = True

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
    translated_text = translator.translate(search_text)
    keywords = data.get('keywords')
    k = int(data.get('k'))
    submission_list = searchByText(translated_text, k=k, discarded_videos=discarded_videos, keywords=keywords) 

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
    translated_first_this = translator.translate(text_first_this)
    translated_then_that = translator.translate(text_then_that)
    keywords = data.get('keywords')
    k = int(data.get('k'))

    submission_list = temporalSearch(translated_first_this, translated_then_that, k=k, range_size=20,
                                     discarded_videos=discarded_videos, keywords=keywords)

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
    keywords = data.get('keywords')
    k = int(data.get('k'))

    translated_text = translator.translate(text_query)

    if sketch_image:
        header, encoded = sketch_image.split(',', 1)  # Tách phần header (data:image/png;base64)
        sketch_image_data = base64.b64decode(encoded)  # Giải mã dữ liệu base64
        sketch_image = Image.open(BytesIO(sketch_image_data))  # Tạo ảnh từ dữ liệu

        # Lưu ảnh để kiểm tra (tùy chọn)
        sketch_image.save("received_sketch.png")
        
    submission_list = searchByTextAndSketch(translated_text, sketch_image, k=k, discarded_videos=discarded_videos, keywords=keywords)

    # Prepare and return the response
    response = jsonify({
        "translated_text": translated_text,
        "submission_list": submission_list
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response, 200

@app.route('/find_similar_images', methods=['POST'])
def find_similar_images():
    data = request.json
    selectedImagesList = data.get('selectedImagesList')
    k = data.get('k')
    discarded_videos = data.get('discardedVideos')
    discarded_set = set(video.strip() for video in discarded_videos.split(','))

    dataset = dataset_manager.get_dataset()
    video_clip14_embedding_dict =  dataset_manager.get_video_clip14_embedding_dict()
    representative_score = np.zeros(768, dtype=np.float32)
    for item in selectedImagesList:
        video_name = re.search(r'L\d+_V\d+', item.get('video_name')).group() if re.search(r'L\d+_V\d+', item.get('video_name')) else None     
        # video_name = item.get('video_name').rsplit(os.sep, 2)[-2]
        frame_id = int(item.get('frame_id'))
        index = 0
        while (index < len(dataset[video_name]) and dataset[video_name][index]['frame_id'] != frame_id):
            index += 1
        representative_score += video_clip14_embedding_dict[video_name][index]

    results = []
    for video_name, embeddings_array in video_clip14_embedding_dict.items():  
        if ("batch 1" in discarded_set):
            if (int(video_name[1:3]) <= 12):
                continue

        if ("batch 2" in discarded_set):
            if (int(video_name[1:3]) <= 24 and int(video_name[1:3]) >= 13):
                continue

        if ("batch 3" in discarded_set):
            if (int(video_name[1:3]) >= 25):
                continue

        sim_scores = cosine_similarity([representative_score], embeddings_array).flatten()
        for index, score in enumerate(sim_scores):
            results.append((video_name, index, score))

    results.sort(key=lambda item: item[2], reverse=True)

    submission_list = []
    video_youtube_link_dict = dataset_manager.get_video_youtube_link_dict()
    video_fps_dict = dataset_manager.get_video_fps_dict()
    video_transcript_dict = dataset_manager.get_video_transcript_dict()

    item = selectedImagesList[0]
    video_name = re.search(r'L\d+_V\d+', item.get('video_name')).group() if re.search(r'L\d+_V\d+', item.get('video_name')) else None  
    frame_id = int(item.get('frame_id'))
    index = 0
    while (index < len(dataset[video_name]) and dataset[video_name][index]['frame_id'] != frame_id):
        index += 1
    transcript = utils.concatenate_surrounding_strings_special(video_transcript_dict[video_name], dataset[video_name][index]['frame_id'], video_fps_dict[video_name])
    index = max(0, index - 10)
    n = min(len(dataset[video_name]), index + 36)
    x = [video_name, video_youtube_link_dict[video_name], [], video_fps_dict[video_name], transcript]
    while (index < n):
        x[2].append((dataset[video_name][index]['filepath'], dataset[video_name][index]['frame_id']))
        index += 1
    submission_list.append(x)

    visited = [False] * k
    for i in range(0, k):
        if (not visited[i]):
            visited[i] = True
            video_name = results[i][0]
            transcript = utils.concatenate_surrounding_strings(video_transcript_dict[video_name], dataset[video_name][results[i][1]]['frame_id'], video_fps_dict[video_name])

            x = [video_name, video_youtube_link_dict[video_name], [(dataset[video_name][results[i][1]]['filepath'], dataset[video_name][results[i][1]]['frame_id'])], video_fps_dict[video_name], transcript]

            for j in range(i + 1, k):
                if (not visited[j] and video_name == results[j][0] and abs(results[i][1] - results[j][1]) < 12):
                    x[2].append((dataset[video_name][results[j][1]]['filepath'], dataset[video_name][results[j][1]]['frame_id']))
                    visited[j] = True

            x[2] = sorted(x[2], key=lambda a:a[1])
            submission_list.append(x)

    # Prepare and return the response
    response = jsonify({
        "submission_list": submission_list
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response, 200

@app.route('/search_by_transcript', methods=['POST'])
def search_by_transcript():
    data = request.json
    k = data.get('k')
    keywords = data.get('keywords')

    submission_list = searchByTranscript(keywords, k)

    response = jsonify({
        "submission_list": submission_list
    })
    return response, 200

@app.route('/search_by_ocr', methods=['POST'])
def search_by_ocr():
    data = request.json
    k = data.get('k')
    words = data.get('keywords')

    submission_list = searchByOCR(words, k)

    response = jsonify({
        "submission_list": submission_list
    })
    return response, 200

@app.route('/submit_to_system', methods=['POST'])
def submit_to_system():
    data = request.json
    video_name = data.get('video_name')
    video_fps_dict = dataset_manager.get_video_fps_dict()

    response = jsonify({
        "session_id": session_id,
        "evaluation_id": evaluation_id,
        "fps": video_fps_dict[video_name]
    })
    return response, 200


app.run(debug=True, use_reloader=False)