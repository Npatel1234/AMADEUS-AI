from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.chat import chat_bp
from app.routes.vision import vision_bp
from app.routes.system import system_bp
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Add rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(vision_bp, url_prefix='/api')
    app.register_blueprint(system_bp, url_prefix='/api')

    # Add specific rate limits for new endpoints
    limiter.limit("30 per minute")(chat_bp)

    @app.route('/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'device': Config.DEVICE,
            'cpu_threads': Config.CPU_THREADS
        }

    return app

if __name__ == '__main__':
    app = create_app()
    print(f"Starting server with device: {Config.DEVICE}")
    print(f"Available CPU threads: {Config.CPU_THREADS}")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
