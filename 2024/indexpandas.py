# index: (title.txt, [document])
# document: (block.txt, before.txt, after.txt, h2.txt, h3.txt, functions)

from pathlib import Path
from elasticsearch import Elasticsearch
import os, re
from typing import List, Optional
from sentence_transformers import SentenceTransformer

ELASTIC_INDEX_PREFIX = "pandas_user_guide-"
ELASTIC_INDEX_NOTES_PREFIX = "notes-"

inp_dir = "/tmp/outd"
elastic_client = Elasticsearch("http://localhost:9200")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_function_terms(func_names) -> List[str]:
    result = set()
    for func_name in func_names:
        result.add(func_name)
        if '_' in func_name:
            result.add(func_name.replace('_',' ').strip())
    return list(result)

def get_function_names(block:str) -> List[str]:
    return get_function_terms(re.findall(r"([_a-zA-Z][_a-zA-Z0-9]*)\(", block, re.MULTILINE))

def fix_htext(text: str) -> Optional[str]:
    if text and text.endswith('¶'):
        return text[:-1]
    return text

def make_document(node_path) -> dict:
    block = Path(os.path.join(node_path, "block.txt")).read_text()
    before = Path(os.path.join(node_path, "before.txt")).read_text()
    after = Path(os.path.join(node_path, "after.txt")).read_text()
    h2 = Path(os.path.join(node_path, "h2.txt")).read_text()
    h3 = Path(os.path.join(node_path, "h3.txt")).read_text()
    permalink = Path(os.path.join(node_path, "permalink.txt")).read_text()

    embed_vector = embed_model.encode(f"{h2} {h3}: {before} {block} {after}")
    return {"block": block, "embed_vector": embed_vector, "permalink":permalink, "before": before, "after": after, "functions":get_function_names(block), "h2": fix_htext(h2), "h3": fix_htext(h3)}

def process_index(index_name: str):
    title = Path(os.path.join(inp_dir, index_name, "title.txt")).read_text()
    print(f"Indexing {title} ...")
    node_names = [x for x in os.listdir(os.path.join(inp_dir, index_name)) if os.path.isdir(os.path.join(inp_dir, index_name, x))]
    prev_after = ""
    for node_name in node_names:
        document = make_document(os.path.join(inp_dir, index_name, node_name))
        document["chapter"] = title
        document["prev_after"] = prev_after
        prev_after = document["after"]
        elastic_client.index(index=f"{ELASTIC_INDEX_PREFIX}{index_name}", id=node_name, document=document)


def main():
    global inp_dir
    import sys
    if len(sys.argv) > 1:
        inp_dir = sys.argv[1]
    print("Writing to ElasticSearch - Pandas user guide ...")
    index_names = [x for x in os.listdir(inp_dir) if os.path.isdir(os.path.join(inp_dir, x))]
    for index_name in index_names:
        process_index(index_name) 

if __name__=='__main__':
    main()

