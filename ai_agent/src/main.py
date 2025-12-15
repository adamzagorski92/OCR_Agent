"""OCR AI Agent with Google Gemini - Cloud Run version"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.models.vertex_ai import VertexAI
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
GEMINI_KEY = os.getenv("GOOGLE_GENERATIVEAI_API_KEY")

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Google ADK
try:
    vertex_model = VertexAI(
        project_id=PROJECT_ID,
        location="europe-west1",
        model_name="gemini-1.5-flash"
    )
    agent = Agent(
        name="ocr_agent",
        model=vertex_model,
        description="OCR Agent with Google ADK"
    )
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="ocr_app",
        session_service=session_service
    )
except Exception as e:
    print(f"Warning: ADK init failed: {e}")
    runner = None


@app.route('/', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ocr-ai-agent",
        "project": PROJECT_ID
    }), 200


@app.route('/api/process-text', methods=['POST'])
def process_text():
    """Process text with Gemini"""
    from flask import request
    
    try:
        data = request.get_json()
        text = data.get("text", "")
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        response = gemini_model.generate_content(text)
        
        return jsonify({
            "status": "success",
            "result": response.text,
            "model": "gemini-1.5-flash"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def detailed_health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "service": "ocr-ai-agent",
        "project_id": PROJECT_ID,
        "model": "gemini-1.5-flash",
        "has_adk": runner is not None
    }), 200


if __name__ == '__main__':
    # Cloud Run sends requests to the port defined by PORT env var
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
