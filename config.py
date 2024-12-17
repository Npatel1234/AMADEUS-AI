import os
from dotenv import load_dotenv
import multiprocessing

load_dotenv()

class Config:
    # Server Settings
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True

    # LM Studio Settings
    LM_STUDIO_HOST = "http://localhost:1234"
    LM_STUDIO_ENDPOINT = f"{LM_STUDIO_HOST}/v1/completions"
    
    # CPU Settings
    DEVICE = "cpu"
    CPU_THREADS = multiprocessing.cpu_count()
    
    # Model Parameters
    MAX_TOKENS = 2048
    TEMPERATURE = 0.7
    TOP_P = 0.9
    PRESENCE_PENALTY = 0.0
    FREQUENCY_PENALTY = 0.0
    
    # Batch size for efficient CPU processing
    BATCH_SIZE = 1
