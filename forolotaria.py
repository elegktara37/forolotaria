# Reads the pdf file, extract the data from it
from line_utils import get_page_line_counts
import pdfplumber
import re

pdf_path = "2025-05.pdf"
lottery_numbers = []

# Define pattern: 1–3 parts; parts 2/3 must be exactly 4 digits
pattern = re.compile(r'(?<![\d.,])(?:\d{1,4} \d{4} \d{4}|\d{1,4} \d{4}(?![\d.])|\d{1,4}(?![\d.,]))(?![\d.,])')

# Get total lines on each page
line_counts = get_page_line_counts(pdf_path)

# Manually define headers if needed
STATIC_HEADERS = {
    1: range(0, 10)       # Page 1 header lines 1–10 (0-indexed 0–9)
}

# Build EXCLUSION_LINES with smart footer handling
EXCLUSION_LINES = {}
last_page = max(line_counts.keys())

for page_num, total_lines in line_counts.items():
    exclusions = {}

    # Apply header only if defined
    if page_num in STATIC_HEADERS:
        exclusions['header'] = STATIC_HEADERS[page_num]

    # Footer logic:
    if total_lines > 0:
        if page_num == last_page:
            # On last page: footer from line 11 to end (0-indexed → line 10 onward)
            exclusions['footer'] = range(10, total_lines)
        else:
            # On other pages: footer is just the last line
            exclusions['footer'] = [total_lines - 1]

    EXCLUSION_LINES[page_num] = exclusions
with pdfplumber.open(pdf_path) as pdf:
    for page_index, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        lines = text.splitlines()
        full_text = '\n'.join(lines)
        matches = list(pattern.finditer(full_text))
        used_spans = []

        exclusions = EXCLUSION_LINES.get(page_index, {})
        excluded_lines = set()

        # Combine header and footer exclusions
        if 'header' in exclusions:
            excluded_lines.update(exclusions['header'])
        if 'footer' in exclusions:
            excluded_lines.update(exclusions['footer'])

        for match in matches:
            start, end = match.span()
            line_num = full_text[:start].count('\n')

            if line_num in excluded_lines:
                continue
            
            number = match.group()

            # Reject numbers that contain anything other than digits and spaces
            if re.search(r'[^\d ]', number):
                continue
            
            if all(end <= s or start >= e for s, e in used_spans):
                lottery_numbers.append(number)
                used_spans.append((start, end))

# Remove duplicates, sort by numeric value
lottery_numbers = sorted(set(lottery_numbers), key=lambda x: int(x.replace(" ", "")))

# Output results
for number in lottery_numbers:
    print(number)

print("\nTotal numbers:", len(lottery_numbers))
if lottery_numbers:
    print("Smallest number:", lottery_numbers[0])
    print("Largest number:", lottery_numbers[-1])
else:
    print("No valid numbers found.")
