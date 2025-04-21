import pdfplumber
import json

def extract_paragraphs_by_line_spacing(pdf_path, output_json_path, max_chars=3000, line_gap_threshold=5):
    all_paragraphs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            lines = page.extract_text(layout=True).split('\n')
            if not lines:
                continue

            current_paragraph = ""
            previous_bottom = None  # موقعیت پایین خط قبلی

            # برای تشخیص دقیق‌تر، با layout line‌ها رو بگیریم
            line_objs = page.lines
            line_texts = lines

            # استفاده از extract_words برای گرفتن مختصات y هر کلمه
            words = page.extract_words(use_text_flow=True, keep_blank_chars=True)
            lines_with_y = {}
            for word in words:
                top = round(word['top'])
                text = word['text']
                if top in lines_with_y:
                    lines_with_y[top] += ' ' + text
                else:
                    lines_with_y[top] = text

            sorted_lines = sorted(lines_with_y.items(), key=lambda x: x[0])  # مرتب‌سازی بر اساس y (بالا به پایین)

            previous_y = None
            for y, line_text in sorted_lines:
                if previous_y is not None and abs(y - previous_y) > line_gap_threshold:
                    # پایان یک پاراگراف
                    if current_paragraph.strip():
                        chunks = [current_paragraph[i:i+max_chars] for i in range(0, len(current_paragraph), max_chars)]
                        for chunk in chunks:
                            all_paragraphs.append({
                                "page": page_number,
                                "paragraph": chunk.strip()
                            })
                    current_paragraph = line_text
                else:
                    current_paragraph += " " + line_text

                previous_y = y

            # پاراگراف آخر صفحه
            if current_paragraph.strip():
                chunks = [current_paragraph[i:i+max_chars] for i in range(0, len(current_paragraph), max_chars)]
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
output_json_path = "output_paragraphs_linegap.json"
results = extract_paragraphs_by_line_spacing(pdf_path, output_json_path)
print(f"{len(results)} پاراگراف استخراج شد.")
