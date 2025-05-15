#Created by AI for testing purposes
from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-time")
def get_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(time=now)

if __name__ == "__main__":
    app.run()