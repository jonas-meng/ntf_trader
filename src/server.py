import os.path

from pysondb import db
from flask import Flask, render_template

app = Flask(__name__)


def get_entries(exchange):
    nft_data = db.getDb(os.path.realpath("db.json"))
    data = nft_data.getByQuery(query={
        "exchange": exchange
    })
    data = sorted(data, key=lambda x: x["timestamp"])
    price_list = [item["data"]["price"] for item in data]
    timestamps = [item["timestamp"] for item in data]
    return {
        "data": price_list,
        "labels": timestamps
    }


@app.route("/")
def index():
    return render_template("index.html", **get_entries("nftrade"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
