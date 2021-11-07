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
    if exchange == "nftrade":
        price_list = [float(item["data"]["price"]) for item in data]
        contract_address = data[0]["data"]["contractAddress"]
        web_link = f"https://app.nftrade.com/assets/bsc/{contract_address}"
    elif exchange == "pancakeswap":
        price_list = [float(item["data"]["currentAskPrice"]) for item in data]
        contract_address = data[0]["data"]["collection"]["id"]
        web_link = f"https://pancakeswap.finance/nfts/collections/{contract_address}"
    else:
        price_list = []
        contract_address = ""
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
    chart_data_list = [get_entries("nftrade"), get_entries("pancakeswap")]
    return render_template("index.html", chart_data_list=chart_data_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
