# 🚀 Multimodal Chatbot integrating OpenAI, Anthropic and Google models

A Multimodal Chatbot capable of deploying models from ChatGPT, Claude, and Gemini in a single interface. The model can process text, images (with vision-capable models), documents, and audio (with whisper-1 only). The model generates text and images (using Dall-E) in a chat window display that can be saved as an HTML file. Features include multi-file batch processing, selective inclusion of the prior chat history in the prompt, and the optional inclusion of a context directory.   

## 🌟 Features 

- 🤖 Implements ChatGPT, Claude, and Gemini models (at present). Additional developers/models can be included in the processor.py file. 
- 📄 Support for various document file types (DOCX, PDF, PPT, HTML), images, spreadsheets (XLS, CSV), audio.
- 📁 Batch process multiple files from a user-provided directory.
- 💬 Optional chat history integration into context window
- 💾 Save conversations as HTML
- 🧠 Include context files from a different user-provided directory.

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
   PYTHONPATH=${PYTHONPATH}:${PWD}  # References the current value of the PYTHONPATH environment variable if it isn't already set
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## 🚀 Usage

Run the application from the terminal:
```
python main.py
```

## 🎯 Interacting with the Agent

1. **Switch between AI Models in the same session**: 
   - Choose the developer (ChatGPT, Claude, or Gemini) from the dropdown menu. Then choose a model specific to the developer. These can be updated in the 'ui.py' file (see 'update_model_options' metho).

2. **Prompt Entry**:
   - Type your question or instruction in the text box, as you would in a conventional chatbot UI.

3. **Include Chat History**:
   - Check the "Include Chat History?" box if you want the chatbot to consider previous interactions (involving text/images) displayed in the chatbox. Note that the latter *only* records the agent's responses, in conjunction with the instructions in the prompt window. 
   - Scroll through the chat window to see the AI's responses. Any images will be displayed inline with the text.

4. **Add Context**:
   - Check the "Add Context" box to reveal a button for selecting a context directory.
   - Clicking in this will allow the user to choose a folder containing context files. *All* files in the the context folder will be processed simultaneously. You can unselect the "Add Context" box to remove the context from the interaction.
  
5. **Batch Process**:
   - Click "Toggle Directory" to select a folder containing files that you want to batch process. All files in the batch process folder will be iteratively processed in conjunction with the provided prompt and, when available, the chat history and context files.
   - The agent has been tested on complex PDFs, Word documents, and images.  
   - *Caution* Be aware of token limits when processing complex PDFs with several images. For large files, Gemini Flash is the most capable.

6. **Start Processing**:
   - Hit the "Process" button to send your request to the selected AI. *DO NOT* interact with the application while it's processing your request as it runs on your main thread for security reasons. The speed of the response is contingent on the quality of your internet connection. To terminate the process, hit Ctrl+C on your terminal window. 

7. **Save Your Conversation**:
   - Click "Save Output" to store the entire chat history as an HTML file.

8. **Start Fresh**:
   - Use the "Clear Window" button to reset the chat and start a new conversation.

## 💡 Useage Tips

- For single/multiple files that you want to input, create a directory and direct the agent there. 
- I recommend having two folders called 'context_files' and 'batch_files'. Populate these in accordance with your needs.
- Experiment with different AI models in the same session to leverage each one's strengths. 
- (Optional) Select the chat history feature to incorporate earlier responses from the chat session into the prompt.
- (Optional) Select the "Add Context" feature, then a directory for including additional files into your prompt (tested with documents and images only). This can direct to the 'context_files' folder. Note that *all* files in the context directory will be processed simultaneously.
- (Optional) Use the "Select Directory" button to identify the directory for batch processing. The prompt (incl. chat history + context if you choose) will be applied to each file incrementally in the 'batch_files' directory that you would have created.

## ⚠️ Important Notes

- **Token Limits**: The application currently does not have built-in token limiters. Be cautious about the amount of data you process, especially with large files or extensive chat histories. You can set token limits in the 'processor.py' file for each AI service.
- **Performance**: The application processes requests on the main thread. For large files or batch processing, expect the UI to be unresponsive until processing is complete. This can be manually terminated from the terminal by hitting 'Ctrl+C'.
- **File Compatibility**: The file types the chatbot currently supports is always expanding. Text and image processing has been successfully tested.
- **API Usage**: Be mindful of your API usage, as processing multiple files or using the chat history feature can quickly consume your token quota. 

## 🛠️ Future Enhancements

- Integrate with Ollama to run locally installed models offline.
- Add multi-threading for improved UI responsiveness during processing.
- Keep expanding file input/output options.
- Implement error handling for API failures and network issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.