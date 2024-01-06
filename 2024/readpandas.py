import os
from bs4 import BeautifulSoup
import lxml
from dataclasses import dataclass
from typing import Iterable

PERMALINK_PREFIX = "https://pandas.pydata.org/pandas-docs/version/1.4/user_guide/"

@dataclass(frozen=True)
class Block:
    before_text: str
    permalink: str
    text: str
    after_text: str
    before_h2_text: str
    before_h3_text: str

@dataclass
class DocumentElements:
    blocks: Iterable[Block]
    title: str

out_dir = "/tmp/outd"

user_guide_files = ['merging.html', 'cookbook.html', 'text.html', 'window.html', 'categorical.html', 'index.html', '10min.html', 'reshaping.html', 'sparse.html', 'io.html', 'basics.html', 'duplicates.html', 'computation.html', 'missing_data.html',
                    'timedeltas.html', 'style.html', 'indexing.html', 'advanced.html', 'gotchas.html', 'integer_na.html', 'visualization.html', 'dsintro.html', 'timeseries.html', 'options.html', 'boolean.html', 'groupby.html', 'scale.html', 'enhancingperf.html']

def get_block(code_div) -> Block:
    permalinks = code_div.find_all_previous('a', href=lambda h: h and ("#" in h) and (not h.startswith("..")))
    permalink = permalinks[0].get("href", "") if permalinks else ""
    before_h3 = code_div.find_previous("h3")
    before_h3_text = before_h3.text if before_h3 else ""
    before_h2 = code_div.find_previous("h2")
    before_h2_text = before_h2.text if before_h2 else ""
    before_block = code_div.find_previous("p")
    before_text = before_block.text if before_block else ""
    after_block = code_div.find_next("p")
    after_text = after_block.text if after_block else ""
    return Block(before_text=before_text,
                 permalink=permalink, 
                 text=code_div.text,
                 after_text=after_text, 
                 before_h2_text=before_h2_text,
                 before_h3_text=before_h3_text)

def get_document_elements(html: str) -> DocumentElements:
    soup = BeautifulSoup(html, "lxml")
    code_divs = soup.find_all("div", class_="highlight")
    title = soup.find("title")
    return DocumentElements(blocks=[get_block(div) for div in code_divs], 
                            title=title.text if title else "")

def create_file(file_name: str):
    f = open(os.path.join(out_dir, file_name), "w")
    f.close()

def write_text(file_name: str, text: str):
    f = open(os.path.join(out_dir, file_name), "w")
    f.write(text)
    f.close()

def make_dir(path):
    os.makedirs(os.path.join(out_dir, path))

def main():
    import sys
    global out_dir
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    print("Extracting and writing metadata information ...")    
    for user_guide_file in user_guide_files:
        html_file = open(os.path.join("pandas/user_guide", user_guide_file))
        html = html_file.read()
        html_file.close()
        make_dir(user_guide_file)
        elements = get_document_elements(html)
        write_text(os.path.join(user_guide_file, "title.txt"), elements.title)
        n = 0
        for block in elements.blocks:
            make_dir(os.path.join(user_guide_file, str(n)))
            write_text(os.path.join(user_guide_file, str(n), "block.txt"), block.text)
            write_text(os.path.join(user_guide_file, str(n), "before.txt"), block.before_text)
            write_text(os.path.join(user_guide_file, str(n), "permalink.txt"), f"{PERMALINK_PREFIX}{user_guide_file}{block.permalink}")
            write_text(os.path.join(user_guide_file, str(n), "after.txt"), block.after_text)
            write_text(os.path.join(user_guide_file, str(n), "h2.txt"), block.before_h2_text)
            write_text(os.path.join(user_guide_file, str(n), "h3.txt"), block.before_h3_text)
            n += 1

if __name__ == '__main__':
    main()