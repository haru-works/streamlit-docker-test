import fitz
import json
from typing import List, Tuple, Dict
import os
import requests
import tempfile
from urllib.parse import urlparse


class PDFPassageProcessor:
    def __init__(self, input_path: str, chars_per_passage: int = 1000):

        self.input_path = input_path
        self.chars_per_passage = chars_per_passage
        self.temp_file = None

        # If input is URL, download it first
        if self._is_url(input_path):
            self.temp_file = self._download_pdf(input_path)
            self.doc = fitz.open(self.temp_file.name)
        else:
            self.doc = fitz.open(input_path)



    def _is_url(self, path: str) -> bool:
        """Check if the input path is a URL."""
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False



    def _download_pdf(self, url: str) -> tempfile.NamedTemporaryFile:
        """Download PDF from URL to a temporary file."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # Create temporary file
        temp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp.write(chunk)
        temp.close()
        return temp
    
    

    def sort_by_bbox(self,chunks: list):
        chunks = sorted(chunks, key=lambda x: x["bbox"][0])
        chunks = sorted(chunks, key=lambda x: x["bbox"][1])
        return chunks



    def extract_text_with_positions(self) -> List[Tuple[str, int, fitz.Rect, int]]:
        """
        Extract text and position information from the PDF.

        Returns:
            List of tuples containing (text, page_number, text_rectangle, char_count)
        """
        text_positions = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            blocks = self.sort_by_bbox(page.get_text("dict")["blocks"])
            for block in blocks:
                if "lines" in block:
                    for line in self.sort_by_bbox(block["lines"]) :
                        for span in self.sort_by_bbox(line["spans"]):
                            text = span["text"]
                            if text.strip():  # Skip empty text
                                bbox = fitz.Rect(span["bbox"])
                                char_count = len(text)
                                text_positions.append((text, page_num, bbox, char_count))

        return text_positions



    def create_passages(self, text_positions: List[Tuple[str, int, fitz.Rect, int]]) -> List[Dict]:
        """
        Create passages with PDF.js compatible annotations.
        """
        passages = []
        current_passage = ""
        current_positions = []
        char_count = 0

        for text, page_num, bbox, text_char_count in text_positions:
            new_char_count = char_count + text_char_count + 1

            page = self.doc[page_num]
            page_height = page.rect.height

            if new_char_count > self.chars_per_passage and current_passage:
                passage_dict = {
                    "page_content": current_passage.strip(),
                    "metadata": {
                        "pid": str(len(passages)),
                        "source": self.input_path,
                        "bbox": json.dumps(current_positions)
                    },
                }
                passages.append(passage_dict)

                # Convert coordinates for PDF.js
                current_passage = text + " "
                current_positions = [{
                    "p": page_num,
                    "x": round(bbox.x0),
                    "y1": round(page_height - bbox.y1),  # Convert y-coordinate
                    "y2": round(bbox.y0),
                    "w": round(bbox.width),
                    "h": round(bbox.height)
                }]
                #current_positions= [page_num,round(bbox.x0),round(page_height - bbox.y1),round(bbox.width),round(bbox.height)]
                char_count = text_char_count + 1
            else:
                current_passage += text + " "
                current_positions.append({
                    "p": page_num,
                    "x": round(bbox.x0),
                    "y1": round(page_height - bbox.y1),  # Convert y-coordinate
                    "y2": round(bbox.y0),
                    "w": round(bbox.width),
                    "h": round(bbox.height)
                })
                #current_positions.append([page_num,round(bbox.x0),round(page_height - bbox.y1),round(bbox.width),round(bbox.height)])
                char_count = new_char_count

        if current_passage.strip():
            passage_dict = {
                "page_content": current_passage.strip(),
                "metadata": {
                    "pid": str(len(passages)),
                    "source": self.input_path,
                    "bbox": json.dumps(current_positions)
                },
            }
            passages.append(passage_dict)

        return passages



    def highlight_passages(self, passages: List[Dict], output_path: str):
        """
        Create a new PDF with highlighted passages.

        Args:
            passages: List of passage dictionaries
            output_path: Path where to save the output PDF
        """
        # Create a copy of the document for highlighting
        output_doc = self.doc

        # Highlight each passage
        for passage in passages:
            bboxs = json.loads(passage["metadata"]["bbox"])
            for bbox in bboxs:
                page = output_doc[bbox["p"]]
                bbox = fitz.Rect(
                     bbox["x"],
                     bbox["y2"],
                     bbox["x"] + bbox["w"],
                     bbox["y2"] + bbox["h"]
                 )
                highlight = page.add_highlight_annot(bbox)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow color
                highlight.update()

        # Save the highlighted PDF
        output_doc.save(output_path)
        output_doc.close()



    def process_pdf(self):
    #def process_pdf(self, output_pdf_path: str, output_jsonl_path: str):

        # Extract text with positions
        text_positions = self.extract_text_with_positions()

        # Create passages
        passages = self.create_passages(text_positions)

        # # Ensure the directory for output_jsonl_path exists
        # output_dir = os.path.dirname(output_jsonl_path)
        # if output_dir:
        #     os.makedirs(output_dir, exist_ok=True)

        # # Save passages to JSONL file
        # with open(output_jsonl_path, 'w', encoding='utf-8') as f:
        #     for passage in passages:
        #         f.write(json.dumps(passage, ensure_ascii=False) + '\n')

        # # Highlight passages in the PDF
        # self.highlight_passages(passages, output_pdf_path)

        return passages


    def close(self):
        if self.temp_file:
            try:
                os.unlink(self.temp_file.name)
            except:
                pass
