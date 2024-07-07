import os
import base64
from io import BytesIO
from docx import Document
from pptx import Presentation
import fitz  # PyMuPDF
import csv
import openpyxl
from bs4 import BeautifulSoup
import markdown2
from PIL import Image

def read_document(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext in ['.docx', '.doc']:
            return read_word_document(file_path)
        elif ext == '.pdf':
            return read_pdf_document(file_path)
        elif ext in ['.pptx', '.ppt']:
            return read_powerpoint_document(file_path)
        elif ext == '.rtf':
            return read_rtf_document(file_path)
        elif ext == '.odt':
            return read_odt_document(file_path)
        elif ext in ['.txt', '.md', '.html', '.htm']:
            return read_text_document(file_path)
        else:
            raise ValueError(f"Unsupported document format: {ext}")
    except Exception as e:
        raise IOError(f"Error reading document {file_path}: {str(e)}")

def read_word_document(file_path):
    doc = Document(file_path)
    content = []
    images = []

    for para in doc.paragraphs:
        content.append(para.text)

    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            image = Image.open(BytesIO(image_data))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            images.append(img_str)

    return "\n".join(content), images

def read_pdf_document(file_path):
    doc = fitz.open(file_path)
    content = []
    images = []

    for page in doc:
        content.append(page.get_text())
        for img in page.get_images():
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            images.append(img_str)

    return "\n".join(content), images

def read_powerpoint_document(file_path):
    prs = Presentation(file_path)
    content = []
    images = []

    for slide in prs.slides:
        slide_content = []
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                slide_content.append(shape.text)
            if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                image = shape.image
                image_bytes = image.blob
                image = Image.open(BytesIO(image_bytes))
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                images.append(img_str)
        content.append("\n".join(slide_content))

    return "\n".join(content), images

def read_rtf_document(file_path):
    # RTF reading is complex and requires a dedicated library
    # For now, we'll just read it as plain text
    with open(file_path, 'r', errors='ignore') as file:
        content = file.read()
    return content, []

def read_odt_document(file_path):
    # ODT reading requires a dedicated library like odfpy
    # For now, we'll return an error message
    return "ODT file format is not supported yet.", []

def read_text_document(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if ext == '.md':
        content = markdown2.markdown(content)
    elif ext in ['.html', '.htm']:
        soup = BeautifulSoup(content, 'html.parser')
        content = soup.get_text()

    return content, []

def read_spreadsheet(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext == '.csv':
            with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                content = '\n'.join([', '.join(row) for row in reader])
        elif ext in ['.xlsx', '.xls']:
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            sheets_data = []
            for sheet in wb.worksheets:
                sheet_data = f"Sheet: {sheet.title}\n"
                sheet_data += '\n'.join([', '.join(str(cell.value) if cell.value is not None else '' for cell in row) for row in sheet.iter_rows()])
                sheets_data.append(sheet_data)
            content = '\n\n'.join(sheets_data)
        else:
            raise ValueError(f"Unsupported spreadsheet format: {ext}")

        return content, []
    except Exception as e:
        raise IOError(f"Error reading spreadsheet {file_path}: {str(e)}")