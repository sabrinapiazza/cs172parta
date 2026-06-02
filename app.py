from flask import Flask, render_template, request
from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.scoring import BM25F

app = Flask(__name__)

INDEX_DIR = "index_dir"

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query_text = ""

    if request.method == "POST":
        query_text = request.form.get("query", "")

        if query_text.strip():
            ix = index.open_dir(INDEX_DIR)

            # Field weighting: title matters more than body
            parser = MultifieldParser(
                ["title", "body"],
                schema=ix.schema,
                fieldboosts={
                    "title": 3.0,
                    "body": 1.0
                }
            )

            query = parser.parse(query_text)

            with ix.searcher(weighting=BM25F()) as searcher:
                hits = searcher.search(query, limit=10)

                for hit in hits:
                    results.append({
                        "title": hit.get("title", "Untitled"),
                        "url": hit.get("url", ""),
                        "body": hit.get("body", "")[:300],
                        "score": round(hit.score, 3),
                        "filename": hit.get("filename", "")
                    })

    return render_template("index.html", results=results, query=query_text)

if __name__ == "__main__":
    app.run(debug=True)