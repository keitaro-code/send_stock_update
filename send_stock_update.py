import yfinance as yf
import requests
import datetime

# LINE Notifyのトークン
LINE_TOKEN = "XVA2ErHPlRAC1aVXZ1TqwPtfMhZIPIZcL0k0xzXnfhx"

# 取得株価と取得株数
purchase_price = 10.0
number_of_shares = 100

def send_stock_update():
    # 前日の日付を取得
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # 前日の株価を取得
    oklo = yf.Ticker("OKLO").history(start=yesterday, end=today)
    if oklo.empty:
        message = "前日の株価データが取得できませんでした。"
    else:
        oklo_data = oklo["Close"][0]
        # 損益計算
        current_value = oklo_data * number_of_shares
        initial_value = purchase_price * number_of_shares
        profit_loss = current_value - initial_value
        profit_loss_percentage = (profit_loss / initial_value) * 100

        # メッセージ作成
        message = (f"前日の株価 \nOKLO : ${oklo_data:.2f}\n"
                   f"取得株価 : ${purchase_price:.2f}\n"
                   f"取得株数 : {number_of_shares}株\n"
                   f"現在の評価額 : ${current_value:.2f}\n"
                   f"損益 : ${profit_loss:.2f}\n"
                   f"損益率 : {profit_loss_percentage:.2f}%")

    # LINEにメッセージを送る
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    requests.post(line_notify_api, headers=headers, data=payload)

# 株価通知関数を実行
send_stock_update()
