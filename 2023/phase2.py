# index: (title.txt, [document])
# document: (block.txt, before.txt, after.txt, h2.txt, h3.txt)

from pathlib import Path
from elasticsearch import Elasticsearch
import os, re
ELASTIC_INDEX_PREFIX = "pandas_user_guide-"
ELASTIC_INDEX_NOTES_PREFIX = "notes-"

inp_dir = "outd"
elastic_client = Elasticsearch("http://localhost:9200")

def get_function_terms(func_names):
    result = set()
    for func_name in func_names:
        result.add(func_name)
        if '_' in func_name:
            result.add(func_name.replace('_',' ').strip())
    return list(result)

def get_function_names(block:str):
    return get_function_terms(re.findall(r"([_a-zA-Z][_a-zA-Z0-9]*)\(", block, re.MULTILINE))

def fix_htext(text: str):
    if text and text.endswith('¶'):
        return text[:-1]
    return text

def make_document(node_path):
    block = Path(os.path.join(node_path, "block.txt")).read_text()
    before = Path(os.path.join(node_path, "before.txt")).read_text()
    after = Path(os.path.join(node_path, "after.txt")).read_text()
    h2 = Path(os.path.join(node_path, "h2.txt")).read_text()
    h3 = Path(os.path.join(node_path, "h3.txt")).read_text()
    return {"block": block, "before": before, "after": after, "functions":get_function_names(block), "h2": fix_htext(h2), "h3": fix_htext(h3)}

def process_index(index_name):
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

print("Writing to ElasticSearch - Pandas user guide ...")
index_names = [x for x in os.listdir(inp_dir) if os.path.isdir(os.path.join(inp_dir, x))]
for index_name in index_names:
    process_index(index_name) 


