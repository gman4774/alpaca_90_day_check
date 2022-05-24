# 90 day asset check for Alpaca.markets
I have a portfolio manager program that trades every day for me on alpaca.markets. One thing I never implemented was to look out for some assets being held for longer trhan I intended, so I put this program together to help with that.

Also Alpaca does not have a simple way to request through the api when you purchased or sold an asset recently, so 
that part of the code might help others with the same problem.

The code is currently set to trade on the paper side of alpaca, keep or change it as you need.


The program pulls all of your accounts trading history, finds the most recent trade for each asset, filters down to only the ones you currently hold, and then it finaly checks for being held for 90 days or more and displays the results if there are any.

