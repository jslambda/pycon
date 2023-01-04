import os
from bs4 import BeautifulSoup
import lxml

out_dir = "outd"

user_guide_files = ['merging.html', 'cookbook.html', 'text.html', 'window.html', 'categorical.html', 'index.html', '10min.html', 'reshaping.html', 'sparse.html', 'io.html', 'basics.html', 'duplicates.html', 'computation.html', 'missing_data.html', 'timedeltas.html', 'style.html', 'indexing.html', 'advanced.html', 'gotchas.html', 'integer_na.html', 'visualization.html', 'dsintro.html', 'timeseries.html', 'options.html', 'boolean.html', 'groupby.html', 'scale.html', 'enhancingperf.html']
def get_tuple(code_div):
    before_h3 = code_div.find_previous("h3")
    before_h3_text = before_h3.text if before_h3 else ""
    before_h2 = code_div.find_previous("h2")
    before_h2_text = before_h2.text if before_h2 else ""
    before_block = code_div.find_previous("p")
    before_text = before_block.text if before_block else ""
    after_block = code_div.find_next("p")
    after_text = after_block.text if after_block else ""
    return (before_text, code_div.text, after_text, before_h2_text, before_h3_text)

def get_elements(html):
    soup = BeautifulSoup(html, "lxml")
    code_divs = soup.find_all("div", class_="highlight")
    title = soup.find("title")
    return {'blocks':[get_tuple(div) for div in code_divs], 
            'title': title.text if title else ""}

def create_file(file_name):
    f = open(os.path.join(out_dir, file_name), "w")
    f.close()

def write_text(file_name, text):
    f = open(os.path.join(out_dir, file_name), "w")
    f.write(text)
    f.close()

def make_dir(path):
    os.makedirs(os.path.join(out_dir, path))

print("Extracting and writing metadata information ...")
for user_guide_file in user_guide_files:
    html_file = open(os.path.join("pandas/user_guide", user_guide_file))
    html = html_file.read()
    html_file.close()
    make_dir(user_guide_file)
    elements = get_elements(html)
    write_text(os.path.join(user_guide_file, "title.txt"), elements["title"])
    n = 0
    for triple in elements["blocks"]:
        make_dir(os.path.join(user_guide_file, str(n)))
        write_text(os.path.join(user_guide_file, str(n), "block.txt"), triple[1])
        write_text(os.path.join(user_guide_file, str(n), "before.txt"), triple[0])
        write_text(os.path.join(user_guide_file, str(n), "after.txt"), triple[2])
        write_text(os.path.join(user_guide_file, str(n), "h2.txt"), triple[3])
        write_text(os.path.join(user_guide_file, str(n), "h3.txt"), triple[4])
        n += 1
