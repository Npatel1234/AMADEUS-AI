from flask import Blueprint, jsonify
import psutil

system_bp = Blueprint('system', __name__)

@system_bp.route('/system/status', methods=['GET'])
def system_status():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return jsonify({
        'status': 'success',
        'system_info': {
            'cpu_usage': f"{cpu_percent}%",
            'cpu_cores': psutil.cpu_count(),
            'memory_used': f"{memory.percent}%",
            'memory_available': f"{memory.available / (1024 * 1024 * 1024):.2f} GB"
        }
    })
