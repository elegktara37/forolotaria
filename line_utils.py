# Function which gives me back the amount of lines on each page
import pdfplumber

def get_page_line_counts(pdf_path):
    line_counts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                lines = text.splitlines()
                line_counts[i] = len(lines)
            else:
                line_counts[i] = 0
    return line_counts
