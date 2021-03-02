import datetime
from yahooquery import Ticker
import matplotlib.pyplot as plt
import pandas as pd

today = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d').date()

from_date = datetime.datetime.strptime("2021-01-06", "%Y-%m-%d").date()

print(f'Collecting data from {from_date} - {today}')
#end_date = date_1 + datetime.timedelta(days=10)
to_date = from_date
spy = Ticker('spy')
li = []
while to_date < today:
    to_date = from_date + datetime.timedelta(days=7)
    print(f'{from_date} - {to_date}')
    temp_df = spy.history(start=from_date, end=to_date, interval="5m")

    li.append(temp_df)
    from_date = to_date

spy_data = pd.concat(li)
outfile = open("spy_data.csv", 'wb')
spy_data.to_csv(outfile, sep='\t', encoding='utf-8')
outfile.close()
