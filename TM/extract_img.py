import pytesseract
from PIL import Image

# Load images
image_paths = [
    '2023 Integrated Report_Kor.jpg'
]

# Use pytesseract to do OCR on the images
extracted_texts = []
for path in image_paths:
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='kor')
    extracted_texts.append(text)

extracted_texts
