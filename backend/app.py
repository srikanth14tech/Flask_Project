import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/users', methods=['GET'])
def get_users():
    users=[
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    return jsonify(users), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Get Azure credentials from .env
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
        
        # Initialize blob client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        
        # Upload file
        blob_client.upload_blob(file, overwrite=True)
        
        return jsonify({"message": f"File {file.filename} uploaded successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ This should NOT be indented inside the function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
