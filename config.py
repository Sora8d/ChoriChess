from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path('./config.env'))

class Config():
    TOKEN= os.getenv('TOKEN')
    STOCKFISH= os.getenv('STOCKFPATH')