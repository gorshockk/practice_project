from flask import Flask, render_template, request
import pickle
import numpy as np
import yfinance as yf
import pandas as pd

# Загружаем модель
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)


def get_last_btc_day():
    import yfinance as yf

    # Загружаем исторические данные
    btc = yf.Ticker("BTC-USD")
    hist = btc.history(period="5d")

    # Берем последние 2 строки и сбрасываем индекс
    last_two = hist.tail(2).reset_index()

    # Удаляем ненужные столбцы
    last_two = last_two.drop(columns=["Dividends", "Stock Splits", "Date"])

    # Добавляем столбец Change (изменение %)
    last_two["Change"] = last_two["Close"].pct_change() * 100

    return last_two.drop([0])

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    btc_features = {}

    # Получаем признаки BTC
    try:
        btc_data = get_last_btc_day()
        row = btc_data.iloc[0]  # первая (и единственная) строка
        btc_features = {
            "Open": round(row["Open"], 2),
            "High": round(row["High"], 2),
            "Low": round(row["Low"], 2),
            "Close": round(row["Close"], 2),
            "Volume": round(row["Volume"], 2),
            "Change": round(row["Change"], 2)
        }
    except Exception as e:
        btc_features = {
            "Open": "—", "High": "—", "Low": "—",
            "Close": "—", "Volume": "—", "Change": "Ошибка"
        }

    # Обработка формы
    if request.method == "POST":
        try:
            data = [
                float(request.form["open"]),
                float(request.form["high"]),
                float(request.form["low"]),
                float(request.form["close"]),
                float(request.form["volume"]),
                float(request.form["change"])
            ]
            data = np.array(data).reshape(1, -1)
            result = model.predict(data)
            prediction = "Цена ВЫРАСТЕТ 🚀" if result[0] == 1 else "Цена НЕ вырастет 📉"
        except:
            prediction = "Ошибка при обработке данных"

    return render_template("index.html", prediction=prediction, btc_features=btc_features)


if __name__ == "__main__":
    app.run(debug=True)