import requests
from datetime import datetime, timedelta

def download_intraday_data_and_save_to_a_txt_file(entry):

    entry = entry.split('@')
    underlying = entry[0]
    option_strike = entry[1]
    option_type = entry[2]
    option_expiry_date = entry[3]
    target_trading_date = entry[4]
    earlier_date = ((datetime.strptime(target_trading_date, "%Y-%m-%d") - timedelta(days=10)).strftime("%Y-%m-%d"))

    # Download data and save to a txt file
    url = f"https://api.polygon.io/v2/aggs/ticker/O:{underlying}{option_expiry_date[2:4]}{option_expiry_date[5:7]}{option_expiry_date[8:10]}{option_type[0]}00{option_strike}000/range/1/second/{target_trading_date}/{target_trading_date}?adjusted=true&sort=asc&limit=50000&apiKey={api_key}"
    data = requests.get(url).json()['results']
    previous_day_close = requests.get(f"https://api.polygon.io/v2/aggs/ticker/O:{underlying}{option_expiry_date[2:4]}{option_expiry_date[5:7]}{option_expiry_date[8:10]}{option_type[0]}00{option_strike}000/range/1/day/{earlier_date}/{target_trading_date}?adjusted=true&sort=asc&limit=120&apiKey={api_key}").json()['results'][-2]['c']

    string = f"v|vw|o|c|h|l|t|n\nprevious day close|{previous_day_close}\n"
    for i in data:
        s = ""
        for value in i.values():
            s = f"{s}{value}|"
        s = s[:-1]
        string = f"{string}{s}\n"
    string = string[:-1]
    with open(f"{working_directory}O|{underlying}{target_trading_date[2:4]}{target_trading_date[5:7]}{target_trading_date[8:10]}{option_type[0]}00{option_strike}000.txt", "w") as file:
        file.write(string)

def calculate_capital_trend(entry):

    entry = entry.split('@')
    underlying = entry[0]
    option_strike = entry[1]
    option_type = entry[2]
    option_expiry_date = entry[3]
    target_trading_date = entry[4]

    capital_trend = 0.0

    # Locate file and open
    file_path = f"{working_directory}O|{underlying}{target_trading_date[2:4]}{target_trading_date[5:7]}{target_trading_date[8:10]}{option_type[0]}00{option_strike}000.txt"
    previous_close = None
    container = []
    with open(file_path, "r") as file:
        content = file.readlines()
        previous_close = float((content[1].split('|')[1]))
        for each_second_data in content[2:]:
            container.append(each_second_data.strip().split('|'))

    # Calculation starts
    for each in container:
        current_close = float(each[3])
        if current_close > previous_close:
            net_capital_inflow = float(each[1]) * float(each[0]) * 100
            capital_trend = capital_trend + net_capital_inflow
            previous_close = current_close
        elif current_close < previous_close:
            net_capital_inflow = float(each[1]) * float(each[0]) * -100
            capital_trend = capital_trend + net_capital_inflow
            previous_close = current_close

    capital_trend = int(capital_trend)
    print(capital_trend)

working_directory = "/Users/curryyao/Downloads/"

entry = "QQQ@410@CALL@2023-12-27@2023-12-26"
api_key = "YOUR_API"

download_intraday_data_and_save_to_a_txt_file(entry)
calculate_capital_trend(entry)
