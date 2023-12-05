# capital-trend-calculator

Code written by @Curry Yao, CEO of Regentquant, CEO of Century KY.

The calculator is used to measure amount of money flowing in and out of a given asset (stock/ETF).

Use second interval to maximize precision. If tick data is available, then use tick data.

Main Idea:
1. Downloading data from polygon.
2. Cleaning data. If no trade happens in a given time interval, api provider skips the data. So we have to clean the data. Check code if you want to know what I mean. I apologize for not writing an user friendly code.
3. Calculating. If price goes up, then accum += price * volume * 1; if price goes down, then accum -= price * volume * -1; if price remains same, then accum += 0.

Hope you find this calculator useful.
We also maintain over 200 assets' capital trend update. Visit: https://www.regentquant.com/capital-trend-dashboard.html

Change max_worker depending on your computing power.
