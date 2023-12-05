import os
import threading

import pyperclip
import requests
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pytz
from datetime import datetime
import json
import time

# FUNCTION
def downloading_json(ticker, date):

    # API endpoint
    api = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/second/{date}/{date}?adjusted=true&sort=asc&limit=50000&apiKey={api_key}'
    # Initialize dictionary
    dict = {}
    # Time range in milliseconds (UTC)
    for i in np.arange(1700643600000, 1700701189000, 1000):
        # Convert the timestamp to seconds
        timestamp_s_new = i / 1000
        new_york_tz = pytz.timezone('America/New_York')

        # Convert the timestamp to a datetime object in UTC
        datetime_utc_new = datetime.utcfromtimestamp(timestamp_s_new)
        # Convert the datetime object to New York timezone
        datetime_new_york_new = new_york_tz.fromutc(datetime_utc_new)

        dict[(datetime_new_york_new.strftime('%Y-%m-%d %H:%M:%S %Z%z')[11:19])] = []

    # Fetch data
    data = requests.get(api, headers={'Cache-Control': 'no-cache'}).json()['results']

    # Lists to hold data
    price_list = [] # Stock price
    volume_list = [] # Volume
    timestamp_list = [] # Timestamps
    datetime_list = [] # Datetime
    # Extracting data
    for item in data:
        timestamp_list.append(item['t'])
        price_list.append(item['c'])
        volume_list.append(item['v'])

        # Convert the timestamp to a datetime object in UTC
        datetime_utc = datetime.utcfromtimestamp(item['t'] / 1000)

        # Convert the datetime object to New York timezone
        datetime_new_york = new_york_tz.fromutc(datetime_utc)

        datetime_list.append(datetime_new_york.strftime('%Y-%m-%d %H:%M:%S %Z%z'))


    # Save data as a json file
    json_data = {
        "prices": price_list,
        "volumes": volume_list,
        "timestamps": timestamp_list,
        "datetimes": datetime_list
    }
    # Save to a file
    file_path = f'/Users/curryyao/Downloads/{date}-{ticker}.json'
    with open(file_path, 'w') as file:
        json.dump(json_data, file)
    file.close()
