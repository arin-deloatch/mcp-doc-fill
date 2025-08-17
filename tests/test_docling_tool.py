import pytest
from tools.docling_tool import DoclingTool

class FakeDoc:
    def __init__(self):
        self.elements = [
            type("Heading", (), {"type": "heading", "text": "Introduction"}),
            type("Paragraph", (), {"type": "paragraph", "text": "Some text"}),
        ]
        self.tables = [
            type("Table", (), {"to_dict": lambda self: {"rows": [[1, 2], [3, 4]]}})()
        ]

    def to_dict(self):
        return {"elements": [e.text for e in self.elements]}

@pytest.fixture
def tool():
    return DoclingTool()

@pytest.fixture
def fake_doc(monkeypatch):
    # Mock parse_document to return our fake object
    from tools import docling_tool
    monkeypatch.setattr(docling_tool, "parse_document", lambda _: FakeDoc())

def test_fetch_headings(tool, fake_doc):
    result = tool.run(document_bytes=b"", query="list all headings")
    assert "headings" in result
    assert result["headings"] == ["Introduction"]

def test_fetch_tables(tool, fake_doc):
    result = tool.run(document_bytes=b"", query="extract tables")
    assert "tables" in result
    assert result["tables"][0]["rows"] == [[1, 2], [3, 4]]

def test_fallback(tool, fake_doc):
    result = tool.run(document_bytes=b"", query="something else")
    assert "elements" in result