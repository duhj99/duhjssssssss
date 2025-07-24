from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import os
import shutil
import uuid
import tempfile
from werkzeug.utils import secure_filename

# 创建临时目录用于存储上传和处理的文件
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'batch-toolbox')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

app = Flask(__name__, static_folder='.')
CORS(app)  # 启用CORS以允许前端访问API

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {
    'word': {'docx', 'doc'},
    'excel': {'xlsx', 'xls'},
    'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'},
    'all': {'docx', 'doc', 'xlsx', 'xls', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
}

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def create_temp_dir():
    """创建一个唯一的临时目录"""
    temp_dir = os.path.join(TEMP_DIR, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/health')
def health_check():
    """健康检查API"""
    return jsonify({"status": "ok"})

# 文件上传API
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    files = request.files.getlist('files[]')
    file_type = request.form.get('type', 'all')
    
    if not files or files[0].filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    temp_dir = create_temp_dir()
    saved_files = []
    
    for file in files:
        if file and allowed_file(file.filename, file_type):
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            saved_files.append({
                "name": filename,
                "path": file_path,
                "size": os.path.getsize(file_path)
            })
    
    if not saved_files:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify({"error": "No valid files uploaded"}), 400
    
    return jsonify({
        "message": f"Successfully uploaded {len(saved_files)} files",
        "files": saved_files,
        "temp_dir": temp_dir
    })

# 清理临时文件
@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    temp_dir = request.json.get('temp_dir')
    if temp_dir and os.path.exists(temp_dir) and temp_dir.startswith(TEMP_DIR):
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify({"message": "Temporary files cleaned up"})
    return jsonify({"error": "Invalid temporary directory"}), 400

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)