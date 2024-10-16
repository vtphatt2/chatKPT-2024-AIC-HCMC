import unicodedata
import re
from rapidfuzz import fuzz, process

def time_difference(start: str, end: str) -> int:
    def convert_to_seconds(time_str: str) -> int:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds

    start_seconds = convert_to_seconds(start)
    end_seconds = convert_to_seconds(end)
    
    difference = end_seconds - start_seconds
    
    return abs(difference)

def count_substrings(s: str, a: list) -> int:
    total_count = 0
    s_lower = s.lower() 
    
    for substring in a:
        total_count += s_lower.count(substring.lower())  
    
    return total_count

def time_to_seconds(time_str: str) -> int:
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def find_closest_tuple_index(tuples_list, frame_id, fps):
    target_time = frame_id / fps
    closest_index = None
    closest_diff = float('inf')
    
    for index, (time_str, _) in enumerate(tuples_list):
        current_time = time_to_seconds(time_str)
        diff = abs(current_time - target_time)
        
        if diff < closest_diff:
            closest_diff = diff
            closest_index = index
            
    return closest_index

def concatenate_surrounding_strings(tuples_list, frame_id, fps):
    closest_index = find_closest_tuple_index(tuples_list, frame_id, fps)
    
    if closest_index is None:
        return ''
    
    # Get indices for concatenation
    start_index = max(0, closest_index - 1)
    end_index = min(len(tuples_list), closest_index + 2)  # +2 to include the next one
    
    # Extract the strings to concatenate
    strings_to_concatenate = [tup[1] for tup in tuples_list[start_index:end_index]]
    
    return ' '.join(strings_to_concatenate)

def normalize_text(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join([char for char in text if not unicodedata.combining(char)])
    text = text.lower()
    return text

def count_keywords_in_string(keywords, text):
    normalized_text = normalize_text(text)
    total_count = 0
    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)
        matches = re.findall(re.escape(normalized_keyword), normalized_text)
        total_count += len(matches)
    return total_count

def find_closest_frame_index(samples, target_frame_id):
    min_diff = float('inf')
    min_index = -1
    for i, sample in enumerate(samples):
        diff = abs(sample['frame_id'] - target_frame_id)
        if diff < min_diff:
            min_diff = diff
            min_index = i
    return min_index

def remove_diacritics_and_lowercase(word):
    nfkd_form = unicodedata.normalize('NFD', word)
    
    without_diacritics = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    return without_diacritics.lower()

def is_substring_in_set(word, words_set):
    for w in words_set:
        if word in w:
            return True
    return False

def is_similar_rapidfuzz(word, word_set, threshold=80):    
    for w in word_set:        
        # Kiểm tra nếu 'word' là substring của 'w' hoặc 'w' là substring của 'word'
        if word in w:
            return True
        
        score = fuzz.token_sort_ratio(word, w)
        if score >= threshold:
            return True
    
    return False


def is_similar_two_words(a, b, threshold=75):
    a_lower = a.lower().replace(" ", "")
    b_lower = b.lower().replace(" ", "")
    
    if a_lower in b_lower:
        return True
    
    similarity_score = fuzz.token_sort_ratio(a_lower, b_lower)
    
    if similarity_score >= threshold:
        return True
    
    return False

def similarity_score_two_words(a, b):
    if a in b:
        return 100
    return fuzz.token_sort_ratio(a, b)