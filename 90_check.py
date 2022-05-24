import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame



API_KEY = "YOURKEYHERE" #API key
API_SECRET = "YOURSECRETHERE" #API secret
APCA_API_BASE_URL = "https://paper-api.alpaca.markets" #https://api.alpaca.markets (for live), https://paper-api.alpaca.markets (for paper)

alp = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

#uncomment this section if you want the program to exit when market is closed
'''
clock = alp.get_clock()
if not clock.is_open:
	print('Market is CLOSED, stopping program. ')
	quit()
else:
	print('Market is OPEN, program is starting. ')
'''

all_pos = []
for pos in alp.list_positions():
	all_pos.append(pos.symbol)

#iterate over all trades and clean up so only keeping most recent and ones that are being currently held
count_orders = []
chunk_size = 500
end_time = (datetime.utcnow())

print('creating trades lists')

count_orders = []
chunk_size = 500
end_time = (datetime.utcnow())
while True:
	order_chunk = alp.list_orders(status='all', nested='False', direction='desc', until=end_time, limit=chunk_size)
	if order_chunk:
		count_orders.extend(order_chunk)
		new_date = pd.Timestamp.to_pydatetime(order_chunk[-1].submitted_at)
		new_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
		end_time = new_date
	else:
		break

full_temp = []
all_dict = {}
for trade in count_orders:
	if trade.filled_at != None:
		full_temp.append((trade.symbol, trade.side, trade.filled_avg_price, trade.filled_at))

for t in list(full_temp):
	for b in list(full_temp):
		if t[0] == b[0] and t[3] > b[3]:
			full_temp.remove(b)

for f in full_temp:
	if (f[1] == 'buy') and (f[0] in all_pos):
		add_days = f[3] + timedelta(90)#adding 90 days to timestamp of when asset was purchased
		all_dict[f[0]] = add_days
		

found = False

print('Looking for assets held for 90 days or more')
for x in all_dict:
	if datetime.now(timezone.utc) >= all_dict[x]: #comparing current timestamp against 90 after purchasing asset
		found = True
		print('ASSET: ' + x)
		print('Date ASSET should have sold: ' + str(all_dict[x]))
		print('Days held too long: ' + str(datetime.now(timezone.utc) - all_dict[x]))
if not found:
	print('No assets are currently being held for 90 days or more')
print('Program Finished')

