def read_doc_content(doc_name: str) -> str:
    try:
        with open(f"./doc/{doc_name}", "r") as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Document {doc_name} not found")
    except IOError:
        raise ValueError(f"Error reading document {doc_name}")
