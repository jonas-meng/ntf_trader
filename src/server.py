import os.path

from pysondb import db
from flask import Flask, render_template

app = Flask(__name__)


def get_entries(exchange, contract_address):
    nft_data = db.getDb(os.path.realpath("db.json"))
    data = nft_data.getByQuery(query={
        "exchange": exchange
    })
    data = sorted(data, key=lambda x: x["timestamp"])
    if exchange == "nftrade":
        price_list = [float(item["data"]["price"]) for item in data if item["data"]["contractAddress"] == contract_address]
        web_link = f"https://app.nftrade.com/assets/bsc/{contract_address}"
    elif exchange == "pancakeswap":
        price_list = [float(item["data"]["currentAskPrice"]) for item in data if item["data"]["collection"]["id"] == contract_address]
        web_link = f"https://pancakeswap.finance/nfts/collections/{contract_address}"
    else:
        price_list = []
        web_link = ""
    timestamps = [item["timestamp"] for item in data]
    return {
        "exchange": exchange,
        "data": price_list,
        "labels": timestamps,
        "contract_address": contract_address,
        "web_link": web_link
    }


@app.route("/")
def index():
    chart_data_list = [
        get_entries("nftrade", "0x57a7c5d10c3f87f5617ac1c60da60082e44d539e"),
        get_entries("pancakeswap", "0x0a8901b0e25deb55a87524f0cc164e9644020eba"),
        get_entries("pancakeswap", "0xdf7952b35f24acf7fc0487d01c8d5690a60dba07"),
        get_entries("pancakeswap", "0x3da8410e6ef658c06e277a2769816688c37496cf")
    ]
    return render_template("index.html", chart_data_list=chart_data_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
