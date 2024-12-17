from flask import Blueprint, request, jsonify
from app.models.llm import LLMService
from app.models.emotion_model import EmotionModel
from app.models.conversation_manager import ConversationManager
from datetime import datetime
import base64

chat_bp = Blueprint('chat', __name__)
llm_service = LLMService()
emotion_model = EmotionModel()
conversation_manager = ConversationManager()

# Load saved conversations on startup
conversation_manager.load_conversations()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message')
        conversation_id = data.get('conversation_id', 'default')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        max_attempts = 3
        for attempt in range(max_attempts):
            # Generate contextual prompt
            contextual_prompt = conversation_manager.generate_contextual_prompt(
                conversation_id, 
                user_input
            )
            
            # Get response from LLM
            response = llm_service.generate_response(contextual_prompt)
            
            if response:
                # Try to add the exchange
                if conversation_manager.add_exchange(conversation_id, user_input, response):
                    # Analyze emotion
                    emotion = emotion_model.analyze(response)
                    
                    return jsonify({
                        'response': response,
                        'emotion': emotion,
                        'conversation_id': conversation_id,
                        'status': 'success'
                    })
                # If exchange wasn't added (due to repetition), try again
                continue
            
        # If we get here, we failed all attempts
        return jsonify({
            'error': 'Failed to generate unique response',
            'status': 'error'
        }), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/chat/history', methods=['GET'])
def get_history():
    conversation_id = request.args.get('conversation_id', 'default')
    history = conversation_manager.get_conversation_history(conversation_id)
    return jsonify({
        'history': history,
        'status': 'success'
    })

@chat_bp.route('/chat/clear', methods=['POST'])
def clear_history():
    conversation_id = request.json.get('conversation_id', 'default')
    conversation_manager.clear_conversation(conversation_id)
    return jsonify({
        'message': 'Conversation history cleared',
        'status': 'success'
    })

@chat_bp.route('/code', methods=['POST'])
def code_assistance():
    try:
        data = request.json
        code_question = data.get('code')
        conversation_id = data.get('conversation_id', 'default')
        
        if not code_question:
            return jsonify({'error': 'No code or question provided'}), 400

        contextual_prompt = conversation_manager.generate_contextual_prompt(
            conversation_id, 
            code_question,
            prompt_type='code'
        )
        
        response = llm_service.generate_response(contextual_prompt)
        
        if response:
            conversation_manager.add_exchange(conversation_id, code_question, response)
            return jsonify({
                'response': response,
                'conversation_id': conversation_id,
                'status': 'success'
            })
            
        return jsonify({
            'error': 'Failed to generate response',
            'status': 'error'
        }), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        text = data.get('text')
        file_content = data.get('file_content')  # Base64 encoded file content
        conversation_id = data.get('conversation_id', 'default')
        
        if file_content:
            # Decode base64 file content
            text = base64.b64decode(file_content).decode('utf-8')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        contextual_prompt = conversation_manager.generate_contextual_prompt(
            conversation_id,
            f"Please summarize the following text:\n\n{text}",
            prompt_type='summary'
        )
        
        response = llm_service.generate_response(contextual_prompt)
        
        if response:
            conversation_manager.add_exchange(
                conversation_id, 
                "Summarize text: " + text[:100] + "...", 
                response
            )
            return jsonify({
                'summary': response,
                'conversation_id': conversation_id,
                'status': 'success'
            })
            
        return jsonify({
            'error': 'Failed to generate summary',
            'status': 'error'
        }), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
