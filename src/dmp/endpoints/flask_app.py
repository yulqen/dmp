from dmp.adaptors import repository
from dmp.domain import models
from flask import Flask

app = Flask(__name__)


@app.route("/inspectors")
def inspectors_list():
    return "bobbins", 200
