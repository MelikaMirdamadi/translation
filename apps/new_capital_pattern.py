import re
import pdfplumber
import json

def extract_paragraphs_with_improved_chunking(pdf_path, output_json_path, max_chars=3000):
    all_text = ""
    page_texts = []
    
    # استخراج متن هر صفحه به صورت جداگانه
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                page_texts.append((page_number, page_text))
    
    # پیش‌پردازش متن برای اتصال خطوط با خط تیره
    processed_text = ""
    for page_num, text in page_texts:
        lines = text.split('\n')
        processed_lines = []
        i = 0
        while i < len(lines):
            current_line = lines[i].strip()
            
            # بررسی خط تیره در انتهای خط
            if current_line.endswith('-') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # حذف خط تیره و اتصال خط بعدی
                current_line = current_line[:-1] + next_line
                i += 1  # خط بعدی را نادیده می‌گیریم چون به خط فعلی متصل شد
            
            processed_lines.append(current_line)
            i += 1
        
        page_processed_text = '\n'.join(processed_lines)
        processed_text += page_processed_text + "\n\n"  # اضافه کردن دو خط جدید بین صفحات
    
    # تقسیم متن به پاراگراف‌ها
    paragraphs = []
    current_paragraph = ""
    for line in processed_text.split('\n'):
        line = line.strip()
        if not line:
            if current_paragraph:
                paragraphs.append(current_paragraph)
                current_paragraph = ""
            continue
        
        # بررسی شروع پاراگراف جدید
        if re.match(r'^[A-Z]', line) and current_paragraph:
            paragraphs.append(current_paragraph)
            current_paragraph = line
        else:
            if current_paragraph:
                current_paragraph += ' ' + line
            else:
                current_paragraph = line
    
    # اضافه کردن آخرین پاراگراف
    if current_paragraph:
        paragraphs.append(current_paragraph)
    
    # تقسیم پاراگراف‌های بزرگ به چانک‌های کوچکتر
    chunks = []
    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            chunks.append(paragraph)
        else:
            # تقسیم پاراگراف‌های بزرگ
            words = paragraph.split()
            current_chunk = words[0]
            for word in words[1:]:
                if len(current_chunk) + len(word) + 1 <= max_chars:
                    current_chunk += ' ' + word
                else:
                    chunks.append(current_chunk)
                    current_chunk = word
            if current_chunk:
                chunks.append(current_chunk)
    
    # تعیین شماره صفحه برای هر چانک
    result = []
    for chunk in chunks:
        page_num = 1
        for pnum, text in page_texts:
            if chunk in text:
                page_num = pnum
                break
        result.append({
            "page": page_num,
            "paragraph": chunk,
            "char_count": len(chunk)
        })
    
    # ذخیره نتایج در فایل JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

# مثال استفاده
pdf_path = r"D:\translation\input\Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf"
output_json_path = r"D:\translation\output\paragraphs_improved.json"
results = extract_paragraphs_with_improved_chunking(pdf_path, output_json_path, max_chars=3000)
print(f"{len(results)} چانک استخراج شد با حداکثر 3000 کاراکتر و در فایل JSON ذخیره شد.")