from flask import Flask, redirect, url_for, render_template
from parse import getBestInEach, cardList

app = Flask(__name__)
deals = getBestInEach()
data = cardList
headers = ("Category", "Cash Back %")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", deals = deals)

@app.route("/Cards")
def Categories():
    return render_template("categories.html", headers= headers, cList = data)

if __name__ == "__main__":
    app.run(debug = True)