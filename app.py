from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("landingpage.html")

@app.route("/mapwi")
def mapwi():
    return render_template("map_wi.html")


if __name__ == "__main__":
    app.run(debug=True)