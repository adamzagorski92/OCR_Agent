"""OCR AI Agent - Pure Google ADK"""

import os
from flask import Flask, jsonify, request

try:
    from google.adk.agents import Agent
    from google.adk.models.vertex_ai import VertexAI
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy", 
        "adk_available": ADK_AVAILABLE,
        "project": os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    }), 200

@app.route('/api/ocr', methods=['POST'])
def ocr():
    if not ADK_AVAILABLE:
        return jsonify({"error": "ADK not available"}), 500
    
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text"}), 400
    
    # Tutaj będzie ADK agent
    return jsonify({
        "status": "ADK OCR processing",
        "input_length": len(text)
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
