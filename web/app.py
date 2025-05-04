from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import sys

# Add the parent directory to the path so we can import spectomate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spectomate.core.registry import ConverterRegistry
from spectomate.schemas.pip_schema import PipSchema
from spectomate.schemas.conda_schema import CondaSchema
from spectomate.schemas.poetry_schema import PoetrySchema
import tempfile

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    source_format = data.get('source_format')
    target_format = data.get('target_format')
    source_content = data.get('source_content')
    options = data.get('options', {})
    
    if not all([source_format, target_format, source_content]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        # Create temporary files for source and target
        with tempfile.NamedTemporaryFile(delete=False, suffix=get_file_extension(source_format)) as source_file:
            source_file.write(source_content.encode('utf-8'))
            source_path = source_file.name
        
        target_path = tempfile.mktemp(suffix=get_file_extension(target_format))
        
        # Get the appropriate converter
        converter_class = ConverterRegistry.get_converter(source_format, target_format)
        if not converter_class:
            return jsonify({"error": f"No converter available for {source_format} to {target_format}"}), 400
        
        # Create converter instance
        converter = converter_class(
            source_file=source_path,
            target_file=target_path,
            options=options
        )
        
        # Execute conversion
        converter.execute()
        
        # Read the result
        with open(target_path, 'r') as f:
            target_content = f.read()
        
        # Clean up temporary files
        os.unlink(source_path)
        if os.path.exists(target_path):
            os.unlink(target_path)
        
        return jsonify({
            "target_content": target_content,
            "source_format": source_format,
            "target_format": target_format
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/formats', methods=['GET'])
def get_formats():
    # Get available formats from the registry
    formats = {
        "pip": "requirements.txt",
        "conda": "environment.yml",
        "poetry": "pyproject.toml"
    }
    
    return jsonify(formats)

def get_file_extension(format_name):
    extensions = {
        "pip": ".txt",
        "conda": ".yml",
        "poetry": ".toml"
    }
    return extensions.get(format_name, ".txt")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
