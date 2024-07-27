import os
import base64
from PIL import Image
from io import BytesIO
from app.read_files import read_document, read_spreadsheet

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB limit, can be adjusted

def read_file(file_path, max_file_size=MAX_FILE_SIZE):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Check file size
    if os.path.getsize(file_path) > max_file_size:
        raise ValueError(f"File size exceeds the maximum allowed size of {max_file_size / (1024 * 1024)} MB")

    try:
        if ext in ['.docx', '.doc', '.pdf', '.pptx', '.ppt', '.rtf', '.odt', '.txt', '.md', '.html', '.htm']:
            return read_document(file_path)
        elif ext in ['.xlsx', '.xls', '.csv']:
            return read_spreadsheet(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return read_image_file(file_path)
        elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
            return f"Audio file: {file_path}", []  # Whisper model will handle transcription
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

def read_image_file(file_path):
    try:
        img = Image.open(file_path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"Image file: {file_path}\nFormat: {img.format}, Size: {img.size}, Mode: {img.mode}", [img_str]
    except Exception as e:
        raise IOError(f"Error processing image file {file_path}: {str(e)}")

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        raise IOError(f"Error encoding image {image_path}: {str(e)}")

def read_context_files(file_paths):
    context_content = []
    for file_path in file_paths:
        try:
            content, _ = read_file(file_path)
            context_content.append(f"Content of {os.path.basename(file_path)}:\n{content}\n")
        except Exception as e:
            context_content.append(f"Error reading {os.path.basename(file_path)}: {str(e)}\n")
    return "\n".join(context_content)