import os
import requests
import json
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_api_key = os.environ.get("STOCK_api_key")
NEWS_api_key = os.environ.get("NEWS_api_key")

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
client = Client(account_sid, auth_token)


stock_parameters = {
    "apikey": STOCK_api_key,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "15min"
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_api_key
}

#Yesterday's closing price
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
daily_prices = stock_response.json()["Time Series (Daily)"]
stock_list = [value for (key, value) in daily_prices.items()]
yesterday_cls_price = stock_list[0]["4. close"]

#Day before yesterday's closing price
dby_cls_price = stock_list[1]["4. close"]

price_diff = float(dby_cls_price)-float(yesterday_cls_price)
if price_diff > 0:
    symbol = "⬆"
if price_diff < 0:
    symbol = "⬇"

diff_percentage = round((abs(price_diff)/float(yesterday_cls_price))*100, 2)
print(diff_percentage)

if diff_percentage > 4:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_articles = news_response.json()["articles"][:3]

    article_list = [f"{COMPANY_NAME}: {symbol} {diff_percentage}% \nHeadline: {item['title']}. \nBrief: {item['description']}." for item in news_articles]

    for i in article_list:
        message = client.messages.create(
            from_ = 'whatsapp:+14155238886',
            body = i,
            to = 'whatsapp:+27715603202'
        )
        print(i)
