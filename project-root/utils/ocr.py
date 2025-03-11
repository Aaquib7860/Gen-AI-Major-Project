import os
import pytesseract
from PIL import Image
import cv2
import numpy as np
import PyPDF2
from pdf2image import convert_from_path
import subprocess

class OCRProcessor:
    def __init__(self, tesseract_path="C:/Program Files/Tesseract-OCR/tesseract.exe", poppler_path="C:/poppler-24.08.0/Library/bin"):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.poppler_path = poppler_path
        self.check_dependencies()

    def check_dependencies(self):
        """Check Tesseract and Poppler availability"""
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            print("Error: Tesseract is not installed or not in your PATH.")
            print("- Windows: Install from https://github.com/tesseract-ocr/tesseract")
            print("- Linux: sudo apt-get install tesseract-ocr")
            print("- Mac: brew install tesseract")
            raise SystemExit("Tesseract is required.")
        try:
            if self.poppler_path:
                subprocess.run([os.path.join(self.poppler_path, 'pdftoppm'), '-v'],
                              capture_output=True, text=True)
            else:
                subprocess.run(['pdftoppm', '-v'], capture_output=True, text=True)
        except Exception:
            print("Error: Poppler is not installed or not in your PATH.")
            print("- Windows: https://github.com/oschwartz10612/poppler-windows/releases")
            print("- Linux: sudo apt-get install poppler-utils")
            print("- Mac: brew install poppler")
            raise SystemExit("Poppler is required for PDF image extraction.")

    def preprocess_image(self, image_path, upscale_factor=2.0):
        """Preprocess image for accurate OCR"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None, "Invalid image file!"
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            new_width = int(width * upscale_factor)
            new_height = int(height * upscale_factor)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            gray = cv2.fastNlMeansDenoising(gray, h=30)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            gray = cv2.filter2D(gray, -1, kernel)
            gray = cv2.equalizeHist(gray)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            temp_path = "preprocessed.png"
            cv2.imwrite(temp_path, thresh)
            return temp_path, None
        except Exception as e:
            return None, f"Preprocessing failed: {str(e)}"

    def image_to_text(self, image_path, psm=6, oem=3):
        """Convert image text to plain text"""
        try:
            if not os.path.exists(image_path):
                return "Image file not found!"
            preprocessed_path, error = self.preprocess_image(image_path)
            if error:
                return error
            custom_config = f'--oem {oem} --psm {psm}'
            text = pytesseract.image_to_string(Image.open(preprocessed_path), config=custom_config)
            os.remove(preprocessed_path)
            return text.strip() if text.strip() else ""
        except Exception as e:
            return f"Error converting image to text: {str(e)}"

    def extract_pdf_text(self, pdf_path):
        """Extract embedded text from PDF"""
        try:
            if not os.path.exists(pdf_path):
                return "PDF file not found!"
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text.append(text.strip())
                return '\n'.join(full_text) if full_text else ""
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    def extract_pdf_images_text(self, pdf_path, psm=6, oem=3):
        """Extract text from images within PDF"""
        try:
            if not os.path.exists(pdf_path):
                return "PDF file not found!"
            images = convert_from_path(pdf_path, poppler_path=self.poppler_path, dpi=300)
            full_text = []
            for i, img in enumerate(images):
                temp_path = f"temp_page_{i}.png"
                img.save(temp_path, 'PNG')
                text = self.image_to_text(temp_path, psm=psm, oem=oem)
                if text and "Error" not in text:
                    full_text.append(text)
                os.remove(temp_path)
            return '\n'.join(full_text) if full_text else ""
        except Exception as e:
            return f"Error processing PDF images: {str(e)}"

    def process_pdf(self, pdf_path):
        """Combine embedded text and image text from PDF"""
        try:
            # Extract embedded text
            embedded_text = self.extract_pdf_text(pdf_path)
            if "Error" in embedded_text:
                return embedded_text

            # Extract text from images
            image_text = self.extract_pdf_images_text(pdf_path)
            if "Error" in image_text:
                return image_text

            # Combine results
            combined_text = []
            if embedded_text:
                combined_text.append("Embedded Text:\n" + embedded_text)
            if image_text:
                combined_text.append("Image Text:\n" + image_text)
            return '\n\n'.join(combined_text) if combined_text else "No text detected in PDF"
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

def main():
    # Initialize processor
    processor = OCRProcessor(tesseract_path="C:/Program Files/Tesseract-OCR/tesseract.exe",poppler_path="C:/poppler-24.08.0/Library/bin")
    # Test with an image
    image_path = "sample_img.png"
    print(f"\nConverting {image_path} to text:")
    result = processor.image_to_text(image_path)
    print(result)

    # Test with a PDF
    pdf_path = "Machine learning algorithms are largely driven by mathematics.pdf"  # Replace with your PDF file
    print(f"\nConverting {pdf_path} to text (embedded + images):")
    result = processor.process_pdf(pdf_path)
    print(result)

if __name__ == "__main__":
    main()