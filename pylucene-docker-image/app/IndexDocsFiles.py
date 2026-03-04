import lucene
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

import sys
import os
import threading
import time
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory


def IndexDocsFiles():
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    store_dir = os.path.join(base_dir, "DocsFilesIndex")
    analyzer = StandardAnalyzer()

    store = NIOFSDirectory(Paths.get(store_dir))
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    root = "../lucene-9.12.0/docs/"

    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    t2 = FieldType()
    t2.setStored(False)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
            print("adding", filename)
            try:
                path = os.path.join(root, filename)
                file = open(path, encoding='iso-8859-1')
                contents = file.read()
                file.close()
                doc = Document()
                doc.add(Field("name", filename, t1))
                doc.add(Field("path", root, t1))
                if len(contents) > 0:
                    doc.add(Field("contents", contents, t2))
                else:
                    print("warning: no content in %s" % filename)
                writer.addDocument(doc)
            except Exception as e:
                print("Failed in indexDocs:", e)

    print('commit index', end=' ')
    writer.commit()
    writer.close()
    print('done')


if __name__ == '__main__':
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        IndexDocsFiles()
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
