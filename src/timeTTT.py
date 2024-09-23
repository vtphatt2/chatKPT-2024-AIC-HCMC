def convert_seconds(seconds):
    seconds = seconds/25
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds


seconds = 7689
minutes, remaining_seconds = convert_seconds(seconds)
print(f"{seconds} giây tương đương với {minutes} phút và {remaining_seconds} giây.")



