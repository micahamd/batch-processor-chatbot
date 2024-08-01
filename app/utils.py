import os
import base64
from PIL import Image
from io import BytesIO
from app.read_files import read_document, read_spreadsheet, process_image

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
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()
        img_str = process_image(image_bytes)  # Use process image to standardize image types
        if img_str:
            return f"Image file: {file_path}", [img_str]
        else:
            return f"Failed to process image file: {file_path}", []
    except Exception as e:
        raise IOError(f"Error processing image file {file_path}: {str(e)}")

def read_context_files(file_paths):
    context_content = []
    for file_path in file_paths:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    image_bytes = image_file.read()
                img_str = process_image(image_bytes)
                if img_str:
                    context_content.append(f"Image file: {os.path.basename(file_path)}\nBase64: {img_str[:20]}...")
                else:
                    context_content.append(f"Failed to process image file: {os.path.basename(file_path)}")
            else:
                content, _ = read_file(file_path)
                context_content.append(f"Content of {os.path.basename(file_path)}:\n{content}\n")
        except Exception as e:
            context_content.append(f"Error reading {os.path.basename(file_path)}: {str(e)}\n")
    return "\n".join(context_content)