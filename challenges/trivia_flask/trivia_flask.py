#!/usr/bin/python3

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
   return render_template("triviaquestion.html")

@app.route("/submit", methods=["POST"])
def submit():
   answer = request.form.get("answer")

   if answer == "Moving Picture":
      return redirect(url_for("correct"))
   else:
      return redirect(url_for("home"))

@app.route("/correct")
def correct():
    return "Your answer is correct."

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224, debug=True)
