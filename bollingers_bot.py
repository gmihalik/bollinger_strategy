import os
import json
import requests
import statistics
import datetime
from trade import Trade

class Bollingers_Bot():
    def __init__(self):
        self.account_balance = 0
        self.alert_sent = False
        self.upper_bollinger_band = 0
        self.lower_bollinger_band = 0
        self.lower_bollinger_alert = 0
        self.upper_bollinger_alert = 0
        self.last_price = 0
        self.moving_average = 0
        self.tick_average = []
        self.stock_json = {}
        self.in_trade = False
        self.alert = False
        self.previous_trades = []
        self.current_trade = None
        self.band = ""
        self.last_date = None
        self.last_tick = False
        self.alert_gap = 0.75
        self.upper_trade_exit = 0.9875
        self.lower_trade_exit = 1.0125
        self.upper_trade_multipler = 1.0125
        self.lower_trade_multipler = 0.975

    def process_tick_data(self,tick_data):
        self.tick_average = round(statistics.mean(tick_data),2)
        self.moving_average = self.tick_average
        self.stand_dev = statistics.stdev(tick_data)
        self.upper_bollinger_band = round(self.moving_average + 2 * self.stand_dev,2)
        self.lower_bollinger_band = round(self.moving_average - 2 * self.stand_dev,2)
        self.last_price = tick_data[-1]
        self.bollinger_spread = (self.upper_bollinger_band - self.lower_bollinger_band)*.1
        #self.upper_bollinger_alert = round(self.upper_bollinger_band - self.bollinger_spread,2)
        #self.lower_bollinger_alert = round(self.lower_bollinger_band + self.bollinger_spread,2)
        self.upper_bollinger_alert = round(self.upper_bollinger_band - self.alert_gap,2)
        self.lower_bollinger_alert = round(self.lower_bollinger_band + self.alert_gap,2)
        self.process_bollinger_bands()

    def process_bollinger_bands(self):
        if self.last_price >= self.upper_bollinger_alert:
            self.alert = True
            self.band = "UPPER"
            alert_message = "Price has crossed Upper Bollinger Alert Threshold"
        elif self.last_price <= self.lower_bollinger_alert:
            self.alert = True
            self.band = "LOWER"
            alert_message = "Price has crossed Lower Bollinger Alert Threshold"
        elif self.last_price >= self.upper_bollinger_band:
            self.alert = True
            self.band = "UPPER"
            alert_message = "Price has crossed Upper Bollinger Band"
        elif self.last_price <= self.lower_bollinger_band:
            self.alert = True
            self.band = "LOWER"
            alert_message = "Price has crossed Lower Bollinger Band"
        else:
            alert_message = "All normal"
            self.band = "NORMAL"
            self.alert = False
        self.manage_trade()

    def manage_trade(self):
        if self.in_trade == False and self.alert == True:
            self.current_trade = Trade(self.last_date, self.last_price, self.band, self.upper_trade_multipler, self.lower_trade_multipler)
            self.in_trade = True
            self.alert = False
        elif self.in_trade == True:
            if self.current_trade.band == "UPPER" and self.last_price <= (self.current_trade.alert_price * self.upper_trade_exit):
                self.exit_position()
            elif self.current_trade.band == "LOWER" and self.last_price >= (self.current_trade.alert_price * self.lower_trade_exit):
                self.exit_position()
            elif self.current_trade.trade_start_day < 2:
                 if self.last_date.weekday() == 2 and self.last_tick == True:
                     self.exit_position()
            elif self.current_trade.trade_start_day >= 2 and self.current_trade.trade_start_day <= 4:
                if self.last_date.weekday() == 4 and self.last_tick == True:
                    self.exit_position()

    def convert_datetime(self,epochtime):
        fmt = "%Y-%m-%d %H:%M:%S"
        t = datetime.datetime.fromtimestamp(float(epochtime)/1000.)
        return t.strftime(fmt)

    def exit_position(self):
        self.current_trade.close_trade(self.last_date, self.last_price)
        self.previous_trades.append(self.current_trade)
        self.in_trade = False
        self.alert = False
