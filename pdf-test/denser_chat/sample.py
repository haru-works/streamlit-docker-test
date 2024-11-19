from pdf_processor import PDFPassageProcessor
import os
from urllib.parse import urlparse
import json
import logging
import argparse
from urllib.parse import urlencode, quote

input_file = "gaiyo2023_07.pdf"
output_dir = "out"
# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

base_name = os.path.splitext(os.path.basename(urlparse(input_file).path))[0]

print(base_name)
passage_file = os.path.join(output_dir, f"{base_name}_passages.jsonl")
print(passage_file)
# Process PDF file
annotated_pdf = os.path.join(output_dir, f"{base_name}_annotated.pdf")
print(annotated_pdf)

processor = PDFPassageProcessor(input_file, 1000)

# Convert each annotation to include page information
viewer_annotations = []
viewer_annotations.append({
    'x': 100,
    'y': 100,
    'width': 100,
    'height': 100,
    'page': 1  # Include the page number for each annotation
})

print( json.dumps(viewer_annotations))

try:
    passages = processor.process_pdf(annotated_pdf, passage_file)
    print(f"Processed {len(passages)} passages from PDF: {input_file}")
finally:
    processor.close()