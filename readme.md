# 🚀 Multimodal Chatbot

A Multimodal Chatbot capable of deploying models from ChatGPT, Claude, and Gemini in a single interface. The model can process text, images (with vision-capable models), documents, and audio (with whisper-1 only), and generate text and images (using Dall-E). You can additionally batch process multiple files with a given prompt, and save the output in HTML. 

## 🌟 Features

- 🤖 Implements ChatGPT, Claude, and Gemini models (at present)
- 📄 Support for various document file types (DOCX, PDF, PPT), images, spreadsheets (XLS, CSV), audio
- 📁 Batch processing multiple files from a user-provided directory
- 💬 Chat history integration
- 💾 Save conversations as HTML

## 🛠️ Installation

1. Clone this repository:
   ```
   git clone https://github.com/micahamd/Batch-Processor-V2.git
   cd multimodal-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## 🚀 Usage

Run the application:
```
python main.py
```

## 🎯 How to Interact with the Agent

1. **Select AI Model**: 
   - Choose the developer (ChatGPT, Claude, or Gemini) from the dropdown menu. Then choose the specific model version. These can be updated directly in the 'processor.py' file.

2. **Enter Your Prompt**:
   - Type your question or instruction in the text box, as you would in a conventional chatbot UI.

3. **Include Chat History**:
   - Check the "Include Chat History?" box if you want the chatbot to consider previous interactions (involving text/images) displayed in the chatbox. Note that the latter *only* records the agent's responses, and your earlier instructions will not be taken into consideration. 

4. **Process Files**:
   - Click "Toggle Directory" to select a folder of files to process.
   - The agent has been tested on complex PDFs, Word documents, and images in the current iteration. 
   - *Caution* Be aware of token limits when processing complex PDFs with several images.

5. **Start Processing**:
   - Hit the "Process" button to send your request to the selected AI. *DO NOT* interact with the application while its processing your request as it runs on your main thread for security reasons. The speed of the response is contingent on the quality of your internet connection. 

6. **Review Output**:
   - Scroll through the chat window to see the AI's responses. Any images will be displayed inline with the text.

7. **Save Your Conversation**:
   - Click "Save Output" to store the entire chat history as an HTML file.

8. **Start Fresh**:
   - Use the "Clear Window" button to reset the chat and start a new conversation.

## 💡 Usage Tips

- For single/multiple files that you want to input, create a directory and direct the agent there.
- When processing documents, ask specific questions about the content, e.g., "Summarize the main points of this report."
- Experiment with different AI models for your workflow. As of July 7, 2024, Claude 3.5 appears useful for most use cases, GPT is good for image generation and audio transcription, and Gemini for its immense context window. 
- Use the chat history feature for more context-aware conversations.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

