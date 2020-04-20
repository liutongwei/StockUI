import easyquotation
import datetime
import pickle
import time

global data
data = {"Time": [], "600048": [], "000002": [], "600837": [],
        "601211": [], "601336": [], "601628": [], "601186": [], "601800": []}


def today_history(data, quotation, pair_stock):
    today = datetime.datetime.today()
    if today.weekday() == 5 or today.weekday() == 6 or datetime.datetime.now() < datetime.datetime(today.year, today.month, today.day, 9, 30, 0) \
            or datetime.datetime.now() > datetime.datetime(today.year, today.month, today.day, 15, 1, 0) or \
        (datetime.datetime.now() > datetime.datetime(today.year, today.month, today.day, 11, 30, 0) and \
     datetime.datetime.now() < datetime.datetime(today.year, today.month, today.day, 13, 0, 0)):
        data = {"Time": [], "600048": [], "000002": [], "600837": [],
                "601211": [], "601336": [], "601628": [], "601186": [], "601800": []}
        return
    a = quotation.stocks(pair_stock)
    data["Time"].append(a["600048"]["time"])
    for i in pair_stock:
        data[i].append(a[i]["now"])
    with open("./files/stocktodayhisdata.pkl", "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    pair_stock = ["600048", "000002", "600837", "601211", "601336", "601628", "601186", "601800"]
    quotation = easyquotation.use("sina")
    while True:
        time.sleep(1)
        today_history(data, quotation, pair_stock)
