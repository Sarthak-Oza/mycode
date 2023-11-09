#!/usr/bin/python3
"""Alta3 Research | rzfeeser@alta3.com
   A simple Flask server. Responds to HTTP 'GET /' requests
   with a 'Hello World' attached to a 200 response"""


# An object of Flask class is our WSGI application
from flask import Flask, redirect, url_for, render_template, request

# Flask constructor takes the name of current
# module (__name__) as argument
app = Flask(__name__)

# route() function of the Flask class is a
# decorator, tells the application which URL
# should call the associated function
@app.route("/")
def home():
   return render_template("postmaker.html")

@app.route("/about")
def about():
   return "About page"

@app.route("/contact")
def contact():
   return "Contact page"

@app.route("/items")
def items():
   return {1: "TV", 2: "Mobile Phone"}

@app.route("/items/<item_id>", methods=["GET", "POST"])
def get_item(item_id):
   if request.method == "GET":
      try:
        item_id = int(item_id)
        item = {"item_id": "Item " + str(item_id)} 
        return item
      except ValueError:
        return redirect(url_for("not_found"))

   elif requests.method == "POST":
      return "POST an item"

@app.route("/notfound")
def not_found():
   return "Not Found"

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224, debug=True) # runs the application
   # app.run(host="0.0.0.0", port=2224, debug=True) # DEBUG MODE

