from fastapi import FastAPI, HTTPException
from lxml import etree
from typing import List

app = FastAPI()

# Load the XML file
XML_FILE = "library.xml"

def load_xml(file_path: str):
    try:
        with open(file_path, "rb") as f:
            return etree.parse(f)
    except Exception as e:
        raise RuntimeError(f"Error loading XML file: {e}")

# Parse the XML file
try:
    xml_tree = load_xml(XML_FILE)
except RuntimeError as e:
    raise RuntimeError(f"Failed to initialize application: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to XPath Express API"}

@app.get("/books")
def get_all_books():
    """
    Fetch all books from the XML file.
    """
    try:
        books = xml_tree.xpath("//book")
        result = []
        for book in books:
            result.append({
                "id": book.get("id"),
                "title": book.findtext("title"),
                "author": book.findtext("author"),
                "year": book.findtext("year"),
                "genre": book.findtext("genre"),
            })
        return {"books": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching books: {e}")

@app.post("/query")
def query_xpath(xpath: str):
    """
    Query the XML file using an XPath expression.
    """
    try:
        # Execute the XPath query
        results = xml_tree.xpath(xpath)
        if not results:
            return {"message": "No results found for the given XPath query."}

        # Convert results to a readable format
        output = []
        for result in results:
            if isinstance(result, etree._Element):
                output.append(etree.tostring(result, pretty_print=True).decode("utf-8"))
            else:
                output.append(str(result))
        return {"results": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid XPath query: {e}")