"""Quandl.com is a collection of thousads of finance and economic databases. Please visit Quandl.com for a detailed list of available data.
This modul provides an API to quandl.com. You can get an api key for free by signing up with quandl.com. You can find the api key 
in the account settings.
"""
from urllib.request import urlopen
from datetime import datetime, timedelta
import json
import numpy

class dataset:
    """API to connect to quandl datasets. You can access the data with the 2D numpy.array attribute self.data. First column of the data is the date. 
Attributes:
data -- 2D numpy.array object containing all data
start -- earliest date of the dataset
end -- latest date of the dataset
frequency --  measurement frequency: daily, weekly, quaterly, annually
len -- number or rows in the data
col -- column names of the data
dates -- list of all dates 
attributes -- list of all quandl attributes callable with self.get()
   """
    def __init__(self, database, dataset, api_key):
        #The database variable is the name of the database, the dataset variable is the name of the dataset to be accessed. 

        self.database = database
        self.dataset = dataset
        self.__api_key__ = api_key
        self.__json__ = self.__get__() 
        self.data = numpy.array(self.__json__['data'])
        self.start = datetime.strptime(self.__json__['start_date'], '%Y-%m-%d') 
        self.end = datetime.strptime(self.__json__['end_date'], '%Y-%m-%d') 
        self.frequency = self.__json__['frequency'] 
        self.col = self.__json__['column_names']
        self.dates = [e[0] for e in self] 
        self.len =  sum([1 for e in self.dates])
        self.attributes = self.__json__.keys()
        return None

    def __get__(self):
        #Private method to retrive the data from the dataset. Output is the content of the dataset as a dictionary.
         
        url = "https://www.quandl.com/api/v3/datasets/"+self.database+"/"+self.dataset+".json?api_key="+self.__api_key__
        jsonRequest = urlopen(url).read().decode('utf-8', 'ignore')
        _json = json.loads(jsonRequest)['dataset']
        for e in _json['data']:
            try:
                e[0] = datetime.strptime(e[0], '%Y-%m-%d')
            except:
                print('Dataset is not in the right format; First column has to be a date')
        return _json

    def get(self, attribute):
        # Returns the value of the given quandl attribute. The attribute self.attributes provides a list of all accessible attributes
        return self.__json__[attribute]

    def __iter__(self):
        # Iterator over 2D numpy.array object self.data
        return iter(self.data)

    def getFutureValue(self, currentDate, period):
        #Function returns the row with the date equal to currentDate + period in days. If there is no such row the function returns the row with the closest date prior to currentDate + period. 
        
        if self.data == []:
            try:
                raise ValueError
            except ValueError:
                print('The dataset object contains no data')
        
        tdelta = timedelta(days = period)
        futureDate = currentDate + tdelta
        futureValue = [e for e in self.data if e[0] <= futureDate]
        maxDate = max([e[0] for e in futureValue])
        futureValue = [e for e in futureValue if e[0] == maxDate]
        return futureValue[0] #Will always return a row unless self.data is empty in which case an exception will be thrown. 
