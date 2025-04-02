from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    # Read PDF
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return "Error extracting text from PDF."

def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Chunks text with overlap to maintain context.
    Returns a list of text chunks.
    """
    # Simple paragraph-based chunking
    paragraphs = text.split("\n\n")
    
    # Remove empty paragraphs and clean up
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    # Combine paragraphs into chunks with size constraints
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed chunk size, save current chunk and start a new one
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep some overlap for context
            current_chunk = current_chunk[-overlap:] if overlap > 0 else ""
        
        current_chunk += "\n" + paragraph if current_chunk else paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks