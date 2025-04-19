import pdfplumber
import json
import re

def pdf_to_json_by_structural_paragraphs(pdf_path, output_json_path):
    paragraphs_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(layout=True)
            if not text:
                continue
            
            # تقسیم متن بر اساس خطوط جدید و تشخیص پاراگراف‌ها
            lines = text.split('\n')
            current_paragraph = ""
            
            for line in lines:
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                
                # اگر خط با عنوان Bold/Italic یا نقل‌قول شروع شود، پاراگراف جدید است
                if re.match(r'^(##|_|“)', stripped_line):
                    if current_paragraph:  # پاراگراف قبلی را ذخیره کن
                        paragraphs_data.append({
                            "page": page_num,
                            "paragraph": current_paragraph.strip()
                        })
                    current_paragraph = stripped_line
                else:
                    # ادامه پاراگراف فعلی
                    current_paragraph += " " + stripped_line
            
            # آخرین پاراگراف صفحه را اضافه کن
            if current_paragraph:
                paragraphs_data.append({
                    "page": page_num,
                    "paragraph": current_paragraph.strip()
                })
    
    # ذخیره به صورت JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(paragraphs_data, f, ensure_ascii=False, indent=4)
    
    return paragraphs_data

# مثال استفاده:
pdf_path = "./input/Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf"
output_json_path = "output_paragraphs.json"
result = pdf_to_json_by_structural_paragraphs(pdf_path, output_json_path)
print(f"تعداد پاراگراف‌های استخراج شده: {len(result)}")