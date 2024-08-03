from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QComboBox, QTextEdit, QFileDialog, 
                             QLabel, QScrollArea, QMessageBox,QProgressBar)
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QByteArray, QBuffer
from io import BytesIO
from html import escape
import base64
from PIL import Image
from app.processor import process_request
import os 

class ChatbotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multimodal Chatbot")
        self.setGeometry(100, 100, 600, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.chat_history = []

        layout = QVBoxLayout()

        # For output styling 
        self.processing_multiple_files = False

        # Aesthetics
        stylesheet_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
        with open(stylesheet_path, 'r') as f:
            self.setStyleSheet(f.read())


        # Developer and Model selection
        dev_model_layout = QHBoxLayout()
        self.developer_combo = QComboBox()
        self.developer_combo.addItems(["ChatGPT", "Claude", "Gemini", "Mistral"])
        self.developer_combo.currentIndexChanged.connect(self.update_model_options)
        dev_model_layout.addWidget(self.developer_combo)
        self.model_combo = QComboBox()
        self.update_model_options()
        dev_model_layout.addWidget(self.model_combo)
        layout.addLayout(dev_model_layout)

        # Prompt input
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.prompt_input.setObjectName("prompt_input") 
        layout.addWidget(self.prompt_input)

        # Include chat history
        self.include_history_checkbox = QCheckBox("Include Chat History?")
        layout.addWidget(self.include_history_checkbox)

        # Add context directory
        context_layout = QHBoxLayout()
        self.add_context_checkbox = QCheckBox("Add Context")
        self.add_context_checkbox.stateChanged.connect(self.toggle_context_button)
        context_layout.addWidget(self.add_context_checkbox)
        
        self.context_button = QPushButton("Context Directory")
        self.context_button.clicked.connect(self.select_context_directory)
        self.context_button.setVisible(False)
        context_layout.addWidget(self.context_button)
        layout.addLayout(context_layout)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_button = QPushButton("Batch Processing Directory")
        self.dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.dir_button)
        self.dir_label = QLabel("No Directory Selected")
        dir_layout.addWidget(self.dir_label)
        layout.addLayout(dir_layout)

        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_request)
        layout.addWidget(self.process_button)

        # Processing label
        self.processing_label = QLabel("Processing...")
        self.processing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processing_label.setStyleSheet("font-weight: bold; color: #4CAF50; min-height: 30px;")
        self.processing_label.setMinimumHeight(30)  # Set a minimum height for the label
        self.processing_label.hide()
        layout.addWidget(self.processing_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Output display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("output_area") 
        self.output_widget = QWidget()
        self.output_layout = QVBoxLayout()
        self.output_widget.setLayout(self.output_layout)
        self.scroll_area.setWidget(self.output_widget)
        layout.addWidget(self.scroll_area)

        # Save button
        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)
        layout.addWidget(self.save_button)

        # Clear window button
        self.clear_button = QPushButton("Clear Window")
        self.clear_button.clicked.connect(self.clear_output)
        layout.addWidget(self.clear_button)

        central_widget.setLayout(layout)

        self.selected_directory = None
        self.directory_files = []
        self.current_file_index = 0
        self.context_files = []
        self.context_directory = None

    def toggle_context_button(self, state):
        self.context_button.setVisible(state == Qt.CheckState.Checked.value)

    def update_model_options(self):
        self.model_combo.clear()
        developer = self.developer_combo.currentText()
        if developer == "ChatGPT":
            self.model_combo.addItems(["gpt-4o-mini","gpt-4o", "dall-e-3", "dall-e-2", "whisper-1"])
        elif developer == "Claude":
            self.model_combo.addItems(["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"])
        elif developer == "Gemini":
            self.model_combo.addItems(["gemini-1.5-flash-001", "gemini-1.5-pro-001", "gemini-1.0-pro-vision-001"])
        elif developer == "Mistral":
            self.model_combo.addItems(["open-mistral-nemo", "mistral-large-latest","codestral-2405","mistral-embed"])    

    def get_filtered_files(self, directory):
        # Takes a directory path as input and returns a list of files in that directory that are not temporary files (do not start with '~$') and have specific extensions.
        filtered_files =  [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.startswith('~$') and f.lower().endswith(('.txt', '.pdf', '.html', '.doc', '.docx','.ppt','.pptx', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp3', '.wav', '.ogg', '.m4a'))]
        print(f"Filtered files: {filtered_files}")  # Debug statement
        return filtered_files

    def select_directory(self):
        # Opens a dialog for the user to select a directory. If a directory is selected, it filters the files using 'get_filtered_files' and updates the 'directory_files'
        # and 'current_file_index' attributes. It also updates the 'dir_label' to show the number of files selected. To unselect a directory, open the dialog option again and
        # press 'Cancel'
        self.selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.selected_directory:
            self.directory_files = self.get_filtered_files(self.selected_directory)
            self.current_file_index = 0
            self.dir_label.setText(f"Directory Selected: {len(self.directory_files)} files")
        else:
            self.directory_files = []
            self.current_file_index = 0
            self.dir_label.setText("No Directory Selected")

    def select_context_directory(self):
        # Similar to 'select_directory', this also opens a dialog for the user to select a context directory. If a directory is selected, files are filtered using 'get_filtered_files'.
        # The 'context_files' and 'context_directory' attributes are updated. Unlike the 'select_directory' method, all files in the context directory are processed simultaneously.
        self.context_directory = QFileDialog.getExistingDirectory(self, "Select Context Directory")
        if self.context_directory:
            self.context_files = self.get_filtered_files(self.context_directory)
            print("Context Files:", self.context_files)  # List context files in terminal
            self.context_button.setText(f"Context Directory: {len(self.context_files)} files")
        else:
            self.context_files = []
            self.context_directory = None
            self.context_button.setText("Select Context Directory")

    def process_request(self):
        # Takes a request object, processes it, and sends the request to the API.
        self.processing_multiple_files = bool(self.selected_directory and self.directory_files) # Flag html output generator

        developer = self.developer_combo.currentText()
        model = self.model_combo.currentText()
        prompt = self.prompt_input.toPlainText()
    
        if not prompt:
            self.append_to_output("Please provide a prompt")
            return
    
        self.processing_label.show() # Show the label
        chat_history = self.chat_history if self.include_history_checkbox.isChecked() else None
        
        context_files = None
        if self.add_context_checkbox.isChecked() and self.context_directory and self.context_files:
            context_files = [os.path.join(self.context_directory, f) for f in self.context_files]      
 
        if self.selected_directory and self.directory_files:
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(self.directory_files))
            
            while self.current_file_index < len(self.directory_files):
                current_file = os.path.join(self.selected_directory, self.directory_files[self.current_file_index])
                self.progress_bar.setValue(self.current_file_index + 1)
                
                result = process_request(developer, model, prompt, current_file, chat_history, context_files)
                self.handle_result(result)
                
                self.append_to_output(f"Processed file {self.current_file_index + 1} of {len(self.directory_files)}: {self.directory_files[self.current_file_index]}")
                self.current_file_index += 1
                
            self.append_to_output("All files in the directory have been processed.")
            self.progress_bar.setVisible(False)
            self.current_file_index = 0  # Reset for next use
        else:
            result = process_request(developer, model, prompt, None, chat_history, context_files)
            self.handle_result(result)
    
        self.processing_label.hide() # Hide the label
        self.progress_bar.setVisible(False)

    def handle_result(self, result):
        if isinstance(result, tuple):
            text, image = result
            if text:
                self.append_to_output(text)
            if isinstance(image, Image.Image):
                self.append_image_to_output(image)
        elif isinstance(result, Image.Image):
            self.append_image_to_output(result)
        elif isinstance(result, str):
            self.append_to_output(result)
        else:
            self.append_to_output(f"Unsupported output format: {type(result)}")

    def get_history_prompt(self):
        history_parts = []
        for item_type, content, _ in self.chat_history:
            if item_type == "text":
                history_parts.append(content)
            elif item_type == "image":
                history_parts.append(f"[An image was shared in the conversation. Base64: {content[:20]}...]")
        return "\n".join(history_parts)

    def append_to_output(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.output_layout.addWidget(label)
        self.output_layout.addWidget(QLabel("---"))
        
        # Store the text content with formatting information
        formatted_text = text.replace('\n', '<br>')  # Preserve line breaks
        self.chat_history.append(("text", formatted_text))

    def append_image_to_output(self, image):
        q_image = self.pil_to_qimage(image)
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        label = QLabel()
        label.setPixmap(scaled_pixmap)
        self.output_layout.addWidget(label)
        self.output_layout.addWidget(QLabel("---"))
        
        # Store the image as base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        self.chat_history.append(("image", img_str))

    def pil_to_qimage(self, pil_image):
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        q_image = QImage()
        q_image.loadFromData(buffer.getvalue())
        return q_image

    def update_output_display(self):
        output = ""
        for item_type, item_content in self.chat_history:
            if item_type == "text":
                output += f"{item_content}\n\n---\n\n"
            elif item_type == "image":
                # Convert PIL Image to QPixmap
                buffer = BytesIO()
                item_content.save(buffer, format="PNG")
                q_image = QImage()
                q_image.loadFromData(buffer.getvalue())
                pixmap = QPixmap.fromImage(q_image)
                
                # Scale the image
                scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                
                # Save the scaled image and add it to the output
                buffer = QBuffer()
                buffer.open(QBuffer.OpenModeFlag.ReadWrite)
                scaled_pixmap.save(buffer, "PNG")
                image_data = buffer.data().toBase64()
                output += f'<img src="data:image/png;base64,{image_data.data().decode()}" />\n\n---\n\n'

    def save_output(self):
        if self.output_layout.count() == 0:
            QMessageBox.warning(self, "No Content", "There's no content to save.")
            return
    
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Output", "", 
                                                   "HTML Files (*.html);;All Files (*)")
        if not file_path:
            return  # User cancelled the save dialog
        
        html_content = self.get_html_output()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            QMessageBox.information(self, "Save Successful", f"Output saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", f"Failed to save output: {str(e)}")

    def get_html_output(self):
        css = """
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f0f0f0;
            }
            .chat-item {
                margin-bottom: 20px;
                padding: 10px;
                border-radius: 5px;
                background-color: #fff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            }
            .chat-item img {
                max-width: 100%;
                height: auto;
                margin-top: 10px;
            }
            .separator {
                border: none;
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }
        </style>
        """
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '<title>Conversation History</title>',
            css,
            '</head>',
            '<body>',
            '<h1>Conversation History</h1>'
        ]
        
        for item_type, content in self.chat_history:
            html_parts.append('<div class="chat-item">')
            if item_type == "text":
                # Use the stored formatted text directly
                html_parts.append(f'<p>{content}</p>')
            elif item_type == "image":
                html_parts.append(f'<img src="data:image/png;base64,{content}" alt="Conversation Image">')
            html_parts.append('</div>')
        
        html_parts.append('</body></html>')
        return '\n'.join(html_parts)

    def format_file_content(self, file_header, content):
        html = [f'<div class="file-section"><h2>{escape(file_header)}</h2>']
        for item_type, item_content in content:
            html.append('<div class="conversation-item">')
            if item_type == "text":
                html.append(f'<p>{escape(item_content)}</p>')
            elif item_type == "image":
                if isinstance(item_content, str):
                    img_base64 = item_content
                else:
                    buffer = BytesIO()
                    item_content.save(buffer, format="PNG")
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                html.append(f'<img src="data:image/png;base64,{img_base64}" alt="Conversation Image">')
            html.append('</div>')
        html.append('</div><hr class="separator">')
        return '\n'.join(html)
   
    def clear_output(self):
            for i in reversed(range(self.output_layout.count())): 
                self.output_layout.itemAt(i).widget().setParent(None)
            self.chat_history.clear()  # Clear the chat history when clearing the output