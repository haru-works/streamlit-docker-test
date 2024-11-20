from pdf_processor import PDFPassageProcessor
import os
from urllib.parse import urlparse

input_file = "n4900000.pdf"
output_dir = "output"
# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

base_name = os.path.splitext(os.path.basename(urlparse(input_file).path))[0]
passage_file = os.path.join(output_dir, f"{base_name}_passages.jsonl")
annotated_pdf = os.path.join(output_dir, f"{base_name}_annotated.pdf")
processor = PDFPassageProcessor(input_file, 1000)

try:
    passages = processor.process_pdf(annotated_pdf, passage_file)
    print(f"Processed {len(passages)} passages from PDF: {input_file}")
finally:
    processor.close()