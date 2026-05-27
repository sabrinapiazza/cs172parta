import os
import argparse
from datetime import datetime
from bs4 import BeautifulSoup

from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED, DATETIME
from whoosh.analysis import StemmingAnalyzer

#building the schema to collect the information from html pages
schema = Schema(
    #store the url as is, it will act as a unique ID
    url = ID(stored=True, unique=True),
    #StemmingAnalyzer will preprocess the text
    title = TEXT(stored=True, analyzer=StemmingAnalyzer()),
    body = TEXT(stored=True, analyzer=StemmingAnalyzer()),
    #STORED will save the value & not index it (can be displayed)
    date = STORED(),
    filename = STORED(),
)

#function to parse the html files
def parse_html(filepath):
    #open the filepath & store what it has
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    #use beautiful soup to grab the text from the html file
    soup = BeautifulSoup(html, "html.parser")

    #grab the title using beautiful soup
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    
    #grab the body by removing the tags in the body
    for html_tag in soup(["script", "style"]):
        #decompose removes the script and style tags
        html_tag.decompose()
    body = soup.get_text(separator=" ", strip=True)

    #return the title and the body
    return title, body

#building the index
def build_index(input_dir, index_dir):
    #makes the index folder
    os.makedirs(index_dir, exist_ok=True)

    #checker to see if index exists already or not
    if index.exists_in(index_dir):
        curr_index = index.open_dir(index_dir)
    else:
        curr_index = index.create_in(index_dir, schema)

    #opens a writer object
    index_writer = curr_index.writer()

    #grab all the html files in our directory
    files = [f for f in os.listdir(input_dir) if f.endswith(".html")]

    for i, filename in enumerate(files):
        #grabs the full filepath for each file
        filepath = os.path.join(input_dir, filename)
        
        #grabs the title and body we got from the parser
        title, body = parse_html(filepath)
        
        #grabs the url
        url = filename.replace(".html", "").replace("_", "/")

        #grabs the time
        mtime    = os.path.getmtime(filepath)

        #grabs the date
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

        #uses the index writer object to add a document & fit the schema 
        index_writer.add_document(
            url      = url,
            title    = title or "untitled",
            body     = body  or "",
            date     = date_str,
            filename = filename,
        )

        #prints how many files were indexed
        if (i + 1) % 100 == 0:
            print(f"  Indexed {i+1}/{len(files)}")

    #commiting the objects from writer 
    index_writer.commit()
    print(f"Done. Index saved to '{index_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder of crawled HTML files")
    parser.add_argument("--index", required=True, help="Where to save the index")
    args = parser.parse_args()

    build_index(args.input, args.index)
