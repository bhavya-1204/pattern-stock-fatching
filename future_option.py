# from flask import Flask, request, render_template
import pandas as pd
import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None

def calculate_ema(df, period):
    """
    Calculate Exponential Moving Average (EMA) for a given period.
    Returns None if insufficient data.
    """
    if len(df) < period:
        return None
    return df['Close'].ewm(span=period, adjust=False).mean()

def find_big_candle(data):
    final_result = -1  # Initialize with -1 to indicate no big candle found
    for i in range(1, len(data)):
        if ((round(data['Close'].iloc[i].item(), 2)) - round(data['Close'].iloc[i-1].item(), 2)) / round(data['Close'].iloc[i-1].item(),2) > 0.02:
            final_result = i
    return final_result

def fetch_price(data):
    final_result = find_big_candle(data)
    days = 3

    # Check if we found a big candle and if we have enough data
    if final_result == -1:
        return False

    # Check if we have enough data after the big candle
    if final_result + days >= len(data):
        return False

    firstday_percentage = ((round(data['Close'].iloc[final_result].item(), 2)) - round(data['Close'].iloc[final_result - 1].item(), 2)) / round(data['Close'].iloc[final_result - 1].item())

    if (round(data['Close'].iloc[final_result].item(), 2)) > round(calculate_ema(data, 9).iloc[final_result].item()):


        if firstday_percentage > 0.02:              #____________ADDED____2________MAIN________
            # Check if we can access final_result + 1
            if final_result + 1 < len(data):
                if round(data['Close'].iloc[final_result + 1].item(), 2) < round(data['Open'].iloc[final_result + 1].item(), 2):
                    starting = round(data['Open'].iloc[final_result + 1].item(), 2)
                else:
                    starting = round(data['Close'].iloc[final_result + 1].item(), 2)
            else:
                print("Cannot access data after big candle")
                return False

            current_volume = data['Volume'].iloc[-1].item()
            targeted_volume = data['Volume'].iloc[final_result + days].item()

            if current_volume == targeted_volume:
                if round(data['Close'].iloc[-1].item(), 2) > round(data['Open'].iloc[-1].item(), 2):
                    ending = round(data['Open'].iloc[-1].item(), 2)
                else:
                    ending = round(data['Close'].iloc[-1].item(), 2)

                for i in range(final_result+2, len(data)):
                    if round(data['Close'].iloc[i].item(), 2) > starting or round(data['Open'].iloc[i].item(), 2) > starting or round(data['Close'].iloc[i].item(), 2) < ending or round(data['Open'].iloc[i].item(), 2) < ending:
                        return False
                    else :
                        percentage_value = ((starting - ending) / starting)

                        if percentage_value > -0.2 and percentage_value < 0.2:
                            return True
                        else:
                            return False
    else:
        return False
    return True

def check_close_of_ema(data):
    result = []

    # Basic validations
    if data is None or len(data) == 0:
        return result

    ema_20_series = calculate_ema(data, 20)
    ema_9_series = calculate_ema(data, 9)
    if ema_20_series is None or ema_9_series is None:
        return result

    latest_ema_20 = ema_20_series.iloc[-1].item()
    latest_ema_9 = ema_9_series.iloc[-1].item()

    if pd.isna(latest_ema_20) or pd.isna(latest_ema_9):
        return result

    ema_20 = float(latest_ema_20)
    ema_9 = float(latest_ema_9)

    last_close = float(data['Close'].iloc[-1].item())
    prev_close = float(data['Close'].iloc[-2].item())

    if prev_close > last_close:
        return result

    final_result = find_big_candle(data)
    if final_result == -1:
        return result

    main_low = float(data['Low'].iloc[final_result].item())
    main_high = float(data['High'].iloc[final_result].item())

    for i in range(final_result + 1, len(data)):
        ema20 = ema_20_series.iloc[i].item()
        ema9 = ema_9_series.iloc[i].item()
        close = data['Close'].iloc[i].item()

        if pd.isna(ema20) or pd.isna(ema9) or pd.isna(close):
            continue

        if close < main_low or close < ema20 or close > main_high:
            return result

    if last_close > ema_20 and last_close > ema_9:
        if fetch_price(data):
            result.append({
                'stock name': data.columns[0][1].split('.')[0],
                'price': last_close
            })

    return result


def index():
    all_results = []

    symbol_name_csv = pd.read_csv('csv_files/F&O.csv')
    nse_stock = [symbol + '.NS' for symbol in symbol_name_csv['Symbol']]

    for ticker in nse_stock:
        data = yf.download(
            ticker,
            period="30d",
            interval="1d",
            progress=False,
            threads=False
        )

        if data is None or data.empty:
            continue

        condition = check_close_of_ema(data)
        df = pd.DataFrame(condition)

        if not df.empty:
            all_results.append(df)

    if all_results:
        return pd.concat(all_results, ignore_index=True)

    return pd.DataFrame()

if __name__ == "__main__":
    stock = index()
    # print(result)
