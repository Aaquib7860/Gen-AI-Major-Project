import os
import docx
from pptx import Presentation
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

class FileHandler:
    
    def __init__(self):
      pass

    def extract_from_txt(self, file_path):
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading TXT file: {str(e)}"

    def extract_from_docx(self, file_path):
        """Extract text from DOCX files"""
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text)
        except Exception as e:
            return f"Error reading DOCX file: {str(e)}"

    def extract_from_pdf(self, file_path):
        """Extract text from text-based PDFs, redirect to OCR if needed"""
        try:
            reader = PyPDF2.PdfReader(file_path)
            full_text = [page.extract_text() for page in reader.pages]
            extracted_text = '\n'.join(full_text)

            return extracted_text
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

    def extract_from_ppt(self, file_path):
        """Extract text from PPT/PPTX files"""
        try:
            prs = Presentation(file_path)
            full_text = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        full_text.append(shape.text)
            return '\n'.join(full_text)
        except Exception as e:
            return f"Error reading PPT file: {str(e)}"

    def process_file(self, file_path):
        """Process any supported file type"""
        if not os.path.exists(file_path):
            return "File not found!"
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            return self.extract_from_txt(file_path)
        elif file_extension == '.docx':
            return self.extract_from_docx(file_path)
        elif file_extension == '.pdf':
            return self.extract_from_pdf(file_path)
        elif file_extension in ['.ppt', '.pptx']:
            return self.extract_from_ppt(file_path)
        else:
            return "Unsupported file format!"

def main():
    handler = FileHandler() 
    
    
    # you need to append uploaded file here
    test_files = [ 
      "ML UNIT-1 NOTES.pdf",
      "Introduction-to-Probability.pptx"
    ]
    
    for file_path in test_files:
        print(f"\nExtracting text from {file_path}:")
        result = handler.process_file(file_path)
        print(result)

if __name__ == "__main__":
    main()