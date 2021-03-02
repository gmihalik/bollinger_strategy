class Trade():
    def __init__(self, date, alert_price, band, upper_strike_multipler, lower_strike_multipler):
        self.date = date
        self.alert_price = alert_price
        self.band = band
        self.trade_start_day = self.date.weekday()
        self.strike_price = 0
        self.upper_strike_multipler = upper_strike_multipler #1.0125
        self.lower_strike_multipler = lower_strike_multipler #0.975
        self.set_strike_price()
        self.closed = False
        self.closed_date = None
        self.close_price = 0
        self.crossed = False


    def set_strike_price(self):
        if self.band == "UPPER":
            self.strike_price = round(self.alert_price * self.upper_strike_multipler)
        else:
            self.strike_price = round(self.alert_price * self.lower_strike_multipler)

    def close_trade(self, closed_date, close_price):
        self.closed = True
        self.closed_date = closed_date
        self.close_price = close_price

        if self.band == "UPPER" and close_price >= self.strike_price:
            self.crossed = True
        elif self.band == "LOWER" and close_price <= self.strike_price:
            self.crossed = True

        self.write_trade()

    def write_trade(self):
        f = open("trade_results.csv", "a")
        f.write(f'{self.date}\t{self.band}\t{self.alert_price}\t{self.strike_price}\t{self.trade_start_day}\t{self.closed_date}\t{self.close_price}\t{self.crossed}\n')
        f.close()
