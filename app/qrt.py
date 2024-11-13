import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from flask import Flask, render_template, url_for
from datetime import datetime
import matplotlib.pyplot as plt
import os

import logging
from statsmodels.tsa.stattools import adfuller
from pycoingecko import CoinGeckoAPI
import io
import base64
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

#initialize coingecko api
cg = CoinGeckoAPI()
# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Set API keys and endpoints
NEWS_API_KEY = 'b814c3739ba54cbf8f8b458c6ce9818c'
NEWS_API_URL = 'https://newsapi.org/v2/everything'
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/coins/markets'

# Define start and end dates for historical data
start_date = int(datetime(2024, 1, 1).timestamp())
end_date = int(datetime(2024, 11, 6).timestamp())


def fetch_crypto_news(api_key):
    """
    Fetch cryptocurrency news articles.
    """
    params = {
        'q': 'cryptocurrency',
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt'
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        
        # Format news data
        news_data = [
            {
                'Title': article['title'],
                'Description': article.get('description', 'No description available'),
                'Source': article['source']['name'],
                'Published_At': article['publishedAt'],
                'URL': article['url'],
                'Image': article.get('urlToImage', 'https://via.placeholder.com/600x400')
            }
            for article in articles
        ]
        logging.info(f"Fetched {len(news_data)} news articles.")
        return news_data
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

def fetch_crypto_data():
    """
    Fetch cryptocurrency data and calculate rankings, along with daily changes in price, volume, and market cap.
    """
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,  # Retrieve the top 10 cryptocurrencies
        'page': 1,
        'sparkline': 'true'
    }
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()
        coins = response.json()

        # Prepare list for processed data
        crypto_data = []
        
        for coin in coins:
            # Retrieve sparkline data for calculating daily change
            prices = coin['sparkline_in_7d']['price']
            daily_changes = {
                'price': round(prices[-1] - prices[-2], 2) if len(prices) > 1 else None,
                'volume': None,  # Placeholder, as volume change data isn't provided in this endpoint
                'market_cap': None  # Placeholder, as market cap change data isn't provided in this endpoint
            }
            # Append each cryptocurrency's data including daily changes
            crypto_data.append({
                'name': coin['name'],
                'symbol': coin['symbol'].upper(),
                'price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'volume': coin['total_volume'],
                'price_change': daily_changes['price'],
                'volume_change': daily_changes['volume'],
                'market_cap_change': daily_changes['market_cap'],
                'image': coin['image'],
                'id': coin['id']
            })

        # Calculate rankings based on volume, market cap, and price
        sorted_by_volume = sorted(crypto_data, key=lambda x: x['volume'], reverse=True)
        sorted_by_market_cap = sorted(crypto_data, key=lambda x: x['market_cap'], reverse=True)
        sorted_by_price = sorted(crypto_data, key=lambda x: x['price'], reverse=True)

        # Add ranking information to each cryptocurrency
        for crypto in crypto_data:
            crypto['price_rank'] = sorted_by_price.index(crypto) + 1
            crypto['market_cap_rank'] = sorted_by_market_cap.index(crypto) + 1
            crypto['volume_rank'] = sorted_by_volume.index(crypto) + 1
        
        logging.info(f"Fetched data for {len(crypto_data)} cryptocurrencies with daily changes and rankings.")
        return crypto_data
    except Exception as e:
        logging.error(f"Error fetching crypto data: {e}")
        return []
@app.route('/')
def home():
    news_articles = fetch_crypto_news(NEWS_API_KEY)
    crypto_rankings = fetch_crypto_data()
    return render_template('index2.html', news_articles=news_articles, crypto_rankings=crypto_rankings)
def fit_time_series_models(price_series):
    """
    Fit ARIMA and SARIMA models to the price series and return forecasts.
    """
    # ARIMA model
    arima_model = ARIMA(price_series, order=(5, 1, 0))  # Adjust (p, d, q) as necessary
    arima_fit = arima_model.fit()
    arima_forecast = arima_fit.forecast(steps=30)  # Forecast next 30 time periods

    # SARIMA model
    sarima_model = SARIMAX(price_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    sarima_fit = sarima_model.fit()
    sarima_forecast = sarima_fit.forecast(steps=30)  # Forecast next 30 time periods

    return arima_forecast, sarima_forecast

def fetch_price_series(coin_id):
    """
    Fetch historical price data for a specific cryptocurrency.
    """
    try:
        # Fetch historical data for the specified coin
        data = cg.get_coin_market_chart_range_by_id(
            id=coin_id,
            vs_currency='usd',
            from_timestamp=start_date,
            to_timestamp=end_date
        )
        
        # Create a DataFrame with the timestamp and price columns
        df = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])
        
        # Convert timestamp to a readable date format
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        
        # Set the timestamp as the index for time series analysis
        df.set_index('Timestamp', inplace=True)
        
        # Return the price series
        return df['Price']
    except Exception as e:
        logging.error(f"Error fetching data for {coin_id}: {e}")
        return None

@app.route('/predict/<coin_id>')
def predict_coin_price(coin_id):
    # Fetch the full price series for the coin
    price_series = fetch_price_series(coin_id)
    if price_series is None:
        return f"Error: Could not fetch data for {coin_id}"

    # Define the number of days for backtesting and future prediction
    test_days = 10
    future_days = 2

    # Split the data into training and testing sets for backtesting
    train_data = price_series[:-test_days]
    test_data = price_series[-test_days:]

    # Initialize lists to store backtest predictions
    arima_backtest = []
    sarima_backtest = []

    # Perform rolling predictions for each day in the test period
    for i in range(test_days):
        # Update training data up to the i-th test day
        current_train_data = price_series[:-(test_days - i)]

        # ARIMA model
        arima_model = ARIMA(current_train_data, order=(5, 1, 0))
        arima_fit = arima_model.fit()
        arima_backtest.append(arima_fit.forecast(steps=1)[0])

        # SARIMA model
        sarima_model = SARIMAX(current_train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        sarima_fit = sarima_model.fit()
        sarima_backtest.append(sarima_fit.forecast(steps=1)[0])

    # Future forecasting after the test period
    arima_future_forecast = arima_fit.forecast(steps=future_days)
    sarima_future_forecast = sarima_fit.forecast(steps=future_days)

    # Plot historical data, backtest forecasts, and future forecasts
    plt.figure(figsize=(14, 7))

    # Plot historical prices for context
    plt.plot(price_series[-(2 * test_days):], label=f'{coin_id.capitalize()} Historical Price', color='blue')

    # Plot backtest forecast
    plt.plot(test_data.index, arima_backtest, label='ARIMA Backtest Forecast', color='red', linestyle='--')
    plt.plot(test_data.index, sarima_backtest, label='SARIMA Backtest Forecast', color='orange', linestyle='--')

    # Plot future forecast beyond the historical data
    future_index = pd.date_range(test_data.index[-1] + pd.Timedelta(days=1), periods=future_days)
    plt.plot(future_index, arima_future_forecast, label='ARIMA Future Forecast', color='red')
    plt.plot(future_index, sarima_future_forecast, label='SARIMA Future Forecast', color='orange')

    # Customize plot
    plt.title(f'{coin_id.capitalize()} Price Forecast - Backtest and Future Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()

    # Save the plot to display on the webpage
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('prediction.html', coin_id=coin_id, plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)