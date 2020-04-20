from flask import Flask, render_template, url_for, request, json, jsonify
from flask_socketio import SocketIO, emit
from threading import Lock
# import easyquotation
import pandas as pd
import numpy as np
import tushare as ts
import datetime
import itertools
import talib
import pickle
import time
import os

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "secret!"
async_mode = None
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
thread = None
thread_lock = Lock()

# pairs = {"房地产": {"600048": "保利地产", "000002": "万科A"},
#          "券商": {"600837": "海通证券", "601211": "国泰君安"},
#          "保险": {"601336": "新华保险", "601628": "中国人寿"},
#          "基建": {"601186": "中国铁建", "601800": "中国交建"}}
pairs = {"房地产": {"600048": "保利地产", "000002": "万科A"}}
pair_stock = ["600048", "000002", "600837", "601211", "601336", "601628", "601186", "601800"]
# quotation = easyquotation.use("sina")
chosen_pairs = "房地产"


@app.route("/", methods=["GET", "POST"])
def display_stock():
    contents = {"pairs": pairs}
    if request.method == "GET":
        return render_template("stockrealtime.html", **contents)
    else:
        select_kind = request.get_json()
        if select_kind is None:
            return render_template("stockrealtime.html", **contents)
        else:
            if len(select_kind.keys()) == 1:
                global chosen_pairs
                chosen_pairs = select_kind["pairs"]
                return {0: "OK!"}
            else:
                return render_template("stockrealtime.html", **contents)


def getstockdata():
    if chosen_pairs is not None:
        stock1 = list(pairs[chosen_pairs].keys())[0]
        stock2 = list(pairs[chosen_pairs].keys())[1]
        while True:
            socketio.sleep(5)
            with open("./files/stocktodayhisdata.pkl", "rb") as f:
                his_data = pickle.load(f)
            time_l, stock1_l, stock2_l = his_data["Time"], his_data[stock1], his_data[stock2]
            stock1_open = stock1_l[0]
            stock2_open = stock2_l[0]
            diff = (np.array(stock1_l) / stock1_open - np.array(stock2_l) / stock2_open).tolist()
            data = {"Time": time_l, stock1: stock1_l, stock2: stock2_l, "涨跌幅差": diff}
            socketio.emit("server_response", data, namespace="/stockdata")


@socketio.on("connect", namespace="/stockdata")
def stockdata():
    if chosen_pairs is not None:
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(target=getstockdata)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5001
    socketio.run(app, host=host, port=port, debug=True)
