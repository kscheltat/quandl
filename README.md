# quandl API and Data Science Projects

Quandl.com is a collection of thousads of finance and economic databases. Please visit Quandl.com for a detailed list of available data.
This modul provides an API to quandl.com. You can get an api key for free by signing up with quandl.com. You can find the api key 
in the account settings.

docs/quandl.py : \n
This modul handles the quandle.com API. See modul for further documentation. 

docs/AAII.py:
This modul analyzes the sentiment data provided by the Ammerican Association of Individual Investors ("AAII") which collects sentiment data from its members on 
a weekly basis in regards to the 6 months stock market outlook. The modul analyzes whether there is a connection between investor sentiment
and future performance of the S&P 500. The S&P 500 performance is measured in the relative change over 6 months. 
The AAII provides three types of sentiment namely bullish, neutral, and bearish such that bullish + neutral + bearish = 1.
