import lucene
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
import sys
import os

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

app = FastAPI()

root = './'
base_dir = os.path.abspath(root)
docs_index_directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, "DocsFilesIndex")))
source_index_directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, "SourceFilesIndex")))
docs_searcher = IndexSearcher(DirectoryReader.open(docs_index_directory))
source_searcher = IndexSearcher(DirectoryReader.open(source_index_directory))
analyzer = StandardAnalyzer()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, query: str='demo'):
    query = QueryParser("contents", analyzer).parse(query)
    docs_score_docs = docs_searcher.search(query, 50).scoreDocs
    source_score_docs = source_searcher.search(query, 50).scoreDocs
    docs_search_length = len(docs_score_docs)
    docs_search_names = []
    docs_search_paths = []
    source_search_length = len(source_score_docs)
    source_search_names = []
    source_search_paths = []
    for docs_score_doc in docs_score_docs:
        docs_doc = docs_searcher.doc(docs_score_doc.doc)
        docs_search_names.append(docs_doc.get('name'))
        docs_search_paths.append(docs_doc.get('path') + '/' + docs_doc.get('name'))
    for source_score_doc in source_score_docs:
        source_doc = source_searcher.doc(source_score_doc.doc)
        source_search_names.append(source_doc.get('name'))
        source_search_paths.append(source_doc.get('path') + '/' + source_doc.get('name'))
    return templates.TemplateResponse(
        "search_result.html",
        {
            "request": request,
            "docs_search_length": docs_search_length,
            "docs_search_names": docs_search_names,
            "docs_search_paths": docs_search_paths,
            "source_search_length": source_search_length,
            "source_search_names": source_search_names,
            "source_search_paths": source_search_paths
        }
    )

@app.get("/view_docs")
async def view_docs(path: str):
    return FileResponse(path, media_type="text/html")

@app.get("/view_source")
async def viewhtml(path: str):
    return FileResponse(path, media_type="text/x-java-source")
