from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QComboBox, QTextEdit, QFileDialog, 
                             QLabel, QScrollArea, QMessageBox,QProgressBar)
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QByteArray, QBuffer
from io import BytesIO
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

        # Aesthetics
        self.setStyleSheet("""
            QMainWindow {background-color: #f0f0f0;} /* Lighter background for the main window */
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E0E0E0, stop:1 #FFFFFF);
                color: #333;
                border: 1px solid #aaa;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #E0E0E0);
                border-color: #ccc;
            }
            QComboBox {
                background-color: #fff;
                color: #333;
                border: 1px solid #aaa;
                border-radius: 3px;
                padding: 5px;
                min-width: 6em;
            }
            QTextEdit, QScrollArea {
                background-color: #fff;
                color: #333;
                border: 1px solid #aaa;
                border-radius: 3px;
                padding: 2px;
            }
        """)


        # Developer and Model selection
        dev_model_layout = QHBoxLayout()
        self.developer_combo = QComboBox()
        self.developer_combo.addItems(["ChatGPT", "Claude", "Gemini"])
        self.developer_combo.currentIndexChanged.connect(self.update_model_options)
        dev_model_layout.addWidget(self.developer_combo)
        self.model_combo = QComboBox()
        self.update_model_options()
        dev_model_layout.addWidget(self.model_combo)
        layout.addLayout(dev_model_layout)

        # Prompt input
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        layout.addWidget(self.prompt_input)

        # Include chat history
        self.include_history_checkbox = QCheckBox("Include Chat History?")
        layout.addWidget(self.include_history_checkbox)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_button = QPushButton("Toggle Directory?")
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

    def update_model_options(self):
        self.model_combo.clear()
        developer = self.developer_combo.currentText()
        if developer == "ChatGPT":
            self.model_combo.addItems(["gpt-3.5-turbo-16k", "gpt-4o", "dall-e-3", "dall-e-2", "whisper-1"])
        elif developer == "Claude":
            self.model_combo.addItems(["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"])
        elif developer == "Gemini":
            self.model_combo.addItems(["gemini-1.5-pro-001", "gemini-1.5-flash-001", "gemini-1.0-pro-vision-001"])

    def select_directory(self):
        self.selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.selected_directory:
            self.directory_files = [f for f in os.listdir(self.selected_directory) if os.path.isfile(os.path.join(self.selected_directory, f)) and f.lower().endswith(('.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp3', '.wav', '.ogg', '.m4a'))]
            self.current_file_index = 0
            self.dir_label.setText(f"Directory Selected: {len(self.directory_files)} files")
        else:
            self.directory_files = []
            self.current_file_index = 0
            self.dir_label.setText("No Directory Selected")

    def process_request(self):
        developer = self.developer_combo.currentText()
        model = self.model_combo.currentText()
        prompt = self.prompt_input.toPlainText()
    
        if not prompt:
            self.append_to_output("Please provide a prompt")
            return
    
        self.processing_label.show() # Show the label

        chat_history = self.chat_history if self.include_history_checkbox.isChecked() else None
    
        if self.selected_directory and self.directory_files:
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(self.directory_files))
            
            while self.current_file_index < len(self.directory_files):
                current_file = os.path.join(self.selected_directory, self.directory_files[self.current_file_index])
                self.progress_bar.setValue(self.current_file_index + 1)
                
                result = process_request(developer, model, prompt, current_file, chat_history)
                self.handle_result(result)
                
                self.append_to_output(f"Processed file {self.current_file_index + 1} of {len(self.directory_files)}: {self.directory_files[self.current_file_index]}")
                self.current_file_index += 1
                
            self.append_to_output("All files in the directory have been processed.")
            self.progress_bar.setVisible(False)
            self.current_file_index = 0  # Reset for next use
        else:
            result = process_request(developer, model, prompt, None, chat_history)
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
        for item_type, item_content in self.chat_history:
            if item_type == "text":
                history_parts.append(item_content)
            elif item_type == "image":
                history_parts.append(f"[An image was shared in the conversation. Base64: {item_content[:20]}...]")
        return "\n".join(history_parts)

    def append_to_output(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.output_layout.addWidget(label)
        self.output_layout.addWidget(QLabel("---"))
        
        # Store the text content
        self.chat_history.append(("text", text))

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
        html_parts = ['<html><body>']
        for item_type, item_content in self.chat_history:
            if item_type == "text":
                html_parts.append(f'<p>{item_content}</p>')
            elif item_type == "image":
                buffer = BytesIO()
                item_content.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                html_parts.append(f'<img src="data:image/png;base64,{img_base64}" />')
            html_parts.append('<hr>')
        html_parts.append('</body></html>')
        return '\n'.join(html_parts)

    def clear_output(self):
        for i in reversed(range(self.output_layout.count())): 
            self.output_layout.itemAt(i).widget().setParent(None)