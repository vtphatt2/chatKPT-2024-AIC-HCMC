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


