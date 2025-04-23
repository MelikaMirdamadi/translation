import re
import pdfplumber
import json

def extract_paragraphs(pdf_path, output_json_path):
    all_paragraphs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract the full text of the page
            full_text = page.extract_text()
            if not full_text:
                continue

            # Split text into paragraphs based on capital letters at the start of sentences
            paragraphs = re.split(r'(?<=\n)(?=[A-Z])', full_text)

            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if paragraph:
                    all_paragraphs.append({
                        "page": page_number,
                        "paragraph": paragraph
                    })

    # Save the paragraphs to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_paragraphs, f, ensure_ascii=False, indent=2)

    return all_paragraphs

# Example usage
pdf_path = r"D:\translation\input\Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf"
output_json_path = r"D:\translation\output\paragraphs_output.json"
results = extract_paragraphs(pdf_path, output_json_path)
print(f"{len(results)} پاراگراف استخراج شد و در فایل JSON ذخیره شد.")