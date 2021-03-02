import pandas as pd
import datetime
from bollingers_bot import Bollingers_Bot
from trade import Trade

def process_bollinger_window(temp_date, bot, window):
    row_date = datetime.datetime.strptime(temp_date.split(" ")[0], "%Y-%m-%d").date()
    print(temp_date)
    bot.last_date = row_date
    if temp_date.split(" ")[1] == "15:55:00":
        bot.last_tick = True
    else:
        bot.last_tick = False
    bot.process_tick_data(window)

spy_data = pd.read_csv('spy_data.csv',delimiter="\t")

print(spy_data)

bollinger_window = []

bollingers_bot = Bollingers_Bot()

f = open("trade_results.csv", "a")
f.write(f'Processing Criteria:\n')
f.write(f'The Bot Processes the Bollinger Bands and enters a trade when a band is within the alert price (band - alert_gap)\n')
f.write(f'The Bot then exits the trade when exit trade price is crossed, or the end of day Wednesday / Friday (depending on trade open day.)\n')
f.write(f'Alert Gap: {bollingers_bot.alert_gap}\n')
f.write(f'Upper Band Exit: {bollingers_bot.upper_trade_exit}\nLower Band Exit: {bollingers_bot.lower_trade_exit}\n')
f.write(f'Upper Strike Multipler: {bollingers_bot.upper_trade_multipler}\nLower Strike Multipler: {bollingers_bot.lower_trade_multipler}\n')
f.write(f'Date\tBollinger Band\tAlert Price\tStrike Price\tTrade Start Date\tTrade Close Date\tTrade Close Price\tCrossed\n')
f.close()

current_trade = ""

for index, row in spy_data.iterrows():
    if index < 200:
        bollinger_window.append(round(row['close'],2))
        if len(bollinger_window) == 200:
            process_bollinger_window(row['date'], bollingers_bot, bollinger_window)
    else:
        bollinger_window.pop(0)
        bollinger_window.append(round(row['close'],2))
        process_bollinger_window(row['date'], bollingers_bot, bollinger_window)

bollingers_bot.exit_position()
print(bollingers_bot.previous_trades)
