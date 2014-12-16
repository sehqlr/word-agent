from flask import Flask, escape
from app.backend import *

app = Flask(__name__)

@app.route("/")
def hello():
    return escape("<h1>Dockerized WordAgent coming to a computer near you!</h1>")

@app.route("/api/<cmd>", methods=['POST'])
def execute(cmd):
    if request.method == "POST":
        if cmd in api_handlers:
            api_handlers[cmd](request.form) #TODO: I have no idea if this works
    else:
        flash("Command not recognized")


if __name__ == "__main__":
    app.run()
