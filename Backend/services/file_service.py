import os
from config import UPLOAD_FOLDER

def save_file(file):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return filepath