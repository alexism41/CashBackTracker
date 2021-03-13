from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/Categories")
def Categories():
    return render_template("categories.html")

if __name__ == "__main__":
    app.run(debug = True)