# FUNCTION
def main(filename, ticker):
    import os

    import requests
    import numpy as np
    import pytz
    from datetime import datetime
    import json
    from datetime import datetime, timezone, timedelta
    import yfinance as yf
    filename = filename
    # Load the JSON file again
    with open(f"/Users/curryyao/Downloads/{filename}", 'r') as file:
        full_data = json.load(file)

    # Display the structure of the JSON data
    structure = {key: type(full_data[key]) for key in full_data}

    time_4_am = f"{filename[:10]} 09:31:33"
    time_4_pm = f"{filename[:10]} 16:00:00"


    uncleaned_data_dict = {}
    prices = [i for i in full_data['prices']]
    volumes = [i for i in full_data['volumes']]
    timestamps = [i for i in full_data['timestamps']]
    datetimes = [i[:19] for i in full_data['datetimes']]


    # Start and end times
    start_time = datetime.strptime("04:00:00", "%H:%M:%S")
    end_time = datetime.strptime("16:00:00", "%H:%M:%S")

    data_container = {}

    # Generate times every second
    current_time = start_time
    while current_time <= end_time:
        time = (f'{filename[:10]} {current_time.strftime("%H:%M:%S")}')
        data_container[time] = []
        current_time += timedelta(seconds=1)

    for datetime, volume, price in zip(datetimes, volumes, prices):
        list = []
        list.append(volume)
        list.append(price)
        data_container[datetime] = list


    # Initializing First Data
    from datetime import datetime, timedelta
    # Given date
    date_str = f'{filename[:10]}'
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Calculate 10 days earlier
    earlier_date = date_obj - timedelta(days=10)
    # Convert back to string
    earlier_date_str = earlier_date.strftime('%Y-%m-%d')
    api_request = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{earlier_date_str}/{date_str}?adjusted=true&sort=asc&apiKey={api_key}"
    previous_day_close = (requests.get(api_request).json()['results'][-2]['c'])

    # Printing the first key and value
    first_key = next(iter(data_container))
    first_value = data_container[first_key]
    if first_value == []:
        tmp_list = [0]
        tmp_list.append(previous_day_close)
        data_container[first_key] = tmp_list

    # Cleaning Data
    first_key = next(iter(data_container))
    first_value = data_container[first_key]
    previous_list = first_value
    for key, value in data_container.items():
        if value == []:
            data_container[key] = previous_list
            tmp_list = [0]
            tmp_list.append(previous_list[1])
            previous_list = tmp_list
        else:
            tmp_list = [0]
            tmp_list.append(previous_list[1])
            previous_list = tmp_list

    is_holiday = False
    if filename[:10] in early_close:
        is_holiday = True

    if is_holiday:
        # Converting To List
        datetime_list = []
        volume_list = []
        price_list = []
        for key, value in data_container.items():
            datetime_list.append(key)
            volume_list.append(value[0])
            price_list.append(value[1])
        # Targeting 09:29:59
        index_a = (datetime_list.index(f"{filename[:10]} 09:29:59"))
        # Targeting 09:30:00
        index_b = (datetime_list.index(f"{filename[:10]} 09:30:00"))
        # Targeting 16:00:00
        index_c = (datetime_list.index(f"{filename[:10]} 13:00:00"))

        # Calculation Starts

        target_datetime_list = datetime_list[index_b: index_c+1]
        target_volume_list = volume_list[index_b: index_c+1]
        target_price_list = price_list[index_b: index_c+1]

        # Intializing previous close
        previous_close_time = datetime_list[index_a] # For debugging
        previous_close = price_list[index_a]

        amount_list = []
        # Loop starts
        for datetime, volume, price in zip(target_datetime_list, target_volume_list, target_price_list):

            if price > previous_close:
                amount_list.append(price * volume)
                previous_close = price
            elif price < previous_close:
                amount_list.append(price * volume * -1)
                previous_close = price
            else:
                amount_list.append(0)
                previous_close = price

        #print(f"{ticker}\t{filename[:10]}\t{previous_close_time}\t{datetime_list[index_b]}\t{datetime_list[index_c]}\t{len(target_datetime_list)}\t{int(sum(amount_list))}")
        return (filename[:10], f"{ticker}\t{filename[:10]}\t{int(sum(amount_list))}")

        file.close()

    else:

        # Converting To List
        datetime_list = []
        volume_list = []
        price_list = []
        for key, value in data_container.items():
            datetime_list.append(key)
            volume_list.append(value[0])
            price_list.append(value[1])
        # Targeting 09:29:59
        index_a = (datetime_list.index(f"{filename[:10]} 09:29:59"))
        # Targeting 09:30:00
        index_b = (datetime_list.index(f"{filename[:10]} 09:30:00"))
        # Targeting 16:00:00
        index_c = (datetime_list.index(f"{filename[:10]} 16:00:00"))

        # Calculation Starts

        target_datetime_list = datetime_list[index_b: index_c + 1]
        target_volume_list = volume_list[index_b: index_c + 1]
        target_price_list = price_list[index_b: index_c + 1]

        # Intializing previous close
        previous_close_time = datetime_list[index_a]  # For debugging
        previous_close = price_list[index_a]

        amount_list = []
        # Loop starts
        for datetime, volume, price in zip(target_datetime_list, target_volume_list, target_price_list):

            if price > previous_close:
                amount_list.append(price * volume)
                previous_close = price
            elif price < previous_close:
                amount_list.append(price * volume * -1)
                previous_close = price
            else:
                amount_list.append(0)
                previous_close = price

        #print(f"{ticker}\t{filename[:10]}\t{previous_close_time}\t{datetime_list[index_b]}\t{datetime_list[index_c]}\t{len(target_datetime_list)}\t{int(sum(amount_list))}")
        return (filename[:10], f"{ticker}\t{filename[:10]}\t{int(sum(amount_list))}")
        file.close()

