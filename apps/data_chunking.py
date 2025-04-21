import pdfplumber
import json
import re

def extract_paragraphs_with_regex(pdf_path, output_json_path, max_chars=3000):
    all_paragraphs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(layout=True)
            if not text:
                continue

            # استفاده از regex برای تشخیص پاراگراف‌ها
            paragraphs = re.findall(r'(.+?)(?:\n\s*\n|\Z)', text.strip(), re.DOTALL)

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                # اگر پاراگراف طولانی‌تر از 3000 کاراکتر بود، تکه‌تکه‌اش کن
                chunks = [para[i:i+max_chars] for i in range(0, len(para), max_chars)]
                for chunk in chunks:
                    all_paragraphs.append({
                        "page": page_number,
                        "paragraph": chunk.strip()
                    })

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_paragraphs, f, ensure_ascii=False, indent=2)

    return all_paragraphs

# استفاده:
pdf_path = r"D:\translation\input\Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf"
output_json_path = "output_paragraphs_regex.json"
results = extract_paragraphs_with_regex(pdf_path, output_json_path)
print(f"{len(results)} پاراگراف استخراج شد.")
