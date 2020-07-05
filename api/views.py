from flask import jsonify, render_template, request

from . import app, model


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def api():
    data = request.form["data"]
    prediction = model.predict([data])
    k = {"message": data, "classification": prediction}
    return jsonify(k)
