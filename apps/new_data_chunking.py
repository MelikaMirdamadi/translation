import re
import pdfplumber
import json

def extract_paragraphs_by_line_spacing(pdf_path, output_json_path, max_chars=3000):
    all_paragraphs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract the full text of the page
            full_text = page.extract_text()
            if not full_text:
                continue

            # Use regex to split the text into paragraphs
            paragraphs = re.findall(r"(.+?)(?:\n\s*\n|\Z)", full_text, re.DOTALL)

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

def extract_paragraphs_by_capital_letters(pdf_path, output_json_path):
    all_paragraphs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract the full text of the page
            full_text = page.extract_text()
            if not full_text:
                continue

            # Use regex to split paragraphs based on capital letters at the start of sentences
            # A paragraph starts with a capital letter and ends before the next capital letter
            paragraphs = re.split(r'(?<!\n)(?=\n?[A-Z])', full_text)

            current_paragraph = ""
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if paragraph:
                    # Append the paragraph to the current paragraph
                    if current_paragraph:
                        current_paragraph += " " + paragraph
                    else:
                        current_paragraph = paragraph

                    # Check if the next paragraph starts with a capital letter
                    if re.match(r'^[A-Z]', paragraph.split("\n")[-1]):
                        all_paragraphs.append({
                            "page": page_number,
                            "paragraph": current_paragraph.strip()
                        })
                        current_paragraph = ""

            # Add the last paragraph on the page
            if current_paragraph.strip():
                all_paragraphs.append({
                    "page": page_number,
                    "paragraph": current_paragraph.strip()
                })

    # Save the paragraphs to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_paragraphs, f, ensure_ascii=False, indent=2)

    return all_paragraphs

def save_pdf_text_to_file(pdf_path, output_text_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_text_path, 'w', encoding='utf-8') as f:
            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract the full text of the page
                full_text = page.extract_text()
                if full_text:
                    f.write(f"--- Page {page_number} ---\n")
                    f.write(full_text)
                    f.write("\n\n")  # Add spacing between pages

def extract_text_with_structure(pdf_path, output_text_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_text_path, 'w', encoding='utf-8') as f:
            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract text with layout information
                lines = page.extract_text().split("\n")
                for line in lines:
                    # Check for indentation or empty lines
                    if line.strip() == "":
                        f.write("\n")  # Add a blank line for paragraph separation
                    elif line.startswith(" "):  # Indented line
                        f.write(f"    {line.strip()}\n")
                    else:
                        f.write(f"{line.strip()}\n")
                f.write("\n--- End of Page ---\n\n")

# Example usage
pdf_path = r"D:\translation\input\Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf"
# output_json_path = "output_paragraphs_linegap.json"
# results = extract_paragraphs_by_line_spacing(pdf_path, output_json_path)
# print(f"{len(results)} پاراگراف استخراج شد.")

# output_text_path = r"D:\translation\output\extracted_text.txt"
# save_pdf_text_to_file(pdf_path, output_text_path)
# print("متن استخراج‌شده در فایل ذخیره شد.")

# structured_output_text_path = r"D:\translation\output\structured_text.txt"
# extract_text_with_structure(pdf_path, structured_output_text_path)
# print("متن با ساختار اولیه استخراج شد.")

output_json_path_capital_letters = r"D:\translation\output\paragraphs_by_capital_letters.json"
results_capital_letters = extract_paragraphs_by_capital_letters(pdf_path, output_json_path_capital_letters)
print(f"{len(results_capital_letters)} پاراگراف استخراج شد.")
