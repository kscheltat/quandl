
""" This module analyzes the sentiment data provided by the American Association of Individual Investors ("AAII") which collects sentiment data from its members on 
a weekly basis in regards to the 6 months’ stock market outlook. The module analyzes whether there is a connection between investor sentiment
and future performance of the S&P 500. The S&P 500 performance is measured in the relative change over 6 months. 
The AAII provides three types of sentiment namely bullish, neutral, and bearish such that bullish + neutral + bearish = 1.
"""


import quandl
import datetime
import numpy as np
from sklearn import linear_model as lm
from sklearn.preprocessing import PolynomialFeatures as pf 
from matplotlib import pyplot



def main(col= 1, deg = 1):
    """ Main function which is called at the end of this file. Takes two optional int parameters. col is the column on which 
       the regression is to be performed, for example col = 1 corresponds to the bullish investors; deg determines the degree of the polynomial regression function. 
       Check the data.col attribute for a list of all column names. """

    api_key = 'pqxsHzei5fGpxxCZ-yKH'
    aaii = quandl.dataset('AAII','AAII_SENTIMENT',api_key)
    regdata = createData(aaii)
    clf = lm.TheilSenRegressor()
    poly = pf(degree = deg) 
    X = np.array([e for e in regdata[:,col]]).reshape(-1,1)
    Y = np.array([e for e in regdata[:,4]])
    clf.fit(poly.fit_transform(X),Y)
    print('Regression coefficients: {0}'.format(clf.coef_))
    linsp = np.arange(0., 1., 0.2).reshape(-1,1)
    plotY = clf.predict(poly.fit_transform(linsp))
    pyplot.plot(X,Y, 'o', linsp, plotY)
    pyplot.show()

def createData(data, period = 168):
    """The function createData takes a quandl.dataset object and an optional int parameter period and returns a numpy.array object containing the
      data to be used in the regression analysis. The output colums are as follows: (0) Date, (1) percentage of bullish investors, (2) percentage of neutral investors, 
      (3) percentage of bearish investors, (4) change in the S&P500 between the date of the data and 6 months later (period = 168 days). """
    
    result = []
    endDate = data.end - datetime.timedelta(days = period)
    iterData = [e for e in data.data if e[0] < endDate and (e[12] != None and e[1] != None and e[2] != None and e[3] != None)]
    # Some of the earlier dates are missing some data points. The above if condition filters out all incomplete data points and restricts the analysis to dates that are up to 6 months before the latest data point.
    
    for e in iterData:
        futureValue = data.getFutureValue(e[0],period)[12]
        # Determines the value of the S&P500 6 months later. The if condition insured that such a data point exists.

        deltaSP = futureValue - e[12]
        if e[12] == 0:
            fraction = 0
        else:
            fraction = deltaSP/e[12]
        result.append([e[0], e[1], e[2], e[3], fraction])
    return np.array(result)

main() 


