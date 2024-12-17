from flask import Blueprint, request, jsonify
import speech_recognition as sr

voice_bp = Blueprint('voice', __name__)
recognizer = sr.Recognizer()

@voice_bp.route('/voice/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        
        # Convert audio to text
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
        
        return jsonify({'transcription': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