# EARLY CLOSE & API KEY
early_close = ['2013-07-03', '2013-11-29', '2013-12-24', '2014-07-03', '2014-11-28', '2014-12-24', '2015-07-02', '2015-11-27', '2015-12-24', '2016-11-25', '2017-07-03', '2017-11-24', '2018-07-03', '2018-11-23', '2018-12-24', '2019-07-03', '2019-11-29', '2019-12-24', '2020-07-02', '2020-11-27', '2020-12-24', '2021-11-26', '2021-12-24', '2022-11-25', '2023-07-03', '2023-11-24']
api_key = '' # Polygon.io API KEY

def macro_main():

    # CONFIGURATION STARTS

    # Tickers that you want to calculate. You can enter multiple
    tickers = '''TSLT
NVDA
AAPL'''.split('\n')

    # Dates to calculate
    dates = '''2023-10-20
2023-10-23
2023-10-24
2023-10-25
2023-10-26
2023-10-27
2023-10-30
2023-10-31
2023-11-01
2023-11-02
2023-11-03
2023-11-06
2023-11-07
2023-11-08
2023-11-09
2023-11-10
2023-11-13
2023-11-14
2023-11-15
2023-11-16
2023-11-17
2023-11-20
2023-11-21
2023-11-22
2023-11-24
2023-11-27
2023-11-28
2023-11-29
2023-11-30
2023-12-01
2023-12-04'''.split('\n')
    directory = '/Users/curryyao/Downloads/' # Replace with your directory
    # CONFIGURATION ENDS


    for ticker in tickers:

        async def fetch_data(session, url, file_name):
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    with open(file_name, 'w') as file:
                        json.dump(data['results'], file)

        async def data_preparation():
            directory = '/Users/curryyao/Downloads/'

            async with aiohttp.ClientSession() as session:
                tasks = []
                for date in dates:
                    api_url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/second/{date}/{date}?adjusted=true&sort=asc&limit=50000&apiKey={api_key}'
                    file_name = f"{directory}{ticker}_{date.strip()}.json"
                    tasks.append(fetch_data(session, api_url, file_name))
                await asyncio.gather(*tasks)


        s = time.time()

        # Run the async function
        asyncio.run(data_preparation())



        # Using ThreadPoolExecutor to process multiple dates in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(downloading_json, ticker, date) for date in dates]
            for future in futures:
                future.result()  # Handling the returned result or exceptions if any This line is optional, it's for handling the returned result or exceptions if any

        print(f"Stage 1 Data Processing Complete")

        # Collecting results from ThreadPoolExecutor
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(main, f"{date}-{ticker}.json", ticker) for date in dates]
            for future in futures:
                date, result = future.result()  # Collecting the result
                results.append((date, result))

        print(f"Stage 2 Data Processing Complete")

        # Sorting results based on dates
        sorted_results = sorted(results, key=lambda x: x[0])

        # Printing sorted results
        for _, result in sorted_results:
            print(result)

        for i in dates:
            os.remove(f"{directory}{i}-{ticker}.json")
            os.remove(f"{directory}{ticker}_{i}.json")

        e = time.time()

        print(e-s)



