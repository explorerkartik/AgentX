import os
import PyPDF2
import docx

def analyze_file(file_path: str) -> str:
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' nahi mili."

        ext = os.path.splitext(file_path)[1].lower()

        # PDF file
        if ext == ".pdf":
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                return "PDF se text extract nahi hua (scanned image ho sakta hai)."
            
            return f"PDF Content ({len(reader.pages)} pages):\n\n{text[:3000]}..."

        # Word file
        elif ext in [".docx", ".doc"]:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            
            if not text.strip():
                return "Document empty hai."
            
            return f"Document Content:\n\n{text[:3000]}..."

        # Text file
        elif ext in [".txt", ".md", ".py", ".js", ".html", ".css", ".json"]:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            return f"File Content:\n\n{text[:3000]}"

        else:
            return f"Unsupported file type: {ext}. Supported: PDF, DOCX, TXT, MD, PY, JS, HTML, CSS, JSON"

    except Exception as e:
        return f"File analyze error: {str(e)}"


# Tool spec for LLM
FILE_ANALYZER_TOOL = {
    "type": "function",
    "function": {
        "name": "analyze_file",
        "description": "Read and analyze files - PDF, Word documents, text files, code files, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Full path to the file to analyze"
                }
            },
            "required": ["file_path"]
        }
    }
}