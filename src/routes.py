from flask import render_template, request, redirect, url_for
import os
import csv
import re

SUBMISSION_FOLDER = os.path.join('..', 'submission')

def sort_by_middle_number(file_list):
    def extract_middle_number(filename):
        match = re.search(r'query-p1-(\d+)-', filename)
        if match:
            return int(match.group(1)) 
        return 0  
    
    sorted_list = sorted(file_list, key=extract_middle_number)
    return sorted_list

def init_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        csv_files = [f for f in os.listdir(SUBMISSION_FOLDER) if f.endswith('.csv')]
        csv_files = sort_by_middle_number(csv_files)
        notify_interact_text = ''
        selected_csv_file = request.args.get('file_name')
        returned_text = request.args.get('returned_text', '')

        csv_content = ""
        if selected_csv_file:
            file_path = os.path.join(SUBMISSION_FOLDER, selected_csv_file)
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    csv_content = "\n".join([", ".join(row) for row in reader])  
                notify_interact_text = f"Open {selected_csv_file} successfully !"
            except Exception as e:
                csv_content = f"Error reading file: {str(e)}"

        return render_template('index.html', csv_files=csv_files, selected_csv_file=selected_csv_file, notify_submit_text=returned_text, 
                            csv_content=csv_content, notify_interact_text=notify_interact_text)
    
    @app.route('/save_csv', methods=['POST'])
    def save_csv():
        csv_content = request.form.get('csv_edit_text') 
        selected_csv_file = request.form.get('file_name') 

        print(f"CSV Content: {csv_content}")  # Add this for debugging
        print(f"Selected File: {selected_csv_file}")  # Add this for debugging

        if selected_csv_file:
            file_path = os.path.join(SUBMISSION_FOLDER, selected_csv_file)
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL) 
                    for row in csv_content.split('\n'):
                        clean_row = [field.strip() for field in row.split(',')]
                        writer.writerow(clean_row)
            except Exception as e:
                return f"Error saving file: {str(e)}"
        
        return render_template('index.html', 
                            csv_files=[f for f in os.listdir(SUBMISSION_FOLDER) if f.endswith('.csv')], 
                            selected_csv_file=selected_csv_file, 
                            csv_content=csv_content, 
                            returned_text="",
                            notify_interact_text=f"{selected_csv_file} saved successfully!")
    
    @app.route('/delete_csv', methods=['POST'])
    def delete_csv():
        selected_csv_file = request.form.get('file_name') 
        if selected_csv_file:
            file_path = os.path.join(SUBMISSION_FOLDER, selected_csv_file)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path) 
            except Exception as e:
                return f"Error deleting file: {str(e)}"
        
        return redirect(url_for('home'))

    @app.route('/create_file', methods=['POST'])
    def create_file():
        file_name = request.form.get('file_name')
        if file_name:
            file_path = os.path.join(SUBMISSION_FOLDER, file_name)
            try:
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as new_file:
                        new_file.write("") 
            except Exception as e:
                return f"Error creating file: {str(e)}"

        return redirect(url_for('home')) 

