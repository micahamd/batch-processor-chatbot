import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
from app.utils import read_file, read_context_files
import requests
from PIL import Image
from io import BytesIO
from .read_files import process_image # Pre-process all images into JPG format

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
        prompt = f"Context:{context_content}\n\nPrompt:\n{prompt}"

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
                processed_image = process_image(base64.b64decode(item_content))
                if processed_image:
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{processed_image}"}}
                        ]
                    })

    if context_files:
        context_message = "Context Files:\n"
        for context_file in context_files:
            try:
                if context_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    with open(context_file, "rb") as image_file:
                        image_bytes = image_file.read()
                    processed_image = process_image(image_bytes)
                    if processed_image and model.startswith("gpt-4"):
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Context image: {os.path.basename(context_file)}"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{processed_image}"
                                    }
                                }
                            ]
                        })
                    else:
                        context_message += f"[An image file was provided: {os.path.basename(context_file)}]\n"
                else:
                    file_content = read_file(context_file)
                    context_message += f"Content of context file {os.path.basename(context_file)}:\n{file_content}\n\n"
            except Exception as e:
                context_message += f"Error reading context file {os.path.basename(context_file)}: {str(e)}\n"
        context_message += "End of Context Files\n"
        messages.append({"role": "user", "content": context_message})

    messages.append({"role": "user", "content": f"Prompt:\n{prompt}"})
    
    if file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    image_bytes = image_file.read()
                processed_image = process_image(image_bytes)
                if processed_image and model.startswith("gpt-4"):
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{processed_image}"
                                }
                            }
                        ]
                    })
                else:
                    print(f"Failed to process image file: {file_path}")  # Added error logging
                    messages.append({"role": "user", "content": f"{prompt}\n\n[An image was shared but could not be processed or the model doesn't support image analysis.]"})
            else:
                file_content = read_file(file_path)
                messages.append({"role": "user", "content": f"{prompt}\n\nFile content: {file_content}"})
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")  # Added error logging
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
                processed_image = process_image(base64.b64decode(item_content))
                if processed_image:
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": processed_image
                        }
                    })
    
    if context_files:
        content.append({"type": "text", "text": "Context Files:"})
        for context_file in context_files:
            try:
                if context_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    with open(context_file, "rb") as image_file:
                        image_bytes = image_file.read()
                    processed_image = process_image(image_bytes)
                    if processed_image:
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": processed_image
                            }
                        })
                        content.append({"type": "text", "text": f"Context image: {os.path.basename(context_file)}"})
                    else:
                        content.append({"type": "text", "text": f"[Failed to process image file: {os.path.basename(context_file)}]"})
                else:
                    file_content = read_file(context_file)
                    content.append({"type": "text", "text": f"Content of context file {os.path.basename(context_file)}:\n\n{file_content}"})
            except Exception as e:
                content.append({"type": "text", "text": f"Error reading context file {os.path.basename(context_file)}: {str(e)}"})
        content.append({"type": "text", "text": "End of Context Files"})
    
    content.append({"type": "text", "text": f"Prompt:\n{prompt}"})

    if file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    image_bytes = image_file.read()
                processed_image = process_image(image_bytes)
                if processed_image:
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": processed_image
                        }
                    })
                    content.append({"type": "text", "text": "Please analyze this image based on the given prompt."})
                else:
                    content.append({"type": "text", "text": "[An image was shared but could not be processed.]"})
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
    
    if context_files:
        contents.append("Context Files:")
        for context_file in context_files:
            try:
                if context_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    with open(context_file, "rb") as image_file:
                        image_bytes = image_file.read()
                    processed_image = process_image(image_bytes)
                    if processed_image:
                        image = Image.open(BytesIO(base64.b64decode(processed_image)))
                        contents.extend([
                            f"Context image: {os.path.basename(context_file)}",
                            image
                        ])
                    else:
                        contents.append(f"[Failed to process image file: {os.path.basename(context_file)}]")
                else:
                    file_content = read_file(context_file)
                    contents.append(f"Content of context file {os.path.basename(context_file)}:\n\n{file_content}")
            except Exception as e:
                contents.append(f"Error reading context file {os.path.basename(context_file)}: {str(e)}")
        contents.append("End of Context Files")
    
    contents.append(f"Prompt:\n{prompt}")
    
    if file_path:
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with open(file_path, "rb") as image_file:
                    image_bytes = image_file.read()
                processed_image = process_image(image_bytes)
                if processed_image:
                    image = Image.open(BytesIO(base64.b64decode(processed_image)))
                    contents.extend([
                        "Please analyze this image based on the given prompt:",
                        image
                    ])
                else:
                    contents.append("[An image was shared but could not be processed.]")
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