import pymupdf4llm
import os

def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Converts a PDF file to a Markdown string using pymupdf4llm.
    """
    if not pdf_path or not os.path.exists(pdf_path):
        return ""
    
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        return md_text
    except Exception as e:
        print(f"Error converting PDF to markdown: {e}")
        return ""
    finally:
        # Clean up the temporary PDF file
        try:
            os.remove(pdf_path)
        except:
            pass