def single_day():
    start = time.time()
    tickers = "ETF:SPY	ETF:QQQ	ETF:SQQQ	ETF:TQQQ	ETF:XLF	ETF:SOXL	STOCK:NVDA	STOCK:TSLA	STOCK:AAPL	STOCK:AMZN	STOCK:META	STOCK:NFLX	STOCK:GOOGL	STOCK:AVGO	STOCK:AMD	STOCK:SNOW	STOCK:LLY	STOCK:V	STOCK:UNH	STOCK:JPM	STOCK:WMT	STOCK:XOM	STOCK:MRK	STOCK:KO	STOCK:ABBV	STOCK:BAC	STOCK:PEP	STOCK:PG	STOCK:ORCL	STOCK:HD	STOCK:ADBE	STOCK:CVX	STOCK:COST	STOCK:MA	STOCK:JNJ	ETF:IWM	ETF:TLT	ETF:IVV	ETF:EFA	ETF:VOO	ETF:XLV	ETF:SMH	ETF:GLD	ETF:ARKK	ETF:UVXY	ETF:SOXS	ETF:IWF	STOCK:BRK.A	STOCK:MSFT	STOCK:UBER	STOCK:INTC	STOCK:DIS	STOCK:MARA	STOCK:QCOM	STOCK:DE	STOCK:MSTR	STOCK:MELI	STOCK:CRM	STOCK:CSCO	STOCK:PYPL	STOCK:BKNG	STOCK:SHOP	STOCK:TMO	STOCK:CRWD	STOCK:MCD	STOCK:INTU	STOCK:PFE	STOCK:MU	STOCK:SBUX	STOCK:COIN	STOCK:PLTR	STOCK:ARM	STOCK:NVO	STOCK:ASML	STOCK:LULU	STOCK:HLT	STOCK:IHG	STOCK:GOOG	STOCK:COF	STOCK:ACN	STOCK:LIN	STOCK:BABA	STOCK:ABT	STOCK:TMUS	STOCK:CMCSA	STOCK:NKE	STOCK:DHR	STOCK:PDD	STOCK:VZ	STOCK:WFC	STOCK:IBM	STOCK:AMGN	STOCK:TXN	STOCK:COP	STOCK:UNP	STOCK:SPGI	STOCK:GE	STOCK:BX	STOCK:UPS	STOCK:HON	STOCK:AMAT	STOCK:CAT	STOCK:AXP	STOCK:NEE	STOCK:LOW	STOCK:RTX	STOCK:ELV	STOCK:SYK	STOCK:ISRG	STOCK:LMT	STOCK:GS	STOCK:BLK	STOCK:MDT	STOCK:SCHW	STOCK:TJX	STOCK:BMY	STOCK:MMC	STOCK:MDLZ	STOCK:PGR	STOCK:LRCX	STOCK:ADP	STOCK:GILD	STOCK:CB	STOCK:ETN	STOCK:ADI	STOCK:VRTX	STOCK:CVS	STOCK:REGN	ETF:HYG	ETF:LQD	ETF:XLE	ETF:XLI	ETF:EEM	ETF:DIA	ETF:IEF	ETF:AGG	ETF:BIL	ETF:XLP	ETF:ACWI	ETF:XLU	ETF:XLK	ETF:IWD	ETF:FXI	ETF:USMV	ETF:XLY	ETF:VTEB	ETF:RSP	ETF:VTV	ETF:SPXL	ETF:IGV	ETF:XOP	ETF:IEMG	ETF:VTI	ETF:XBI	ETF:IYR	ETF:JNK	ETF:EWZ	ETF:MUB	ETF:KWEB	ETF:IEFA	ETF:VEA	ETF:VNQ	ETF:SLV	ETF:EMB	ETF:IWB	ETF:VWO	ETF:MBB	ETF:IJH	ETF:HYLB	ETF:KRE	ETF:IEI	ETF:VCIT	ETF:VCSH	ETF:SCHD	ETF:BND	ETF:GDXJ	ETF:IJR	ETF:XRT	ETF:SHY	ETF:USO	ETF:MDY	ETF:VIG	ETF:TLH	ETF:SOXX	ETF:VUG	ETF:TNA	ETF:SGOV	ETF:JMBS	ETF:XLC	ETF:BIV	ETF:XLB	ETF:JEPI	ETF:SPYG	ETF:EWJ	ETF:IGSB	ETF:TZA	ETF:BSV	ETF:TIP	ETF:BOIL	ETF:SHV	ETF:XME	ETF:SPLG	ETF:EWY	ETF:SPIB	ETF:PSQ	ETF:IBB	ETF:VGT	ETF:KIE	ETF:IVW".split('\t')
    tickers = [i.split(":")[1] for i in tickers]
    date = "2023-12-04"
    threads = []
    for ticker in tickers:
        thread = threading.Thread(target=downloading_json, args=(ticker, date))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    results = []

    for ticker in tickers:
        results.append(main(f"{date}-{ticker}.json", ticker))
    fs = ""

    for i in results:
        print(i)
        value = (i[1].split('\t')[-1])
        fs = f"{fs}{value}\t"

    print(fs[:-1])
    end = time.time()
    print(f"Time spent: {round(end - start, 2)}")


macro_main()
