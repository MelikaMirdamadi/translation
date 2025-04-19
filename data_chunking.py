import pdfplumber
import json

def extract_paragraphs_with_pages(pdf_path):
    paragraphs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(layout=True)  # حالت layout برای تشخیص ساختار
            if not text:
                continue
            
            lines = text.split('\n')
            current_para = ""
            
            for line in lines:
                line = line.strip()
                if not line:  # خط خالی = پایان پاراگراف
                    if current_para:
                        paragraphs.append({
                            "page": page_num,
                            "text": current_para.strip()
                        })
                        current_para = ""
                else:
                    # ادغام خطوط شکسته (مثال: "جملهٔ شکسته- │ شده" → "جملهٔ شکسته شده")
                    if line.endswith('-'):
                        current_para += line[:-1]  # حذف خط تیره
                    else:
                        current_para += line + " "
            
            if current_para:  # پاراگراف آخر صفحه
                paragraphs.append({
                    "page": page_num,
                    "text": current_para.strip()
                })
    
    return paragraphs

pdf_paragraphs = extract_paragraphs_with_pages("your_file.pdf")

def smart_chunking(paragraphs, max_chars=3000, overlap_ratio=0.1):
    chunks = []
    current_chunk = ""
    current_page = 1
    
    for para in paragraphs:
        if len(current_chunk) + len(para["text"]) <= max_chars:
            current_chunk += para["text"] + "\n\n"
            current_page = para["page"]  # شماره صفحه آخرین پاراگراف
        else:
            # محاسبه Overlap (۱۰٪ از انتهای چانک قبلی)
            overlap_chars = int(len(current_chunk) * overlap_ratio)
            overlap_text = current_chunk[-overlap_chars:] if overlap_chars > 0 else ""
            
            # ذخیره چانک فعلی
            chunks.append({
                "start_page": current_page,
                "text": current_chunk.strip()
            })
            
            # شروع چانک جدید با Overlap
            current_chunk = overlap_text + "\n\n" + para["text"]
            current_page = para["page"]
    
    if current_chunk:  # چانک باقی‌مانده
        chunks.append({
            "start_page": current_page,
            "text": current_chunk.strip()
        })
    
    return chunks

chunks = smart_chunking(pdf_paragraphs, max_chars=3000, overlap_ratio=0.1)


output = {
    "metadata": {
        "source": "./input/Contact_Center_Management_on_Fast_Forward_Succeeding_in_the_New (1).pdf",
        "chunk_size": 3000,
        "overlap": "10%"
    },
    "chunks": chunks
}

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)