from flask import Flask, render_template, request
import pickle
import re
import os

app = Flask(__name__)

# Load model safely
with open("vectorizer.pkl", "rb") as f:
    vector = pickle.load(f)

with open("phishing.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "")

        # Clean URL
        cleaned_url = re.sub(r'^https?://(www\.)?', '', url)

        # Prediction
        predict = model.predict(vector.transform([cleaned_url]))[0]

        if predict == 'bad':
            result = " This is a Phishing website !!"
        elif predict == 'good':
            result = "This is a safe website !!"
        else:
            result = "Something went wrong !!"

        return render_template("index.html", predict=result)

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)