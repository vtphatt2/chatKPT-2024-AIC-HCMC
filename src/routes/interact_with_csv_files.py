from flask import Blueprint, render_template, request, jsonify
import re
import os

SUBMISSION_FOLDER = os.path.join(os.getcwd(), "..", "submission")

# Create a blueprint
csv_routes = Blueprint('csv_routes', __name__)

# Useful functions
def sort_by_middle_number(file_list):
    def extract_middle_number(filename):
        # Modify regex to capture p followed by any number
        match = re.search(r'query-p(\d+)-(\d+)-', filename)
        if match:
            # Extract both the `pX` part and the middle number
            p_number = int(match.group(1))  # Number after 'p'
            middle_number = int(match.group(2))  # Middle number after '-pX-'
            return (p_number, middle_number)
        return (0, 0)  # Return tuple for cases where match is not found
    
    # Sort by both the p number and the middle number
    sorted_list = sorted(file_list, key=extract_middle_number)
    return sorted_list

def get_current_csv_files():
    csv_files = [f for f in os.listdir(SUBMISSION_FOLDER) if f.endswith('.csv')]
    csv_files = sort_by_middle_number(csv_files)
    return csv_files

# Define routes here
@csv_routes.route('/')
def home():
    csv_files = get_current_csv_files()
    return render_template('index.html', csv_files=csv_files)

@csv_routes.route('/get_csv_content', methods=['POST'])
def get_csv_content():
    filename = request.json.get('filename')
    file_path = os.path.join(SUBMISSION_FOLDER, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return {'content': content}, 200
    else:
        return {'error': 'File not found'}, 404
    
@csv_routes.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')
    
    file_path = os.path.join(SUBMISSION_FOLDER, filename)
    
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"message": "File saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@csv_routes.route('/delete_csv', methods=['POST'])
def delete_csv():
    data = request.json
    filename = data.get('filename')
    
    file_path = os.path.join(SUBMISSION_FOLDER, filename)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "File deleted successfully!"}), 200
        else:
            return jsonify({"error": "File not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@csv_routes.route('/create_csv', methods=['POST'])
def create_csv():
    data = request.json
    filename = data.get('filename')

    # Ensure the filename ends with ".csv"
    if not filename.endswith('.csv'):
        return jsonify({"error": "Filename must end with .csv"}), 400
    
    file_path = os.path.join(SUBMISSION_FOLDER, filename)

    if os.path.exists(file_path):
        return jsonify({"error": "File already exists"}), 400
    else:
        try:
            # Create an empty file
            with open(file_path, 'w') as file:
                file.write("")  # Write an empty string to create the file
            
            return jsonify({"message": "File created successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

