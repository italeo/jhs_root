from flask import Flask, request, jsonify, render_template
import os
import zipfile
import shutil
from graphs.cluster_graph import create_cluster_chat_graph
from graphs.sentiment_graph import generate_sentiment_graph
from graphs.popularities_graph import generate_popularity_graph  # Import the population graph function
import plotly.io as pio

app = Flask(__name__)

# Define the path to the temp folder
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')

# Ensure the temp directory exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route("/")
def home():
    return "Hello, Flask is running!", 200

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Clear out the temp directory before saving the new upload
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to delete {file_path}. Reason: {str(e)}"}), 500

    file_path = os.path.join(TEMP_DIR, file.filename)
    file.save(file_path)

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR)

        all_files = []
        csv_and_txt_files = []
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), TEMP_DIR)
                
                # Skip __MACOSX and hidden files (those starting with .)
                if rel_path.startswith("__MACOSX") or os.path.basename(rel_path).startswith('.'):
                    continue
                
                all_files.append(rel_path)
                if file.endswith('.csv') or file.endswith('.txt'):
                    csv_and_txt_files.append(rel_path)

        if not csv_and_txt_files:
            return jsonify({"error": "No CSV or TXT files found"}), 200

        return jsonify({"files": csv_and_txt_files, "all_files": all_files}), 200
    else:
        return jsonify({"error": "Uploaded file is not a valid zip file"}), 400

@app.route("/api/generate_sent_graph", methods=["POST"])
def generate_sent_graph():
    # Dynamically find the relevant CSV file
    try:
        # Generate population graph
        population_fig = generate_sentiment_graph(TEMP_DIR)
        population_graph_json = pio.to_json(population_fig)

        # Return the population graph
        return jsonify({"graph": population_graph_json}), 200

    except Exception as e:
        print(f"Error generating graph: {e}")
        return jsonify({"error": f"Failed to generate graph: {str(e)}"}), 500
    
@app.route("/api/generate_pop_graph", methods=["POST"])
def generate_pop_graph():
    # Dynamically find the relevant CSV file
    try:
        # Generate population graph
        population_fig = generate_popularity_graph(TEMP_DIR)
        population_graph_json = pio.to_json(population_fig)

        # Return the population graph
        return jsonify({"graph": population_graph_json}), 200

    except Exception as e:
        print(f"Error generating graph: {e}")
        return jsonify({"error": f"Failed to generate graph: {str(e)}"}), 500
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
