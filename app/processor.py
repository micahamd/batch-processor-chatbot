import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
from app.utils import read_file, encode_image, read_context_files
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

def process_request(developer, model, prompt, file_path, chat_history=None, context_files=None):
    if chat_history:
        history_prompt = "\n".join([
            item_content if item_type == "text" else f"[Image: Base64 encoded, starts with {item_content[:20]}...]"
            for item_type, item_content in chat_history
        ])
        prompt = f"{history_prompt}\n\nNew prompt: {prompt}"

    if context_files:
        context_content = read_context_files(context_files)
        prompt = f"{context_content}\n\nContext:\n{prompt}"

    if developer == "ChatGPT":
        return process_chatgpt(model, prompt, file_path, chat_history, context_files)
    elif developer == "Claude":
        return process_claude(model, prompt, file_path, chat_history, context_files)
    elif developer == "Gemini":
        return process_gemini(model, prompt, file_path, chat_history, context_files)
    else:
        return "Invalid developer selected"

def process_chatgpt(model, prompt, file_path, chat_history=None, context_files=None):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    messages = []
    if chat_history:
        for item_type, item_content in chat_history:
            if item_type == "text":
                messages.append({"role": "user", "content": item_content})
            elif item_type == "image":
                if model.startswith("gpt-4"):  # For GPT-4 models with vision capabilities
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{item_content}"
                                }
                            }
                        ]
                    })
                else:
                    messages.append({"role": "user", "content": "[An image was here. It's not directly viewable in this context.]"})
    
    if model.startswith("gpt-4") and file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        })
    elif file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                messages.append({"role": "user", "content": f"{prompt}\n\n[An image was shared. It's not directly viewable in this context.]"})
            else:
                file_content = read_file(file_path)
                messages.append({"role": "user", "content": f"{prompt}\n\nFile content: {file_content}"})
        except Exception as e:
            return f"Error processing file {file_path}: {str(e)}"
    else:
        messages.append({"role": "user", "content": prompt})

    if model in ["dall-e-3", "dall-e-2"]:
        try:
            response = client.images.generate(
                model=model,
                prompt=messages[-1]["content"],
                size = "512x512" if model == "dall-e-2" else "1024x1024",  # Default for DALL-E 3
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            return image
        except Exception as e:
            error_message = f"Error generating image: {str(e)}"
            return error_message
    
    elif model == "whisper-1":
        try:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model=model,
                    file=audio_file
                )
            return f"Transcription of {os.path.basename(file_path)}:\n\n{transcription.text}"
        except Exception as e:
            return f"Error transcribing audio file: {str(e)}"
    else:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=12000
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error processing request: {str(e)}"
        
def process_claude(model, prompt, file_path, chat_history=None, context_files=None):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    content = []
    if chat_history:
        for item_type, item_content in chat_history:
            if item_type == "text":
                content.append({"type": "text", "text": item_content})
            elif item_type == "image":
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": item_content
                    }
                })
    
    content.append({"type": "text", "text": prompt})

    if file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image
                    }
                })
                content.append({"type": "text", "text": "Please analyze this image based on the given prompt."})
            else:
                file_content = read_file(file_path)
                content.append({"type": "text", "text": f"Here's the content of the file {os.path.basename(file_path)}:\n\n{file_content}\n\nPlease analyze this content based on the given prompt."})
        except Exception as e:
            return f"Error processing file {file_path}: {str(e)}"

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response.content[0].text
    
    except Exception as e:
        return f"Error processing request: {str(e)}"

def process_gemini(model, prompt, file_path, chat_history=None, context_files=None):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name=model)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8000
    }
    
    contents = []
    if chat_history:
        for item_type, item_content in chat_history:
            if item_type == "text":
                contents.append(item_content)
            elif item_type == "image":
                image = Image.open(BytesIO(base64.b64decode(item_content)))
                contents.append(image)
    
    contents.append(prompt)
    
    if file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image = Image.open(file_path)
                contents.extend([
                    "Please analyze this image based on the given prompt:",
                    image
                ])
            else:
                file_content = read_file(file_path)
                contents.append(f"Here's the content of the file {os.path.basename(file_path)}:\n\n{file_content}\n\nPlease analyze this content based on the given prompt.")
        except Exception as e:
            return f"Error processing file {file_path}: {str(e)}"

    try:
        response = model.generate_content(
            contents,
            generation_config=generation_config
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No text response generated."
    
    except Exception as e:
        return f"Error processing request: {str(e)}"    