from modelcontextprotocol import Tool
from docling import DoclingDocument, parse_document  # adjust imports based on Docling API

class DoclingTool(Tool):
    name = "docling_fetch"
    description = "Parse a document and fetch parts based on user instructions"

    def run(self, *, document_bytes: bytes, query: str):
        """
        - document_bytes: raw file content
        - query: free-text instruction (e.g., "list all section headings")
        """
        doc = parse_document(document_bytes)
        # Simple parsing logic:
        if "headings" in query.lower():
            headings = [elem.text for elem in doc.elements if elem.type == "heading"]
            return {"headings": headings}

        if "tables" in query.lower():
            tables = [t.to_dict() for t in doc.tables]
            return {"tables": tables}

        # Fallback: return full JSON
        return doc.to_dict()