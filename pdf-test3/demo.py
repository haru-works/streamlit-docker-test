import streamlit as st
import os
import json
import logging
from pdf_processor import PDFPassageProcessor
from urllib.parse import urlparse,urlencode, quote
import streamlit.components.v1 as stc

logger = logging.getLogger(__name__)


st.set_page_config(layout="wide")


def create_viewer_url_by_passage(base_url,passage):
    """Create a URL to open PDF.js viewer with annotation highlighting."""
    try:
        ann_list = json.loads(passage["metadata"].get('bbox', '[]'))
        pdf_url = passage["metadata"].get('source', None)
        if not pdf_url or not ann_list:
            return None
        viewer_annotations = []
        for ann in ann_list:
            viewer_annotations.append({
                'x': ann.get('x', 0),
                'y': ann.get('y1', 0),
                'width': ann.get('w', 0),
                'height': ann.get('h', 0),
                'page': ann.get('p', 0) 
            })

        params = {
            'file': pdf_url,
            'annotations': json.dumps(viewer_annotations),
            'pageNumber': viewer_annotations[0]['page'] + 1
        }
        return f"{base_url}?{urlencode(params, quote_via=quote)}"

    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error in create_viewer_url_by_passage: {e}")
        return None


def post_process_html(base_url: str,full_response: str, passages: list) -> str:
    """Similar to post_process but outputs HTML links that open in new tab."""
    import re

    def replace_citation(match):
        num = int(match.group(1)) - 1
        if num < len(passages):
            source = passages[num]["metadata"].get('source', '')
            # PDF以外のすべてのURLに対して新しいタブを開く
            if source.startswith(('http://', 'https://')) and not source.endswith('.pdf'):
                return f'<a href="{source}" target="_blank">[{num + 1}]</a>'
            else:
                viewer_url = create_viewer_url_by_passage(base_url,passages[num])
                if viewer_url:
                    return f'<a href="{viewer_url}" target="_blank">[{num + 1}]</a>'
                else:
                    return f'[{num + 1}]'
        return match.group(0)

    processed_text = re.sub(r'\[(\d+)\]', replace_citation, full_response)
    return processed_text


def main():

    try:

        base_url = "http://localhost:9000/viewer.html"
        #input_file = "gaiyo2023_07.pdf"
        input_file = "n4900000.pdf"
        #input_file = "outline_01.pdf"
        #output_dir = "output"
        # Ensure the output directory exists
        #os.makedirs(output_dir, exist_ok=True)
        #base_name = os.path.splitext(os.path.basename(urlparse(input_file).path))[0]
        #passage_file = os.path.join(output_dir, f"{base_name}_passages.jsonl")
        #annotated_pdf = os.path.join(output_dir, f"{base_name}_annotated.pdf")
        chunk_size = 1000
        processor = PDFPassageProcessor(input_file, chunk_size)

        passages = processor.process_pdf()
        print(f"Processed {len(passages)} passages from PDF: {input_file}")
    finally:
        processor.close()

    col1, col2 = st.columns(2)

    full_response = "別window pdfハイライト表示：[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]"
    user_msg = st.chat_input("ここにメッセージを入力")

    with col1.container(height=670):
        # viewer.htmlを別window表示
        processed_response = post_process_html(base_url,full_response, passages)
        h_no = st.selectbox('iframe pdfハイライト表示',[1,2,3,4,5,6,7,8,9,10],index=None)
        st.markdown(processed_response, unsafe_allow_html=True)

    with col2.container(height=670):
        # viewer.htmlをinframe表示
        if h_no:
             viewer_url = create_viewer_url_by_passage(base_url,passages[h_no-1])
             #print(viewer_url)
             stc.iframe(viewer_url,height=650,scrolling=True)

   
if __name__ == "__main__":
    main()
