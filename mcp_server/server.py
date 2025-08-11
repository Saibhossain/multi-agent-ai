from flask import Flask,request,jsonify
import pandas as pd
import pdfplumber

app = Flask(__name__)

@app.route("/parse_pdf", methods=["POST"])
def parse_pdf():
    file_path = request.json.get("file_path")
    data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            data.append(text)
    return jsonify({"content": "\n".join(data)})

@app.route("/parse_csv", methods=["POST"])
def parse_csv():
    file_path = request.json.get("file_path")
    df = pd.read_csv(file_path)
    return jsonify({"content": df.to_dict()})

if __name__ == "__main__":
    app.run(port=5001)