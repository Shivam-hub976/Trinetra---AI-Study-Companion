import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF

def extract_text_from_image(file_storage):
    try:
        image = Image.open(file_storage)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return ''

def extract_text_from_pdf_images(file_storage):
    try:
        pdf_bytes = file_storage.read()
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ''
        for page in pdf:
            pix = page.get_pixmap()
            img_bytes = pix.tobytes()
            image = Image.open(io.BytesIO(img_bytes))
            text += pytesseract.image_to_string(image) + '\n'
        return text
    except Exception as e:
        return ''